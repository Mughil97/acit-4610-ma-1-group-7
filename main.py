"""Run the full JSSP experiment: every instance x every parameter set x N runs.

ACIT4610 - Mid-Term Group Portfolio 1, Group 7.

Usage:
    python main.py                          # full experiment
    python main.py --group Small            # one size category
    python main.py --runs 10                # fewer independent runs
    python main.py --quick                  # short smoke run
"""

import argparse
import os
import random
import statistics

import pandas as pd

import config
import jssp
import plots


def summarise(results, instance, params_name):
    """Aggregate the runs of one (instance, parameter set) cell."""
    best = [r["best_makespan"] for r in results]
    time_to_best = [r["time_to_best_s"] for r in results]
    execution_times = [r["execution_time_s"] for r in results]
    optimum = config.OPTIMUM.get(instance)

    return {
        "instance": instance,
        "params": params_name,
        "runs": len(results),
        "best": min(best),
        "worst": max(best),
        "mean": round(statistics.mean(best), 2),
        "std": round(statistics.pstdev(best), 2),
        "mean_time_to_best_s": round(statistics.mean(time_to_best), 4),
        "mean_execution_time_s": round(statistics.mean(execution_times), 4),
        "mean_conv_gen": round(statistics.mean(r["convergence_gen"] for r in results), 1),
        "optimum": optimum,
        "gap_%": round(100 * (min(best) - optimum) / optimum, 2) if optimum else None,
    }


def run_cell(jobs, params, n_runs):
    """Run one parameter set on one instance for n_runs independent runs."""
    results = []
    for run in range(n_runs):
        rng = random.Random(config.BASE_SEED + run)
        results.append(jssp.run_ga(jobs, params, rng))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=list(config.GROUPS), help="only this size category")
    parser.add_argument("--runs", type=int, default=config.N_RUNS)
    parser.add_argument("--quick", action="store_true", help="short run for testing")
    args = parser.parse_args()

    groups = {args.group: config.GROUPS[args.group]} if args.group else config.GROUPS
    n_runs = 3 if args.quick else args.runs

    param_sets = config.PARAM_SETS
    if args.quick:
        param_sets = [dict(p, generations=20, pop_size=30) for p in param_sets]

    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    summaries = []

    for group, instances in groups.items():
        for instance in instances:
            jobs = jssp.load_instance(f"{config.DATA_DIR}/{instance}.txt")
            print(f"\n{group} / {instance}: {len(jobs)} jobs x {jssp.n_machines(jobs)} machines, "
                  f"lower bound {jssp.lower_bound(jobs)}, best known {config.OPTIMUM[instance]}")

            best_overall = None
            histories = {}

            for params in param_sets:
                results = run_cell(jobs, params, n_runs)
                row = summarise(results, instance, params["name"])
                summaries.append(row)

                print(
                    f"  {params['name']}: best {row['best']}  worst {row['worst']}  "
                    f"mean {row['mean']}  std {row['std']}  "
                    f"time-to-best {row['mean_time_to_best_s']}s  "
                    f"runtime {row['mean_execution_time_s']}s  "
                    f"conv gen {row['mean_conv_gen']}"
            )

                champion = min(results, key=lambda r: r["best_makespan"])
                histories[params["name"]] = champion["history"]
                if best_overall is None or champion["best_makespan"] < best_overall["best_makespan"]:
                    best_overall = champion

            plots.convergence(
                histories,
                f"{instance} - convergence (best run per parameter set)",
                f"{config.RESULTS_DIR}/{instance}_convergence.png",
            )

            schedule, makespan = jssp.decode(best_overall["best_chromosome"], jobs)
            assert jssp.is_feasible(schedule, jobs), "decoder produced an infeasible schedule"
            plots.gantt(
                schedule, jobs,
                f"{instance} - best schedule, makespan {makespan}",
                f"{config.RESULTS_DIR}/{instance}_gantt.png",
            )

    table = pd.DataFrame(summaries)
    table.to_csv(f"{config.RESULTS_DIR}/summary.csv", index=False)

    time_to_best_table = table.pivot(
        index="instance",
        columns="params",
        values="mean_time_to_best_s"
    )

    execution_time_table = table.pivot(
        index="instance",
        columns="params",
        values="mean_execution_time_s"
    )

    time_to_best_table.to_csv(
        f"{config.RESULTS_DIR}/timing.csv"
    )

    execution_time_table.to_csv(
        f"{config.RESULTS_DIR}/execution_timing.csv"
    )

    print("\n=== summary ===")
    print(table.to_string(index=False))
    print("\n=== mean time to best (seconds) ===")
    print(time_to_best_table.to_string())

    print("\n=== mean execution time (seconds) ===")
    print(execution_time_table.to_string())
    print(f"\nsaved to {config.RESULTS_DIR}/")


if __name__ == "__main__":
    main()
