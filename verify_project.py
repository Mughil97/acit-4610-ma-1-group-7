"""Verification checks for the JSSP Genetic Algorithm implementation.

This script checks that:
1. benchmark instances can be loaded;
2. generated chromosomes contain the correct job multiplicities;
3. crossover preserves chromosome validity;
4. mutation preserves chromosome validity;
5. the decoder produces feasible schedules;
6. the reported makespan matches the decoded schedule;
7. a short end-to-end GA run produces a valid feasible solution.
"""

from collections import Counter
import random

import config
import jssp


def expected_job_counts(jobs):
    """Return the required number of occurrences of each job ID."""
    return Counter(
        {
            job_id: len(operations)
            for job_id, operations in enumerate(jobs)
        }
    )


def chromosome_is_valid(chromosome, jobs):
    """Check chromosome length, job IDs, and required job multiplicities."""

    expected = expected_job_counts(jobs)

    # Correct/Check total chromosome length.
    if len(chromosome) != sum(expected.values()):
        return False

    # Every gene must represent an existing job.
    if any(job_id < 0 or job_id >= len(jobs) for job_id in chromosome):
        return False

    # Every job must occur exactly once for each of its operations.
    return Counter(chromosome) == expected


def check_instance(instance_name):
    """Run representation, crossover, mutation, and decoder checks."""

    jobs = jssp.load_instance(
        f"{config.DATA_DIR}/{instance_name}.txt"
    )

    rng = random.Random(4610)

    # ---------------------------------------------------------
    # 1. INITIALIZATION - Create two random chromosomes.
    # ---------------------------------------------------------

    parent_a = jssp.random_chromosome(jobs, rng)
    parent_b = jssp.random_chromosome(jobs, rng)

    assert chromosome_is_valid(parent_a, jobs)
    assert chromosome_is_valid(parent_b, jobs)

    # ---------------------------------------------------------
    # 2. CROSSOVER
    # ---------------------------------------------------------

    child = jssp.crossover(parent_a, parent_b, rng)

    assert chromosome_is_valid(child, jobs)

    # ---------------------------------------------------------
    # 3. MUTATION
    # ---------------------------------------------------------

    mutant = jssp.mutate(child, rng)

    assert chromosome_is_valid(mutant, jobs)

    if len(set(child)) > 1:
        assert mutant != child

    # ---------------------------------------------------------
    # 4. DECODING / SBA - Decode chromosome into a schedule.
    # ---------------------------------------------------------

    schedule, makespan = jssp.decode(mutant, jobs)

    # Every required operation should appear in the schedule.
    expected_operations = sum(len(job) for job in jobs)

    assert len(schedule) == expected_operations

    # Decoder schedule must satisfy precedence and machine capacity.
    assert jssp.is_feasible(schedule, jobs)

    # Makespan should equal the latest operation finish time.
    calculated_makespan = max(
        finish
        for _, _, _, _, finish in schedule
    )

    assert makespan == calculated_makespan

    print(
        f"PASS {instance_name}: "
        f"chromosome, crossover, mutation and decoder verified "
        f"(Cmax={makespan})"
    )


def check_end_to_end_ga():
    """Run a small/short GA experiment and validate its best solution or best returned chromosome."""

    jobs = jssp.load_instance(
        f"{config.DATA_DIR}/la01.txt"
    )

    # Copy P1 so the real configuration is not modified.
    # Start from P1 but reduce population/generations
    #so this verification finishes quickly. 
    params = dict(config.PARAM_SETS[0])

    # Keep this verification run intentionally short.
    params["pop_size"] = 20
    params["generations"] = 20

    rng = random.Random(2026)

    result = jssp.run_ga(jobs, params, rng)

    best_chromosome = result["best_chromosome"]

    assert chromosome_is_valid(best_chromosome, jobs)

    schedule, makespan = jssp.decode(
        best_chromosome,
        jobs
    )

    assert jssp.is_feasible(schedule, jobs)

    assert makespan == result["best_makespan"]

    print(
        f"PASS end-to-end GA: "
        f"la01 best Cmax={makespan}"
    )


def main():
    """Run all verification checks."""

    print("=== JSSP project verification ===\n")

    for category, instances in config.GROUPS.items():
        print(f"{category} instances")

        for instance_name in instances:
            check_instance(instance_name)

        print()

    check_end_to_end_ga()

    print("\nAll verification checks passed.")


if __name__ == "__main__":
    main()