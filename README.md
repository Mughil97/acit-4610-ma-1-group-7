# Job Shop Scheduling with a Genetic Algorithm

ACIT4610 - Mid-Term Group Portfolio 1 (2026), **Group 7**.

A Genetic Algorithm in Python that solves the Job Shop Scheduling Problem
(JSSP) by minimising the makespan `Cmax`, evaluated on six benchmark instances
from the Lawrence (1984) family of [JSPLib](https://scheduleopt.github.io/benchmarks/jsplib/).

## Installation

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The six instance files are already in `data/`. To download them again:

```bash
for i in la01 la02 la16 la17 la31 la32; do
  curl -o "data/$i.txt" "https://raw.githubusercontent.com/tamy0612/JSPLIB/master/instances/$i"
done
```

## Running

```bash
python verify_project.py           # verify chromosome validity, operators and schedule feasibility
python main.py                     # full experiment: 6 instances x 3 parameter sets x 20 runs
python main.py --group Small       # one size category (Small | Medium | Large)
python main.py --runs 10           # fewer independent runs
python main.py --quick             # short smoke run, finishes in seconds

python example_decode.py           # worked chromosome -> schedule example
python example_decode.py la01      # same, on a real instance
```

`main.py` writes into `results/`:

| File                        | Contents                                             |
| --------------------------- | ---------------------------------------------------- |
| `summary.csv`               | best, worst, mean, std, time-to-best, execution time, convergence generation |
| `timing.csv`                | mean time-to-best, instances x parameter sets         |
| `execution_timing.csv`      | mean total execution time, instances x parameter sets |
| `<instance>_convergence.png`| mean best-so-far makespan per generation across repeated runs                   |
| `<instance>_gantt.png`      | Gantt chart of the best schedule found                |

## Test problems

| Category | Instances    | Size                  | Best known    |
| -------- | ------------ | --------------------- | ------------- |
| Small    | la01, la02   | 10 jobs x 5 machines  | 666, 655      |
| Medium   | la16, la17   | 10 jobs x 10 machines | 945, 784      |
| Large    | la31, la32   | 30 jobs x 10 machines | 1784, 1850    |

## Files

```
config.py            instance groups, the three GA parameter sets, run settings
jssp.py              instance loading, chromosome decoding (SBA), GA operators
plots.py             Gantt chart and convergence curve
main.py              experiment runner, writes tables and plots
example_decode.py    worked genotype -> schedule -> Gantt example
verify_project.py    verifies chromosome validity, GA operators and schedule feasibility
data/                the six JSPLib instance files
results/             generated output
```

## Chromosome representation

An **operation-based repeated-job sequence**: a list of job IDs in which job `j`
appears once for every operation it owns. The k-th occurrence of `j` denotes
operation `k` of job `j`. For three jobs of three operations each:

```
[1, 2, 0, 0, 1, 2, 2, 0, 1]   ->   J1O0, J2O0, J0O0, J0O1, J1O1, J2O1, J2O2, J0O2, J1O2
```

Reading the list left to right always yields the operations of each job in
their required order, so *any* permutation of this multiset is a valid
individual as long as the required number of occurences of each job ID is preserved.
Crossover and mutation only need to preserve the number of genes
per job, and no repair step is ever required.

## Schedule Building Algorithm

The chromosome gives an operation *order*, not start and finish times.
`jssp.decode()` converts it into a feasible schedule using
**earliest-feasible-gap insertion**.

```
for each gene (job j) in the chromosome, left to right:
    k        <- next unscheduled operation of job j
    m, d     <- machine and duration of operation k
    earliest <- finish time of operation k-1 of job j (0 if k = 0)
    start    <- earliest time >= earliest at which machine m has an
                idle gap of length d
    finish   <- start + d
    record (j, k, m, start, finish); mark [start, finish) busy on m

makespan <- latest finish time over all operations
```

The two hard constraints are enforced structurally:

- **precedence** - `start` is never earlier than `earliest`, the finish time of
  the job's previous operation;
- **machine capacity** - `start` is chosen from the idle gaps of machine `m`,
  so no two operations on a machine ever overlap.

Because the decoder searches for the earliest feasible idle gap instead of
automatically appending every operation to the end of the machine schedule,
existing idle time can be used when the precedence constraint allows it.

`jssp.is_feasible()` independently re-checks precedence, machine assignment,
processing duration and machine non-overlap.

## Fitness function
The fitness of a chromosome is the makespan of its decoded schedule,

```
Cmax = max over jobs i of C_i        C_i = finish time of the last operation of job i
```

which the GA **minimises**. Tournament selection compares raw makespans
directly (lower wins), so no fitness scaling is needed.

## Genetic algorithm

| Component     | Choice                                                            |
| ------------- | ----------------------------------------------------------------- |
| Initialisation| random shuffles of the operation multiset                         |
| Selection     | binary tournament (`k = 2`); lower makespan wins                  |
| Crossover     | job-based (half the jobs keep their genes from parent A, the rest are filled from parent B in its own order) |
| Mutation      | swap two positions containing different job IDs                   |
| Elitism       | the best 2 individuals survive unchanged                          |
| Termination   | fixed generation limit                                            |

The swap mutation selects two positions containing different job IDs.
This guarantees that a triggered mutation changes the chromosome while
preserving its length and the required number of occurrences of every job.

## Parameter sets

| Set | Population | Generations | Crossover | Mutation | Tournament | Elitism |
| --- | ---------- | ----------- | --------- | -------- | ---------- | ------- |
| P1  | 50         | 100         | 0.70      | 0.05     | 2          | 2       |
| P2  | 100        | 200         | 0.85      | 0.10     | 2          | 2       |
| P3  | 200        | 300         | 0.95      | 0.20     | 2          | 2       |

Tournament size and elite count are kept fixed across P1-P3, while population
size, generation count, crossover probability and mutation probability are varied.

## Statistical metrics

The GA is stochastic, so every (instance, parameter set) pair is repeated over
`N_RUNS = 20` independent runs with seeds `BASE_SEED + 0 ... 19`.

The reported metrics are:

- **best** - lowest `Cmax` observed across the runs;
- **worst** - highest `Cmax` observed across the runs;
- **mean** - average `Cmax` across the runs;
- **std** - sample standard deviation of `Cmax` across runs;
- **mean_time_to_best_s** - mean elapsed time at which the final global-best solution was discovered;
- **mean_execution_time_s** - mean wall-clock time required to complete the full GA run;
- **mean_conv_gen** - mean generation of the final global-best improvement;
- **best_gap_%** - percentage gap between the best observed makespan and the BKS;
- **mean_gap_%** - percentage gap between the mean makespan and the BKS;
- **bks_hit_%** - percentage of runs that reached or improved upon the BKS.

## Verification

Run:

```bash
python verify_project.py
```

The verification script checks:

- chromosome length and required job multiplicities;
- crossover offspring validity;
- mutation validity and whether a triggered mutation changes the chromosome;
- completeness of decoded schedules;
- precedence and machine-capacity constraints;
- onsistency between the returned makespan and the latest schedule finish time;
- a short end-to-end GA execution.