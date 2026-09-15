# Source Alignment — Course Principles and Project Settings

This note separates course/assignment requirements from settings selected for this implementation.

## Course and assignment principles used directly

- GA lifecycle: **Initialise → Evaluate → Select → Crossover → Mutation → Repeat**.
- Genotype and phenotype are distinct representations.
- A JSSP chromosome stores ordering information and must be decoded before objective evaluation.
- The Schedule Building Algorithm must enforce job precedence and machine capacity.
- The assignment permits an Active schedule builder using earliest valid idle slots.
- Objective: minimise makespan `Cmax`.
- Tournament selection is stochastic; the course/lab example uses two candidates.
- Swap mutation is compatible with order/permutation-style representations.
- Multiple independent runs are required because GA behavior is stochastic.
- Required metrics: Best, Worst, Average, Standard Deviation, Execution Time, and Convergence Generation.

## Project settings

These exact values are implementation settings rather than prescribed values:

```text
Tournament size = 2
Elite count = 2
P1/P2/P3 parameter values
20 runs per condition
BASE_SEED = 4610
```
Tournament size and elite count are held constant across P1/P2/P3 so the three configurations differ only in the four parameters requested for comparison: population size, generation count, crossover probability, and mutation probability.

## Job-Based Crossover (JBX)

The course establishes the broader principle that genetic operators must match the representation. The exact JBX operator used here is a JSSP-specific implementation choice for the repeated-job operation sequence.

Reasoning:

- TSP-style Ordered Crossover commonly assumes unique items;
- the selected JSSP genotype contains repeated job IDs;
- JBX preserves the required occurrence count of every job;
- no repair step is required after crossover.

## Direct makespan minimisation

Tournament selection compares decoded makespans directly:

```text
smaller Cmax = better
```

This avoids unnecessary inverse scaling while preserving the required ordering of solutions.
