"""Run the ACIT4610 Group 7 JSSP experiment.

Default experiment:
    6 benchmark instances x 3 parameter sets x 20 independent runs = 360 runs

Generated evidence:
    results/raw_results.csv
    results/summary_results.csv
    results/timing_table.csv
    results/histories.jsonl
    results/best_chromosomes.json
    results/convergence/*.png
    results/gantt/*.png

Metrics:
    Best Cmax: lowest makespan found across the independent runs.
    Worst Cmax: highest makespan found across the independent runs.
    Average Cmax: mean makespan across the independent runs.
    Sample SD: sample standard deviation of makespan across the runs.
    BKS hit rate: percentage of runs reaching or improving on the stored BKS.

Convergence:
    The convergence generation is the generation in which the final
    global-best makespan was first found and remained the best thereafter.

Timing:
    time_to_best_seconds records when the final best solution was first found.
    execution_time_seconds records the total duration of the complete GA run.

For execution-time comparisons, use the same computer/environment for all
runs and avoid heavy background workloads.
"""

import json
from pathlib import Path

import pandas as pd

import config
from plots import plot_gantt, plot_mean_convergence
from jssp_ga import genetic_algorithm, load_instance

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"


def category_for(instance_name: str) -> str:
    for category, names in config.INSTANCE_GROUPS.items():
        if instance_name in names:
            return category
    raise KeyError(instance_name)


def gap_percent(value: float, bks: float) -> float:
    return 100.0 * (value - bks) / bks


