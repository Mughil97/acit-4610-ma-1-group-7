# Assignment Requirements Checklist

## Problem setup

- [x] Lawrence/JSPLib benchmark family used.
- [x] Two Small instances: `la01`, `la02` (10×5).
- [x] Two Medium instances: `la16`, `la17` (10×10).
- [x] Two Large instances: `la31`, `la32` (30×10).
- [x] BKS values recorded for solution-quality comparison.

## Chromosome and Schedule Building Algorithm

- [x] Operation-based repeated-job chromosome.
- [x] Chromosome decoded before objective evaluation.
- [x] Active SBA uses earliest feasible machine idle slots.
- [x] Job precedence enforced.
- [x] Machine capacity enforced.
- [x] `schedule_is_feasible()` independently checks schedules.
- [x] `Cmax` extracted from decoded completion times.

## GA design

- [x] Random initialisation.
- [x] Tournament parent selection.
- [x] JBX crossover compatible with repeated job IDs.
- [x] Swap mutation.
- [x] Elitism.
- [x] Fixed-generation termination.
- [x] Best-so-far tracking.

## Parameter comparison

- [x] Three parameter configurations.
- [x] Population size varied.
- [x] Generation count varied.
- [x] Crossover probability varied.
- [x] Mutation probability varied.
- [x] Tournament size held constant at 2.
- [x] Elite count held constant at 2.

## Statistical performance metrics

- [x] 20 independent runs per instance × parameter-set condition.
- [x] Best `Cmax`.
- [x] Worst observed `Cmax`.
- [x] Average `Cmax`.
- [x] Sample standard deviation.
- [x] Execution time.
- [x] Convergence generation.
- [x] Time to best recorded as additional timing evidence.
- [x] BKS gap and BKS hit rate recorded as additional quality evidence.

## Required decoding example

- [x] Reduced genotype provided.
- [x] Operation order shown by the script.
- [x] Start/finish schedule table generated.
- [x] Gantt chart generated.
- [x] Example makespan calculated.
- [x] Example schedule feasibility checked.

## Repository deliverables

- [x] Executable Python code.
- [x] `README.md` with installation and run instructions.
- [x] Inline documentation and supporting code explanation.
- [x] Dataset files included.
- [x] Verification script included.
- [x] Gantt rendering included.
- [x] Convergence rendering included.
- [x] Raw and summarized experiment outputs included.

## Report evidence available

- [x] Complete GA design evidence.
- [x] Decoder/SBA explanation.
- [x] Constraint-enforcement evidence.
- [x] Objective/fitness evidence.
- [x] Genotype-to-schedule example.
- [x] Small/Medium/Large comparison statistics.
- [x] Time-to-solution table.
- [x] Parameter-set comparison evidence.
- [x] Early/later convergence figures.

## Before submission

- [ ] Run `python verify_project.py` from a clean environment.
- [ ] Confirm the committed results contain 20 runs per instance × parameter-set condition.
- [ ] Confirm the GitHub repository is accessible using the submitted link.
- [ ] Confirm the PDF report is 1000–1500 words.
- [ ] Confirm the report states Group 7.
- [ ] Confirm every numerical report claim matches the committed CSV evidence.
