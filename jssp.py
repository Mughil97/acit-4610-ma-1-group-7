"""Core of the JSSP genetic algorithm: instances, decoding and evolution.

Chromosome representation
    An operation-based permutation: a list of job ids in which job j appears
    once for every operation it owns. The k-th occurrence of j means
    "operation k of job j". Every ordering of this list decodes to a legal
    schedule, so crossover and mutation never need a repair step.

Schedule Building Algorithm
    decode() builds an *active* schedule: each operation is placed in the
    earliest idle gap on its machine that starts after the previous operation
    of the same job has finished. This enforces both hard constraints
    (job precedence, one operation per machine at a time) and no operation
    could start earlier without delaying another one.
"""

import time
from bisect import insort

# Local imports
def load_instance(path):
    """Read a JSPLib file and return jobs as [[(machine, duration), ...], ...]."""
    with open(path) as f:
        lines = [ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")]

    n_jobs = int(lines[0].split()[0])
    jobs = []
    for line in lines[1:n_jobs + 1]:
        numbers = [int(x) for x in line.split()]
        jobs.append(list(zip(numbers[0::2], numbers[1::2])))
    return jobs

# Count the number of machines in the instance.
def n_machines(jobs):
    return len({machine for job in jobs for machine, _ in job})

# Compute a lower bound on the optimal makespan.
def lower_bound(jobs):
    """max(longest job, busiest machine) - no schedule can beat this."""
    longest_job = max(sum(d for _, d in job) for job in jobs)

    load = {}
    for job in jobs:
        for machine, duration in job:
            load[machine] = load.get(machine, 0) + duration
    return max(longest_job, max(load.values()))

# Generate a random chromosome.
def random_chromosome(jobs, rng):
    chromosome = []
    for job_id, operations in enumerate(jobs):
        chromosome += [job_id] * len(operations)
    rng.shuffle(chromosome)
    return chromosome

# Find the earliest time when a job can start on a machine.
def _earliest_start(busy, earliest, duration):
    """First time >= earliest where duration fits between the busy intervals."""
    start = earliest
    for busy_start, busy_finish in busy:
        if busy_finish <= start:
            continue
        if start + duration <= busy_start:
            break
        start = busy_finish
    return start

# Decode a chromosome into a schedule.
def decode(chromosome, jobs):
    """Build an active schedule from a chromosome.

    Returns (schedule, makespan) where schedule holds
    (job, operation, machine, start, finish) tuples.
    """
    next_op = [0] * len(jobs)
    job_free = [0] * len(jobs)
    busy = {}
    schedule = []

    for job_id in chromosome:
        op_index = next_op[job_id]
        machine, duration = jobs[job_id][op_index]

        intervals = busy.setdefault(machine, [])
        start = _earliest_start(intervals, job_free[job_id], duration)
        finish = start + duration

        insort(intervals, (start, finish))
        schedule.append((job_id, op_index, machine, start, finish))
        job_free[job_id] = finish
        next_op[job_id] += 1

    return schedule, max(job_free)


def makespan(chromosome, jobs):
    return decode(chromosome, jobs)[1]


def is_feasible(schedule, jobs):
    """True if the schedule respects precedence and machine capacity."""
    finish_of = {(job, op): finish for job, op, _, _, finish in schedule}

    for job, op, machine, start, finish in schedule:
        if finish != start + jobs[job][op][1] or machine != jobs[job][op][0]:
            return False
        if op > 0 and start < finish_of[(job, op - 1)]:
            return False

    per_machine = {}
    for job, op, machine, start, finish in schedule:
        per_machine.setdefault(machine, []).append((start, finish))
    for intervals in per_machine.values():
        intervals.sort()
        if any(a[1] > b[0] for a, b in zip(intervals, intervals[1:])):
            return False
    return True


def tournament(population, scores, k, rng):
    contenders = rng.sample(range(len(population)), k)
    return min(contenders, key=lambda i: scores[i])


def crossover(parent_a, parent_b, rng):
    """Job-based crossover: half the jobs keep their genes from parent A, the
    remaining slots are filled with parent B's genes in its own order, so every
    job keeps exactly the right number of genes."""
    all_jobs = sorted(set(parent_a))
    kept = set(rng.sample(all_jobs, len(all_jobs) // 2))

    child = [gene if gene in kept else None for gene in parent_a]
    fill = iter([gene for gene in parent_b if gene not in kept])
    return [gene if gene is not None else next(fill) for gene in child]


def mutate(chromosome, rng):
    """Swap two genes."""
    child = chromosome[:]
    i, j = rng.sample(range(len(child)), 2)
    child[i], child[j] = child[j], child[i]
    return child


def run_ga(jobs, params, rng):
    """Run the GA once.

    params keys: pop_size, generations, p_crossover, p_mutation,
    tournament_k, elitism.

    Returns a dict with the best solution, the best-so-far history, the
    generation where the best value stabilised, and the run time.
    """
    pop_size = params["pop_size"]
    k = params["tournament_k"]
    elitism = params["elitism"]

    started = time.perf_counter()

    population = [random_chromosome(jobs, rng) for _ in range(pop_size)]
    scores = [makespan(c, jobs) for c in population]

    best = min(range(pop_size), key=lambda i: scores[i])
    best_chromosome, best_score = population[best][:], scores[best]
    history = [best_score]
    convergence_gen = 0

    for generation in range(1, params["generations"] + 1):
        ranked = sorted(range(pop_size), key=lambda i: scores[i])
        new_population = [population[i][:] for i in ranked[:elitism]]

        while len(new_population) < pop_size:
            child = population[tournament(population, scores, k, rng)][:]
            if rng.random() < params["p_crossover"]:
                mate = population[tournament(population, scores, k, rng)]
                child = crossover(child, mate, rng)
            if rng.random() < params["p_mutation"]:
                child = mutate(child, rng)
            new_population.append(child)

        population = new_population
        scores = [makespan(c, jobs) for c in population]

        best = min(range(pop_size), key=lambda i: scores[i])
        if scores[best] < best_score:
            best_chromosome, best_score = population[best][:], scores[best]
            convergence_gen = generation
        history.append(best_score)

    return {
        "best_makespan": best_score,
        "best_chromosome": best_chromosome,
        "history": history,
        "convergence_gen": convergence_gen,
        "time": time.perf_counter() - started,
    }
