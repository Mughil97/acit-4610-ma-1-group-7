"""Verification checks for parser, representation, operators and SBA feasibility."""

from pathlib import Path
import random

import config
from jssp_ga import (
    chromosome_is_valid,
    create_individual,
    decode_chromosome,
    genetic_algorithm,
    job_based_crossover,
    load_instance,
    schedule_is_feasible,
    swap_mutation,
)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

EXPECTED = {
    "la01": (10, 5),
    "la02": (10, 5),
    "la16": (10, 10),
    "la17": (10, 10),
    "la31": (30, 10),
    "la32": (30, 10),
}


def main() -> None:
    rng = random.Random(config.BASE_SEED)

    for name, (expected_jobs, expected_machines) in EXPECTED.items():
        instance = load_instance(DATA_DIR / f"{name}.txt")
        assert instance.n_jobs == expected_jobs
        assert instance.n_machines == expected_machines

        parent_1 = create_individual(instance, rng)
        parent_2 = create_individual(instance, rng)
        assert chromosome_is_valid(parent_1, instance)
        assert chromosome_is_valid(parent_2, instance)

        child_1, child_2 = job_based_crossover(parent_1, parent_2, rng)
        assert chromosome_is_valid(child_1, instance)
        assert chromosome_is_valid(child_2, instance)

        mutant = swap_mutation(child_1, rng)
        assert chromosome_is_valid(mutant, instance)

        makespan, schedule = decode_chromosome(mutant, instance)
        assert makespan > 0
        assert schedule_is_feasible(schedule, instance)

        print(f"PASS {name}: parser/representation/operators/SBA feasible")

    # Short end-to-end GA smoke test.
    instance = load_instance(DATA_DIR / "la01.txt")
    result = genetic_algorithm(
        instance,
        population_size=20,
        generations=20,
        crossover_probability=0.80,
        mutation_probability=0.10,
        tournament_size=2,
        elite_size=2,
        seed=2026,
    )
    assert chromosome_is_valid(result.best_chromosome, instance)
    assert schedule_is_feasible(result.best_schedule, instance)
    print(f"PASS end-to-end GA: la01 Cmax={result.best_makespan}")
    print("All verification checks passed.")


if __name__ == "__main__":
    main()
