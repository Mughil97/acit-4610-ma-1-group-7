"""Worked chromosome decoding example for the report.

Prints the chromosome, the operation order the decoder reads from it, the
resulting start/finish table, and saves the matching Gantt chart.

Usage:
    python example_decode.py            # small 3x3 illustrative instance
    python example_decode.py la01       # a real benchmark instance
"""

import os
import random
import sys

import config
import jssp
import plots

# 3 jobs x 3 machines, small enough to check the decoder by hand.
EXAMPLE = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 2), (2, 1), (1, 4)],
    [(1, 4), (2, 3), (0, 1)],
]


def operation_order(chromosome, jobs):
    """Expand the chromosome into the (job, operation) sequence it encodes."""
    next_op = [0] * len(jobs)
    order = []
    for job_id in chromosome:
        order.append((job_id, next_op[job_id]))
        next_op[job_id] += 1
    return order


def main():
    os.makedirs(config.RESULTS_DIR, exist_ok=True)

    if len(sys.argv) > 1:
        name = sys.argv[1]
        jobs = jssp.load_instance(f"{config.DATA_DIR}/{name}.txt")
        chromosome = jssp.random_chromosome(jobs, random.Random(config.BASE_SEED))
    else:
        name = "example"
        jobs = EXAMPLE
        chromosome = [1, 2, 0, 0, 1, 2, 2, 0, 1]

    print(f"instance: {name}  ({len(jobs)} jobs x {jssp.n_machines(jobs)} machines)")
    for job_id, operations in enumerate(jobs):
        print(f"  job {job_id}: " + "  ".join(f"M{m}({d})" for m, d in operations))

    print(f"\nchromosome:      {chromosome}")
    print("operation order: " + " -> ".join(
        f"J{job}O{op}" for job, op in operation_order(chromosome, jobs)))

    schedule, makespan = jssp.decode(chromosome, jobs)

    print(f"\n{'job':>4} {'op':>3} {'machine':>8} {'start':>6} {'finish':>7}")
    for job, op, machine, start, finish in schedule:
        print(f"{job:>4} {op:>3} {machine:>8} {start:>6} {finish:>7}")

    print(f"\nmakespan: {makespan}")
    print(f"feasible: {jssp.is_feasible(schedule, jobs)}")

    path = f"{config.RESULTS_DIR}/{name}_decode_gantt.png"
    plots.gantt(schedule, jobs, f"{name} - decoded chromosome, makespan {makespan}", path)
    print(f"gantt:    {path}")


if __name__ == "__main__":
    main()
