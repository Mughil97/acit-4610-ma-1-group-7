# Job Shop Scheduling with a Genetic Algorithm

**ACIT4610 – Mid-Term Group Portfolio/Project 1 (2026), Group 7**

This repository implements a Genetic Algorithm (GA) for the Job Shop Scheduling Problem (JSSP) using six Lawrence (1984) benchmark instances from JSPLib.

The implementation follows the GA flow used in the course:

> **Initialize → Evaluate → Select → Crossover → Mutation → Repeat**

For JSSP, evaluation first requires chromosome decoding:

> **operation-based genotype → Active Schedule Building Algorithm (SBA) → feasible schedule phenotype → makespan `Cmax`**

## Benchmark instances

| Category | Instances | Size | JSPLib BKS |
|---|---|---:|---:|
| Small | `la01`, `la02` | 10 jobs × 5 machines | 666, 655 |
| Medium | `la16`, `la17` | 10 jobs × 10 machines | 945, 784 |
| Large | `la31`, `la32` | 30 jobs × 10 machines | 1784, 1850 |

Dataset source: JSPLib, Lawrence1984 family.

- https://scheduleopt.github.io/benchmarks/jsplib/
- https://github.com/ScheduleOpt/benchmarks/tree/main/jobshop/instances/text/Lawrence1984

## GA design

### 1. Chromosome representation

A chromosome is an **operation-based repeated-job sequence**. Job `j` appears once for every operation belonging to that job.

Example for three jobs with three operations each:

```text
[0, 1, 2, 0, 2, 1, 0, 1, 2]
```

The first occurrence of `0` represents the first operation of Job 0, the second occurrence represents its second operation, and so on. The chromosome is the **genotype**; it stores operation-order information rather than explicit start and finish times.

### 2. Initialization

The program builds the required repeated-job multiset and shuffles it. This creates random valid chromosomes while preserving the correct number of operations for every job.

### 3. Schedule Building Algorithm (SBA)

`decode_chromosome()` constructs an **Active schedule** by reading the chromosome from left to right.

For each gene:

1. identify that job's next unscheduled operation;
2. read its required machine and processing time;
3. obtain the earliest release time from the completion of the preceding operation of the same job;
4. inspect the occupied intervals on the required machine;
5. place the operation into the earliest non-overlapping idle slot that begins no earlier than its release time;
6. record start and finish times;
7. continue until all operations are scheduled.

The decoder enforces both JSSP constraints:

- **precedence:** operation `k+1` cannot start before operation `k` finishes;
- **machine capacity:** a machine processes at most one operation at a time.

`schedule_is_feasible()` independently re-checks completeness, precedence, machine assignment, processing duration, and machine non-overlap.

### 4. Objective / fitness evaluation

The objective is:

```text
minimize Cmax = max_i(C_i)
```

where `C_i` is the completion time of the last operation of job `i`.

The implementation compares decoded makespans directly:

```text
smaller Cmax = better
```

Tournament selection therefore chooses the candidate with the lower makespan.

### 5. Parent selection

**Binary tournament selection (`k=2`)** is used. Two chromosomes are sampled at random, evaluated by makespan, and the one with the lower `Cmax` is selected as a parent.

### 6. Crossover

**Job-Based Crossover (JBX)** is used because the operation-sequence representation contains repeated job IDs. A subset of job classes is preserved from one parent and the remaining positions are filled in the order supplied by the other parent. Two children are produced by reversing the parent roles.

JBX preserves the required number of occurrences of each job, so no repair step is required.

### 7. Mutation

**Swap mutation** exchanges two positions containing different job IDs. The order changes while job multiplicities remain valid.

### 8. Elitism and best-so-far tracking

The two best chromosomes are copied unchanged to the next generation. The program also stores the best solution observed throughout each run.

### 9. Termination

Each parameter set uses a fixed generation limit. The program also records the generation of the last best-so-far improvement as the convergence-generation measure.

## Parameter sets

The four parameters requested in the assignment are varied across three configurations. Tournament size and elitism are held constant.

| Set | Population | Generations | Crossover probability | Mutation probability |
|---|---:|---:|---:|---:|
| P1 | 50 | 100 | 0.70 | 0.05 |
| P2 | 100 | 200 | 0.85 | 0.10 |
| P3 | 200 | 300 | 0.95 | 0.20 |

Because the four values change together, the experiment compares **parameter-set configurations** rather than isolating one-parameter causality.

Fixed controls:

```text
tournament size = 2
elite size      = 2
```

## Installation

Requires Python 3.10 or newer.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Verification

Run the verification script before experiments:

```bash
python verify_project.py
```

Expected message:

```text
All verification checks passed.
```

The verifier checks:

- all six benchmark files and expected dimensions;
- chromosome validity;
- JBX offspring validity;
- swap-mutation validity;
- decoder feasibility;
- precedence constraints;
- machine non-overlap;
- a short end-to-end GA run.

## Main experiment

The default experiment uses 20 independent runs for every instance × parameter-set condition:

```bash
python run_experiments.py
```

This executes:

```text
6 instances × 3 parameter sets × 20 runs = 360 GA runs
```

The assignment permits 10–30 independent runs. For timing comparisons, run all configurations on the same computer under comparable load.

## Generated outputs

```text
results/
├── raw_results.csv
├── summary_results.csv
├── timing_table.csv
├── histories.jsonl
├── best_chromosomes.json
├── example_decoding_table.csv
├── example_decoding_gantt.png
├── convergence/
│   ├── la01_convergence.png
│   └── ...
└── gantt/
    ├── la01_best_gantt.png
    └── ...
```

### `raw_results.csv`

One row per independent run, including:

- instance and category;
- parameter set;
- seed;
- GA parameter values;
- best `Cmax`;
- BKS gap;
- convergence generation;
- time to best;
- total execution time;

### `summary_results.csv`

For each instance × parameter-set condition:

- Best `Cmax`;
- Worst observed `Cmax`;
- Average `Cmax`;
- Sample standard deviation;
- BKS gap;
- BKS hit rate;
- average convergence generation;
- average time to best;
- average execution time.

### Convergence figures

Each convergence figure shows the **mean best-so-far makespan across the independent runs** for P1, P2, and P3, together with the JSPLib BKS reference line.

### Gantt figures

Each Gantt figure visualizes the best decoded schedule observed for that benchmark instance.


## AI Use Disclosure

During the development of this project, generative AI tools, including ChatGPT (OpenAI) and Claude (Anthropic), were used as supporting tools for permitted coding-related activities.

The tools were used for:

- **Technical and coding clarification:** Clarifying programming concepts, algorithm behaviour, and implementation requirements.

- **Data visualization:** Assisting with Python/Matplotlib code used to generate plots and visualise experimental results.

- **Code review and refactoring:** Assisting with debugging and refactoring code for better performance, readability, and structure.

All algorithmic decisions, parameter choices, experiments, outputs, and final code were reviewed and verified by the group.

The final written report was produced by the group members in their own words in accordance with the assignment's AI-use requirements.