def summarize(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate repeated-run quality, convergence, and timing statistics."""

    rows = []
    grouping = ["instance", "category", "parameter_set", "BKS"]

    for keys, group in raw_df.groupby(grouping, sort=False):
        instance, category, parameter_set, bks = keys
        values = group["best_Cmax"]
        best = int(values.min())
        worst = int(values.max())
        average = float(values.mean())
        std = float(values.std(ddof=1)) if len(values) > 1 else 0.0

        rows.append(
            {
                "instance": instance,
                "category": category,
                "parameter_set": parameter_set,
                "runs": len(group),
                "BKS": int(bks),
                "best_Cmax": best,
                "worst_Cmax": worst,
                "average_Cmax": round(average, 3),
                "sample_std_Cmax": round(std, 3),
                "best_gap_percent": round(gap_percent(best, bks), 3),
                "average_gap_percent": round(gap_percent(average, bks), 3),

                # Percentage of independent runs that reach or improve on the stored BKS.
                "BKS_hit_rate_percent": round(100.0 * float((values <= bks).mean()), 2),
                "average_convergence_generation": round(
                    float(group["convergence_generation"].mean()), 2
                ),
                "average_time_to_best_seconds": round(
                    float(group["time_to_best_seconds"].mean()), 4
                ),
                "average_execution_time_seconds": round(
                    float(group["execution_time_seconds"].mean()), 4
                ),
            }
        )

    return pd.DataFrame(rows)


def build_timing_table(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Create report-ready factual timing evidence (not report prose)."""

    rows = []
    for instance in [
        name for group in config.INSTANCE_GROUPS.values() for name in group
    ]:
        item = {
            "instance": instance,
            "category": category_for(instance),
            "BKS": config.BKS[instance],
        }
        for parameter_set in config.PARAMETER_SETS:
            row = summary_df[
                (summary_df["instance"] == instance)
                & (summary_df["parameter_set"] == parameter_set)
            ].iloc[0]
            item[f"{parameter_set}_avg_time_to_best_s"] = row[
                "average_time_to_best_seconds"
            ]
            item[f"{parameter_set}_avg_execution_time_s"] = row[
                "average_execution_time_seconds"
            ]
        rows.append(item)
    return pd.DataFrame(rows)


def main():
    """
    Run the complete experiment and generate all result evidence files.
    """
    all_instances = [
        name for names in config.INSTANCE_GROUPS.values() for name in names
    ]
    run_count = config.DEFAULT_RUNS

    output_dir = RESULTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "convergence").mkdir(exist_ok=True)
    (output_dir / "gantt").mkdir(exist_ok=True)

    records: list[dict] = []
    histories: dict[str, dict[str, list[list[int]]]] = {
        instance: {parameter: [] for parameter in config.PARAMETER_SETS}
        for instance in all_instances
    }
    best_by_instance: dict[str, dict] = {}

    total = len(all_instances) * len(config.PARAMETER_SETS) * run_count
    completed = 0

    for instance_name in all_instances:
        instance = load_instance(DATA_DIR / f"{instance_name}.txt")
        bks = config.BKS[instance_name]
        category = category_for(instance_name)

        for parameter_name, original_params in config.PARAMETER_SETS.items():
            params = dict(original_params)

            for run_number in range(1, run_count + 1):
                # Use the same deterministic run seeds for every experimental condition.
                seed = config.BASE_SEED + run_number - 1
                result = genetic_algorithm(
                    instance,
                    **params,
                    tournament_size=config.TOURNAMENT_SIZE,
                    elite_size=config.ELITE_SIZE,
                    seed=seed,
                )

                record = {
                    "instance": instance_name,
                    "category": category,
                    "parameter_set": parameter_name,
                    "run": run_number,
                    "seed": seed,
                    **params,
                    "tournament_size": config.TOURNAMENT_SIZE,
                    "elite_size": config.ELITE_SIZE,
                    "BKS": bks,
                    "best_Cmax": result.best_makespan,
                    "gap_percent": round(gap_percent(result.best_makespan, bks), 4),
                    "convergence_generation": result.convergence_generation,
                    "time_to_best_seconds": round(result.time_to_best_seconds, 6),
                    "execution_time_seconds": round(result.execution_time_seconds, 6),
                    "best_chromosome": json.dumps(result.best_chromosome),
                }
                records.append(record)
                histories[instance_name][parameter_name].append(result.history)

                current = best_by_instance.get(instance_name)
                if current is None or result.best_makespan < current["best_makespan"]:
                    best_by_instance[instance_name] = {
                        "parameter_set": parameter_name,
                        "run": run_number,
                        "seed": seed,
                        "best_makespan": result.best_makespan,
                        "chromosome": result.best_chromosome,
                        "schedule": result.best_schedule,
                    }

                completed += 1
                print(
                    f"[{completed:03d}/{total}] {instance_name} {parameter_name} "
                    f"run {run_number:02d}/{run_count}: Cmax={result.best_makespan}"
                )

    raw_df = pd.DataFrame(records)
    raw_df.to_csv(output_dir / "raw_results.csv", index=False)

    summary_df = summarize(raw_df)
    summary_df.to_csv(output_dir / "summary_results.csv", index=False)
    build_timing_table(summary_df).to_csv(output_dir / "timing_table.csv", index=False)

    with (output_dir / "histories.jsonl").open("w", encoding="utf-8") as file:
        for instance_name in all_instances:
            for parameter_name in config.PARAMETER_SETS:
                for run_number, history in enumerate(
                    histories[instance_name][parameter_name], start=1
                ):
                    file.write(
                        json.dumps(
                            {
                                "instance": instance_name,
                                "parameter_set": parameter_name,
                                "run": run_number,
                                "seed": config.BASE_SEED + run_number - 1,
                                "history": history,
                            }
                        )
                        + "\n"
                    )

    best_json = {}
    for instance_name in all_instances:
        best = best_by_instance[instance_name]
        best_json[instance_name] = {
            "parameter_set": best["parameter_set"],
            "run": best["run"],
            "seed": best["seed"],
            "makespan": best["best_makespan"],
            "chromosome": best["chromosome"],
        }

        plot_gantt(
            best["schedule"],
            load_instance(DATA_DIR / f"{instance_name}.txt").n_machines,
            f"{instance_name} best decoded schedule — Cmax={best['best_makespan']}",
            output_dir / "gantt" / f"{instance_name}_best_gantt.png",
        )
        plot_mean_convergence(
            histories[instance_name],
            config.BKS[instance_name],
            f"{instance_name} mean convergence — GA",
            output_dir / "convergence" / f"{instance_name}_convergence.png",
        )

    (output_dir / "best_chromosomes.json").write_text(
        json.dumps(best_json, indent=2), encoding="utf-8"
    )

    print("\nSummary:\n")
    with pd.option_context("display.max_columns", None, "display.width", 220):
        print(summary_df.to_string(index=False))
    print(f"\nFiles written to: {output_dir}")


if __name__ == "__main__":
    main()
