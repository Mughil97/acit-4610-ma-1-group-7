# Benchmark data

This folder contains six Lawrence (1984) JSSP instances from JSPLib.

| Category | Instances | Size | JSPLib BKS |
|---|---|---|---|
| Small | `la01`, `la02` | 10 jobs × 5 machines | 666, 655 |
| Medium | `la16`, `la17` | 10 jobs × 10 machines | 945, 784 |
| Large | `la31`, `la32` | 30 jobs × 10 machines | 1784, 1850 |

Sources:

- https://scheduleopt.github.io/benchmarks/jsplib/
- https://github.com/ScheduleOpt/benchmarks/tree/main/jobshop/instances/text/Lawrence1984

Format:

```text
number_of_jobs number_of_machines
machine processing_time machine processing_time ...
...
```

Machine IDs in the benchmark files are 0-based.
