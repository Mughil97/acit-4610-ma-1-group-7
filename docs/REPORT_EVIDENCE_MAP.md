# Report Evidence Map

This file maps each report requirement to the relevant repository evidence.

## 1. Complete GA design

Use:

```text
README.md
jssp_ga.py
docs/CODE_EXPLANATION.md
```

Implementation elements to describe:

```text
representation
initialisation
selection
crossover
mutation
elitism / replacement
termination
Schedule Building Algorithm
```

## 2. Decoder pseudocode and constraints

Relevant code:

```text
jssp_ga.py -> decode_chromosome()
jssp_ga.py -> _earliest_machine_gap()
jssp_ga.py -> schedule_is_feasible()
```

Core decoder flow:

```text
FOR each job ID in chromosome:
    identify next unscheduled operation of that job
    read required machine and processing time
    release = completion time of preceding job operation
    find earliest non-overlapping idle slot on required machine >= release
    start = earliest feasible time
    finish = start + processing time
    insert operation into machine schedule
    update job-ready time
END
Cmax = largest job completion time
```

Constraint statements:

```text
precedence: start(j,k+1) >= finish(j,k)
machine capacity: operation intervals on the same machine do not overlap
```

## 3. Objective / fitness

Evidence:

```text
Cmax = max_i(C_i)
minimise Cmax
```

The implementation compares decoded makespans directly; lower values win tournament selection.

## 4. Chromosome-decoding example

The reduced genotype-to-schedule example is documented in the final report and is consistent with the chromosome representation described in `README.md` and the decoder implemented in `jssp_ga.py`.

Example genotype:

```text
[0,1,2,0,2,1,0,1,2]
```

The r-th occurrence of a job ID represents that job's r-th operation. The decoder converts the genotype into machine assignments and start/finish times while enforcing precedence and machine-capacity constraints.

For the reduced example used in the report:

```text
Cmax = 12
```

## 5. Compare Small / Medium / Large

Benchmark grouping:

| Category | Instances | Size |
|---|---|---|
| Small | la01, la02 | 10×5 |
| Medium | la16, la17 | 10×10 |
| Large | la31, la32 | 30×10 |

Use:

```text
results/summary_results.csv
results/convergence/*.png
results/gantt/*.png
docs/RESULTS_TABLES.md
```

Compare Best, Worst observed, Mean, Standard Deviation, BKS gap, convergence generation, and execution cost.

## 6. Time required to find the solution

Use:

```text
results/timing_table.csv
```

Primary measure for time-to-solution discussion:

```text
average_time_to_best_seconds
```

Total computational cost:

```text
average_execution_time_seconds
```

Runtime is hardware- and load-dependent. If the experiment is run on another computer, use the timing values generated in that environment.

## 7. Parameter findings / correlation

Parameter configurations:

| Set | Population | Generations | Pc | Pm |
|---|---:|---:|---:|---:|
| P1 | 50 | 100 | 0.70 | 0.05 |
| P2 | 100 | 200 | 0.85 | 0.10 |
| P3 | 200 | 300 | 0.95 | 0.20 |

Important limitation:

```text
population, generations, Pc and Pm change together
```

Therefore the evidence compares **configurations** rather than proving that one individual parameter caused an observed change.

Questions supported by `summary_results.csv`:

- Which configuration gives the lowest average makespan on each instance?
- Which configuration gives the smallest standard deviation?
- Which configuration reaches the BKS most reliably?
- What execution-time increase accompanies P2 and P3?
- Is one configuration strongest for every benchmark?

## 8. Early and later evolutionary stages

Use:

```text
results/convergence/*.png
```

Interpretation prompts:

```text
early stage  -> steeper improvement, more readily available gains
later stage  -> flatter best-so-far curve, fewer improvements, possible convergence
```

Fast stabilisation does not automatically imply a strong solution. Compare both the speed of flattening and the makespan value where the curve stabilises.


## Numerical evidence

The committed `summary_results.csv` contains 20 runs per condition. `raw_results.csv` contains each individual run and seed. Use these files as the numerical evidence source unless the experiment is rerun and the outputs are replaced.
