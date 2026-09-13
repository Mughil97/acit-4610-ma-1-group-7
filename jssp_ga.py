"""Core Genetic Algorithm for the Job Shop Scheduling Problem (JSSP).

Course-aligned structure:
    Initialise -> Evaluate -> Select -> Crossover -> Mutation -> Repeat

JSSP-specific evaluation:
    operation-sequence genotype -> Active Schedule Building Algorithm (SBA)
    with earliest-feasible-gap insertion -> feasible schedule phenotype
    -> makespan Cmax

Representation
--------------
A chromosome is a repeated-job operation sequence. Job j appears once for each
operation belonging to that job. The k-th occurrence of job j means operation k
of job j. The chromosome therefore contains priority/order information, not
explicit start and finish times.

Decoder / SBA
-------------
The decoder scans the chromosome from left to right. Each next operation is
inserted into the earliest idle interval of its required machine that starts no
earlier than the finish of the preceding operation of the same job.
This Active schedule-building approach uses earliest-feasible-gap insertion
and structurally enforces precedence and machine-capacity constraints.
"""


from dataclasses import dataclass
from pathlib import Path
from random import Random
from time import perf_counter
from typing import Iterable


@dataclass(frozen=True)
class JSSPInstance:
    """
    Parsed JSSP instance.

    jobs[j][k] = (machine_id, processing_time) for operation k of job j.
    """

    name: str
    jobs: tuple[tuple[tuple[int, int], ...], ...]
    n_jobs: int
    n_machines: int

    @property
    def chromosome_length(self) -> int:
        return sum(len(job) for job in self.jobs)


@dataclass(frozen=True)
class ScheduledOperation:
    """One operation in the decoded phenotype/schedule."""

    job: int
    operation: int
    machine: int
    start: int
    finish: int

    @property
    def duration(self) -> int:
        return self.finish - self.start


@dataclass
class GARunResult:
    """Outputs retained from one independent GA run."""

    best_makespan: int
    best_chromosome: list[int]
    best_schedule: list[ScheduledOperation]
    history: list[int]
    convergence_generation: int
    time_to_best_seconds: float
    execution_time_seconds: float


def load_instance(path: str | Path) -> JSSPInstance:
    """Read and validate one JSPLib Lawrence-format instance."""

    path = Path(path)
    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines:
        raise ValueError(f"Empty instance file: {path}")

    header = lines[0].split()
    if len(header) < 2:
        raise ValueError(f"Invalid header in {path}")
    n_jobs, n_machines = map(int, header[:2])

    if len(lines) - 1 < n_jobs:
        raise ValueError(f"{path.name}: expected {n_jobs} job rows")

    jobs: list[tuple[tuple[int, int], ...]] = []
    for job_id, line in enumerate(lines[1 : n_jobs + 1]):
        values = [int(value) for value in line.split()]
        expected_values = 2 * n_machines
        if len(values) != expected_values:
            raise ValueError(
                f"{path.name}, job {job_id}: expected {expected_values} integers, "
                f"got {len(values)}"
            )

        operations: list[tuple[int, int]] = []
        for machine, duration in zip(values[0::2], values[1::2]):
            if not 0 <= machine < n_machines:
                raise ValueError(f"Invalid machine {machine} in job {job_id}")
            if duration <= 0:
                raise ValueError(f"Invalid duration {duration} in job {job_id}")
            operations.append((machine, duration))
        jobs.append(tuple(operations))

    return JSSPInstance(
        name=path.stem,
        jobs=tuple(jobs),
        n_jobs=n_jobs,
        n_machines=n_machines,
    )


def base_chromosome(instance: JSSPInstance) -> list[int]:
    """Create the required repeated-job multiset before shuffling."""

    return [
        job_id
        for job_id, operations in enumerate(instance.jobs)
        for _ in operations
    ]


def create_individual(instance: JSSPInstance, rng: Random) -> list[int]:
    """Create one random valid chromosome by shuffling the operation multiset."""

    chromosome = base_chromosome(instance)
    rng.shuffle(chromosome)
    return chromosome


def chromosome_is_valid(chromosome: Iterable[int], instance: JSSPInstance) -> bool:
    """Return True when length, job IDs, and multiplicities are all correct."""

    chromosome = list(chromosome)
    if len(chromosome) != instance.chromosome_length:
        return False

    expected = [len(job) for job in instance.jobs]
    observed = [0] * instance.n_jobs
    for gene in chromosome:
        if gene < 0 or gene >= instance.n_jobs:
            return False
        observed[gene] += 1
    return observed == expected


