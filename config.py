#Configuration for the JSSP project

"""We have three groups of scenarios (small, medium, large), 
each with two instances from the Lawrence family within the GitHub-folder
provided in the assignment.

Tournament size and elitism have fixed values, while the remaining 
parameters changes across the parameter sets."""

#our three groups of scenarios
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

#setting parameters
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

#fized values
TOURNAMENT_SIZE = 2
ELITE_SIZE = 2

# Reproducibility controls.
BASE_SEED = 4610
DEFAULT_RUNS = 20
