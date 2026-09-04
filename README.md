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
| `summary.csv`               | best, worst, mean, std, time, convergence generation |
| `timing.csv`                | mean run time, instances x parameter sets            |
| `<instance>_convergence.png`| best-so-far makespan per generation                  |
| `<instance>_gantt.png`      | Gantt chart of the best schedule found               |

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
data/                the six JSPLib instance files
results/             generated output
```

## Chromosome representation

An **operation-based permutation**: a list of job ids in which job `j` appears
once for every operation it owns. The k-th occurrence of `j` denotes operation
`k` of job `j`. For three jobs of three operations each:

```
[1, 2, 0, 0, 1, 2, 2, 0, 1]   ->   J1O0, J2O0, J0O0, J0O1, J1O1, J2O1, J2O2, J0O2, J1O2
```

Reading the list left to right always yields the operations of each job in
their required order, so *any* permutation of this multiset is a valid
individual. Crossover and mutation only need to preserve the number of genes
per job, and no repair step is ever required.

## Schedule Building Algorithm

The chromosome gives an operation *order*, not times. `jssp.decode()` turns it
into an **active schedule**:

```
for each gene (job j) in the chromosome, left to right:
    k        <- next unscheduled operation of job j
    m, d     <- machine and duration of operation k
    earliest <- finish time of operation k-1 of job j   (0 if k = 0)
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

Because operations are inserted into the *earliest* idle gap rather than
appended to the end of the machine, no operation could start earlier without
delaying another one, i.e. the schedule is active rather than merely
semi-active. `jssp.is_feasible()` re-checks both constraints and is asserted on
every schedule that gets plotted.

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
| Selection     | k-way tournament                                                  |
| Crossover     | job-based (half the jobs keep their genes from parent A, the rest are filled from parent B in its own order) |
| Mutation      | swap two genes                                                    |
| Elitism       | the best few individuals survive unchanged                        |
| Termination   | fixed generation limit                                            |

## Parameter sets

| Set | Population | Generations | Crossover | Mutation | Tournament | Elitism |
| --- | ---------- | ----------- | --------- | -------- | ---------- | ------- |
| P1  | 50         | 100         | 0.70      | 0.05     | 3          | 2       |
| P2  | 100        | 200         | 0.85      | 0.10     | 3          | 2       |
| P3  | 200        | 300         | 0.95      | 0.20     | 5          | 4       |

## Statistical metrics

The GA is stochastic, so every (instance, parameter set) pair is repeated over
`N_RUNS = 20` independent runs with seeds `BASE_SEED + 0 … 19`, and reported as:

- **best** - lowest `Cmax` over the runs;
- **worst** - highest `Cmax`, the worst-case bound;
- **mean** and **std** - central tendency and stability;
- **mean_time_s** - wall-clock seconds per run;
- **mean_conv_gen** - generation at which the best value stopped improving;
- **gap_%** - distance of the best solution from the JSPLib best-known value.
