"""Reduced 3x3 genotype -> phenotype example required for the report evidence."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.jssp_ga import JSSPInstance, decode_chromosome, schedule_is_feasible

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"

EXAMPLE = JSSPInstance(
    name="illustrative_3x3",
    n_jobs=3,
    n_machines=3,
    jobs=(
        ((0, 3), (1, 2), (2, 2)),
        ((0, 2), (2, 1), (1, 4)),
        ((1, 4), (2, 3), (0, 1)),
    ),
)

CHROMOSOME = [0, 1, 2, 0, 2, 1, 0, 1, 2]


def operation_order(chromosome: list[int]) -> list[tuple[int, int]]:
    next_operation = [0] * EXAMPLE.n_jobs
    order = []
    for job in chromosome:
        order.append((job, next_operation[job]))
        next_operation[job] += 1
    return order


def main() -> None:
    makespan, schedule = decode_chromosome(CHROMOSOME, EXAMPLE)
    feasible = schedule_is_feasible(schedule, EXAMPLE)

    print(f"Genotype: {CHROMOSOME}")
    print(
        "Operation order: "
        + " -> ".join(f"J{job+1}O{op+1}" for job, op in operation_order(CHROMOSOME))
    )
    print(f"Cmax: {makespan}")
    print(f"Feasible: {feasible}\n")

    rows = []
    print("Job  Op  Machine  Duration  Start  Finish")
    for op in schedule:
        print(
            f"{op.job+1:<4} {op.operation+1:<3} {op.machine:<8} "
            f"{op.duration:<9} {op.start:<6} {op.finish}"
        )
        rows.append(
            {
                "job": op.job + 1,
                "operation": op.operation + 1,
                "machine": op.machine,
                "duration": op.duration,
                "start": op.start,
                "finish": op.finish,
            }
        )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(
        RESULTS_DIR / "example_decoding_table.csv", index=False
    )

    fig, ax = plt.subplots(figsize=(9, 4.5))
    for op in schedule:
        ax.barh(
            op.machine,
            op.duration,
            left=op.start,
            edgecolor="black",
            linewidth=0.5,
            alpha=0.82,
        )
        ax.text(
            op.start + op.duration / 2,
            op.machine,
            f"J{op.job+1}O{op.operation+1}",
            ha="center",
            va="center",
            fontsize=9,
        )

    ax.set_yticks(range(EXAMPLE.n_machines))
    ax.set_yticklabels(["M0", "M1", "M2"])
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title(f"Illustrative chromosome decoding — Cmax={makespan}")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "example_decoding_gantt.png", dpi=180)
    plt.close(fig)

    print("\nSaved results/example_decoding_table.csv")
    print("Saved results/example_decoding_gantt.png")


if __name__ == "__main__":
    main()
