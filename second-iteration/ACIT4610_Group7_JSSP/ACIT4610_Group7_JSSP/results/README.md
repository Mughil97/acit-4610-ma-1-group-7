# Experiment outputs

This folder contains the 20-run experiment outputs for the six selected Lawrence instances and the three GA parameter sets.

Fixed controls across P1/P2/P3:

```text
tournament size = 2
elite size      = 2
two-child reproduction
swap mutation exchanges different job IDs
```

Files:

- `raw_results.csv` — one row per stochastic run;
- `summary_results.csv` — repeated-run statistics per instance × parameter set;
- `timing_table.csv` — time-to-best and total-execution summaries;
- `convergence/` — mean best-so-far curves;
- `gantt/` — best decoded schedule for each instance;
- `example_decoding_table.csv` and `example_decoding_gantt.png` — reduced decoder example.

Runtime measurements depend on hardware and system load. If the experiment is rerun on another computer, use the timing values generated on that computer for timing comparisons.

Running `python run_experiments.py --runs 20` also writes `histories.jsonl` and `best_chromosomes.json` for reproducibility and plotting support.
