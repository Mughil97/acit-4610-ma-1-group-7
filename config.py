"""Experiment settings: instances, GA parameter sets and run counts."""

# Two Lawrence instances per size category.
GROUPS = {
    "Small": ["la01", "la02"],    # 10 jobs x 5 machines
    "Medium": ["la16", "la17"],   # 10 jobs x 10 machines
    "Large": ["la31", "la32"],    # 30 jobs x 10 machines
}

# Best-known makespans from JSPLib, used to report the gap of our solutions.
OPTIMUM = {
    "la01": 666,
    "la02": 655,
    "la16": 945,
    "la17": 784,
    "la31": 1784,
    "la32": 1850,
}

PARAM_SETS = [
    {
        "name": "P1", # default parameters from the report
        "pop_size": 50, # population size
        "generations": 100, # number of generations
        "p_crossover": 0.7, # probability of crossover
        "p_mutation": 0.05, # probability of mutation
        "tournament_k": 3, # tournament size for selection
        "elitism": 2, # number of best individuals to carry over unchanged to the next generation
    },
    {
        "name": "P2",
        "pop_size": 100,
        "generations": 200,
        "p_crossover": 0.85,
        "p_mutation": 0.10,
        "tournament_k": 3,
        "elitism": 2,
    },
    {
        "name": "P3",
        "pop_size": 200,
        "generations": 300,
        "p_crossover": 0.95,
        "p_mutation": 0.20,
        "tournament_k": 5,
        "elitism": 4,
    },
]

N_RUNS = 20        # independent runs per instance and parameter set
BASE_SEED = 4610   # run r uses BASE_SEED + r

DATA_DIR = "data"
RESULTS_DIR = "results"
