"""Gantt chart and convergence curve rendering."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def gantt(schedule, jobs, title, path):
    """One row per machine, one coloured bar per operation, labelled by job."""
    machines = sorted({machine for _, _, machine, _, _ in schedule})
    colours = plt.get_cmap("tab20")(range(20))

    fig, ax = plt.subplots(figsize=(12, 0.5 * len(machines) + 2))

    for job, op, machine, start, finish in schedule:
        row = machines.index(machine)
        ax.broken_barh(
            [(start, finish - start)],
            (row - 0.4, 0.8),
            facecolors=colours[job % 20],
            edgecolors="white",
            linewidth=0.5,
        )
        if finish - start > 0.02 * max(f for *_, f in schedule):
            ax.text(
                (start + finish) / 2, row, str(job),
                ha="center", va="center", fontsize=7, color="white",
            )

    ax.set_yticks(range(len(machines)))
    ax.set_yticklabels([f"M{m}" for m in machines])
    ax.invert_yaxis()
    ax.set_xlabel("time")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def convergence(histories, title, path):
    """Best-so-far makespan against generation; histories maps label -> list."""
    fig, ax = plt.subplots(figsize=(8, 5))

    for label, history in histories.items():
        ax.plot(history, label=label, linewidth=1.5)

    ax.set_xlabel("generation")
    ax.set_ylabel("best makespan so far")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
