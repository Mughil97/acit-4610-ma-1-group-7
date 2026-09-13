"""Experiment configuration for the ACIT4610 Group 7 JSSP project.

The experiment uses two Lawrence instances in each required problem category.
Only population size, generation count, crossover probability, and mutation
probability change across P1/P2/P3. Tournament size and elite count remain fixed.
"""

INSTANCE_GROUPS = {
    "Small": ["la01", "la02"],
    "Medium": ["la16", "la17"],
    "Large": ["la31", "la32"],
}

# Best-known makespans (BKS) for the selected Lawrence JSPLib instances.
BKS = {
    "la01": 666,
    "la02": 655,
    "la16": 945,
    "la17": 784,
    "la31": 1784,
    "la32": 1850,
}

# GA parameter sets tested in the experiments.
PARAMETER_SETS = {
    "P1": {
        "population_size": 50,
        "generations": 100,
        "crossover_probability": 0.70,
        "mutation_probability": 0.05,
    },
    "P2": {
        "population_size": 100,
        "generations": 200,
        "crossover_probability": 0.85,
        "mutation_probability": 0.10,
    },
    "P3": {
        "population_size": 200,
        "generations": 300,
        "crossover_probability": 0.95,
        "mutation_probability": 0.20,
    },
}

# Fixed GA controls.
TOURNAMENT_SIZE = 2
ELITE_SIZE = 2

# Reproducibility controls.
BASE_SEED = 4610
DEFAULT_RUNS = 20
