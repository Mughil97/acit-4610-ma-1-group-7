# Comprehensive Code Explanation

This document explains the implementation structure and the reasoning behind each major function.

## `jssp_ga.py`

### `JSSPInstance`

Stores the benchmark instance:

```text
jobs[job][operation] = (machine, processing_time)
```

### `ScheduledOperation`

Stores one operation in the decoded schedule:

```text
job
operation
machine
start
finish
duration
```

### `base_chromosome()`

Builds the required repeated-job multiset. For a 3×3 example:

```text
[0,0,0,1,1,1,2,2,2]
```

### `create_individual()`

Copies and shuffles the base chromosome. The result is a random **valid chromosome**, not yet a schedule.

### `chromosome_is_valid()`

Checks:

- total chromosome length;
- legal job IDs;
- exact number of required occurrences for each job.

## Decoder / Active SBA

### `_earliest_machine_gap()`

Receives:

```text
occupied intervals on one machine
job-ready time
operation duration
```

It scans occupied intervals from left to right and returns the earliest non-overlapping start time.

### `decode_chromosome()`

Maintains three state structures:

```text
next_operation[job]
job_ready_time[job]
machine_intervals[machine]
```

For each gene:

```text
job ID
  ↓
next operation of that job
  ↓
(machine, duration)
  ↓
release = previous operation finish
  ↓
earliest idle machine slot >= release
  ↓
start and finish
```

After all genes:

```text
Cmax = maximum job completion time
```

### Precedence constraint

Operation `k+1` cannot start before operation `k` finishes because its release time is the stored completion time of the preceding operation of the same job.

### Machine-capacity constraint

Every operation is inserted only into an idle interval on its required machine. Two operations assigned to the same machine therefore cannot overlap.

### `schedule_is_feasible()`

Independently checks:

1. every operation is present exactly once;
2. correct machine and processing duration;
3. job precedence;
4. valid start/finish duration;
5. no machine overlap.

## Objective / evaluation

`evaluate()` returns the decoded makespan:

```text
smaller Cmax = better
```

## Tournament selection

With `k=2`:

```text
randomly choose candidate A and B
compare decoded Cmax
return the chromosome with smaller Cmax
```

## Job-Based Crossover (JBX)

The parent chromosomes contain repeated job IDs.

For one child:

1. select half of the job classes to preserve;
2. preserve the positions of those jobs from the first parent;
3. fill the empty positions using the relative order of the remaining job classes from the second parent.

Two children are produced using reversed parent roles. Each child independently selects its preserved subset of job classes. The operator preserves chromosome length and job multiplicities, so no repair step is required.

## Swap mutation

Two positions containing **different job IDs** are exchanged. This changes sequencing while preserving all job counts.

## Main GA loop

```text
INITIALISE population
EVALUATE population
FOR each generation:
    copy the top two elites
    WHILE the new population is not full:
        SELECT parent 1 by binary tournament
        SELECT parent 2 by binary tournament
        CROSSOVER with probability Pc
        MUTATE child 1 with probability Pm
        MUTATE child 2 with probability Pm
        add children
    EVALUATE the new population
    update the best-so-far solution
REPEAT until the generation limit
```

### Best-so-far solution

The best solution observed anywhere during one run.

### Convergence generation

The generation in which the final global-best makespan was first found and remained the best thereafter.

### Time to best

Elapsed wall-clock time when the best-so-far makespan that remained unbeaten for the rest of the run was first discovered.

### Execution time

Total wall-clock time required to complete the configured generations.

## `run_experiments.py`

The main experiment runs:

```text
6 instances × 3 parameter sets × 20 independent runs = 360 runs
```

Within each condition, seeds 4610–4629 are used. Reusing the same seed set across parameter configurations supports reproducible comparisons.

Generated outputs:

```text
raw_results.csv
summary_results.csv
timing_table.csv
histories.jsonl
best_chromosomes.json
mean convergence plots
best Gantt charts
```

## Reduced decoding example

The final report contains a reduced 3×3 genotype-to-schedule example using:

```text
[0,1,2,0,2,1,0,1,2]
```

The example demonstrates:

```text
genotype → operation order → machine assignment → start/finish times → Cmax
```

The resulting feasible schedule has:
```text
Cmax = 12
```

The same decoding principles are implemented by `decode_chromosome()` in `jssp_ga.py`.

## `verify_project.py`

Checks dataset loading, chromosome validity, JBX validity, mutation validity, decoder feasibility, makespan consistency, and a short end-to-end GA run.

