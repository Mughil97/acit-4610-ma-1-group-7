"""Plotting helpers for Gantt and convergence figures."""

from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_gantt(schedule, n_machines: int, title: str, output: str | Path) -> None:
    """Plot one horizontal row per machine and one bar per operation."""

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, max(4.5, 0.55 * n_machines + 2)))
    for op in schedule:
        ax.barh(
            op.machine,
            op.duration,
            left=op.start,
            height=0.72,
            edgecolor="black",
            linewidth=0.25,
            alpha=0.82,
        )
        if op.duration > 0:
            ax.text(
                op.start + op.duration / 2,
                op.machine,
                f"J{op.job}O{op.operation}",
                ha="center",
                va="center",
                fontsize=6,
            )

    ax.set_yticks(range(n_machines))
    ax.set_yticklabels([f"M{machine}" for machine in range(n_machines)])
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_mean_convergence(
    histories_by_parameter: dict[str, list[list[int]]],
    bks: int,
    title: str,
    output: str | Path,
) -> None:
    """Plot mean best-so-far Cmax across repeated runs for each parameter set."""

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for parameter_name, histories in histories_by_parameter.items():
        if not histories:
            continue
        length = min(len(history) for history in histories)
        mean_history = [
            mean(history[generation] for history in histories)
            for generation in range(length)
        ]
        ax.plot(range(length), mean_history, label=parameter_name)

    ax.axhline(bks, linestyle="--", linewidth=1.2, label="JSPLib BKS")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Mean best-so-far makespan")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)