def _earliest_machine_gap(
    intervals: list[tuple[int, int]], job_ready_time: int, duration: int
) -> int:
    """
    Return the earliest start >= job_ready_time that does not overlap.

    intervals must be sorted by start time. If no internal gap is large enough,
    the operation is appended after the last conflicting interval.
    """

    start = job_ready_time
    for busy_start, busy_finish in intervals:
        if busy_finish <= start:
            continue
        if start + duration <= busy_start:
            return start
        start = busy_finish
    return start


def decode_chromosome(
    chromosome: list[int], instance: JSSPInstance, *, validate: bool = True
) -> tuple[int, list[ScheduledOperation]]:
    """
    Decode genotype into a feasible active schedule using
    earliest-feasible-gap insertion and return (Cmax, schedule).

    Precedence:
        The k-th occurrence of a job schedules only operation k, and the start
        cannot be earlier than that job's previous-operation finish time.

    Machine capacity:
        The operation is inserted into the earliest non-overlapping idle slot on
        its specified machine.
    """

    if validate and not chromosome_is_valid(chromosome, instance):
        raise ValueError("Invalid chromosome for this instance")

    next_operation = [0] * instance.n_jobs
    job_ready_time = [0] * instance.n_jobs
    machine_intervals: list[list[tuple[int, int]]] = [
        [] for _ in range(instance.n_machines)
    ]
    schedule: list[ScheduledOperation] = []

    for job in chromosome:
        operation = next_operation[job]
        machine, duration = instance.jobs[job][operation]
        intervals = machine_intervals[machine]

        start = _earliest_machine_gap(
            intervals, job_ready_time[job], duration
        )
        finish = start + duration

        # Keep machine intervals sorted by start time.
        insert_at = 0
        while insert_at < len(intervals) and intervals[insert_at][0] <= start:
            insert_at += 1
        intervals.insert(insert_at, (start, finish))

        schedule.append(
            ScheduledOperation(job, operation, machine, start, finish)
        )
        next_operation[job] += 1
        job_ready_time[job] = finish

    # After decoding, each job_ready_time stores the final completion time C_i
    # of one job. The makespan Cmax is the maximum of these completion times.
    makespan = max(job_ready_time)
    return makespan, schedule


def schedule_is_feasible(
    schedule: list[ScheduledOperation], instance: JSSPInstance
) -> bool:
    """Independently re-check completeness, precedence and machine capacity."""

    if len(schedule) != instance.chromosome_length:
        return False

    by_operation = {(op.job, op.operation): op for op in schedule}
    if len(by_operation) != instance.chromosome_length:
        return False

    # Correct operation identity/machine/duration and job precedence.
    for job_id, operations in enumerate(instance.jobs):
        for operation_index, (machine, duration) in enumerate(operations):
            op = by_operation.get((job_id, operation_index))
            if op is None:
                return False
            if op.machine != machine or op.duration != duration:
                return False
            if operation_index > 0:
                previous = by_operation[(job_id, operation_index - 1)]
                if op.start < previous.finish:
                    return False

    # No overlap between consecutive intervals on the same machine.
    per_machine: list[list[ScheduledOperation]] = [
        [] for _ in range(instance.n_machines)
    ]
    for op in schedule:
        per_machine[op.machine].append(op)

    for machine_ops in per_machine:
        machine_ops.sort(key=lambda op: (op.start, op.finish))
        for first, second in zip(machine_ops, machine_ops[1:]):
            if first.finish > second.start:
                return False

    return True


def evaluate(chromosome: list[int], instance: JSSPInstance) -> int:
    """Return objective value Cmax; lower is better."""

    return decode_chromosome(chromosome, instance, validate=False)[0]


def tournament_selection(
    population: list[list[int]], scores: list[int], rng: Random, k: int = 2
) -> list[int]:
    """Binary/k-way tournament selection for minimisation (smaller Cmax wins)."""

    if k < 2 or k > len(population):
        raise ValueError("Tournament size must satisfy 2 <= k <= population size")
    contenders = rng.sample(range(len(population)), k)
    winner = min(contenders, key=lambda index: scores[index])
    return population[winner].copy()


def _job_based_child(
    parent_a: list[int], parent_b: list[int], rng: Random
) -> list[int]:
    """
    Create one Job-Based Crossover (JBX) child.

    Half of the job classes preserve their positions from parent A. Empty
    positions are filled using the relative order of all other job classes from
    parent B. Required job multiplicities are preserved exactly, so repair is
    unnecessary.
    """

    job_classes = sorted(set(parent_a))
    keep_count = max(1, len(job_classes) // 2)
    kept_jobs = set(rng.sample(job_classes, keep_count))

    child: list[int | None] = [
        gene if gene in kept_jobs else None for gene in parent_a
    ]
    fill_values = iter(gene for gene in parent_b if gene not in kept_jobs)

    return [
        gene if gene is not None else next(fill_values)
        for gene in child
    ]


def job_based_crossover(
    parent_a: list[int], parent_b: list[int], rng: Random
) -> tuple[list[int], list[int]]:
    """
    Return two valid JBX children from two parents.

    Each child independently selects a subset of job classes to preserve from
    its first parent, then fills remaining positions from the other parent.
    """

    child_1 = _job_based_child(parent_a, parent_b, rng)
    child_2 = _job_based_child(parent_b, parent_a, rng)
    return child_1, child_2


def swap_mutation(chromosome: list[int], rng: Random) -> list[int]:
    """
    Swap two positions containing different job IDs.

    This preserves job multiplicities and guarantees that a triggered mutation
    actually changes the genotype.
    """

    child = chromosome.copy()
    first = rng.randrange(len(child))
    candidates = [
        index for index, gene in enumerate(child) if gene != child[first]
    ]
    if not candidates:
        return child
    second = rng.choice(candidates)
    child[first], child[second] = child[second], child[first]
    return child


def genetic_algorithm(
    instance: JSSPInstance,
    *,
    population_size: int,
    generations: int,
    crossover_probability: float,
    mutation_probability: float,
    tournament_size: int,
    elite_size: int,
    seed: int,
) -> GARunResult:
    """
    Run one independent GA experiment.

    Flow:
        1. Initialise population.
        2. Evaluate Cmax.
        3. Copy elite survivors.
        4. Select two parents by tournament.
        5. Apply JBX with probability Pc, producing two children.
        6. Apply swap mutation independently to each child with probability Pm.
        7. Evaluate new population and update global best.
        8. Repeat until the fixed generation limit.
    """

    if population_size < 2:
        raise ValueError("population_size must be >= 2")
    if not 0 <= elite_size < population_size:
        raise ValueError("elite_size must satisfy 0 <= elite_size < population_size")
    if not 0 <= crossover_probability <= 1:
        raise ValueError("crossover_probability must be between 0 and 1")
    if not 0 <= mutation_probability <= 1:
        raise ValueError("mutation_probability must be between 0 and 1")

    rng = Random(seed)
    started = perf_counter()

    population = [
        create_individual(instance, rng) for _ in range(population_size)
    ]
    scores = [evaluate(chromosome, instance) for chromosome in population]

    best_index = min(range(population_size), key=lambda i: scores[i])
    best_chromosome = population[best_index].copy()
    best_makespan = scores[best_index]
    history = [best_makespan]
    convergence_generation = 0
    time_to_best_seconds = perf_counter() - started

    for generation in range(1, generations + 1):
        ranked = sorted(range(population_size), key=lambda i: scores[i])
        new_population = [
            population[index].copy() for index in ranked[:elite_size]
        ]

        while len(new_population) < population_size:
            parent_1 = tournament_selection(
                population, scores, rng, tournament_size
            )
            parent_2 = tournament_selection(
                population, scores, rng, tournament_size
            )

            if rng.random() < crossover_probability:
                child_1, child_2 = job_based_crossover(parent_1, parent_2, rng)
            else:
                child_1, child_2 = parent_1.copy(), parent_2.copy()

            if rng.random() < mutation_probability:
                child_1 = swap_mutation(child_1, rng)
            if rng.random() < mutation_probability:
                child_2 = swap_mutation(child_2, rng)

            new_population.append(child_1)
            if len(new_population) < population_size:
                new_population.append(child_2)

        population = new_population
        scores = [evaluate(chromosome, instance) for chromosome in population]

        generation_best_index = min(
            range(population_size), key=lambda i: scores[i]
        )
        generation_best = scores[generation_best_index]

        if generation_best < best_makespan:
            best_makespan = generation_best
            best_chromosome = population[generation_best_index].copy()
            convergence_generation = generation
            time_to_best_seconds = perf_counter() - started

        history.append(best_makespan)

    decoded_makespan, best_schedule = decode_chromosome(
        best_chromosome, instance
    )
    if decoded_makespan != best_makespan:
        raise RuntimeError("Stored best chromosome does not match best makespan")
    if not schedule_is_feasible(best_schedule, instance):
        raise RuntimeError("GA produced an infeasible best schedule")

    return GARunResult(
        best_makespan=best_makespan,
        best_chromosome=best_chromosome,
        best_schedule=best_schedule,
        history=history,
        convergence_generation=convergence_generation,
        time_to_best_seconds=time_to_best_seconds,
        execution_time_seconds=perf_counter() - started,
    )
