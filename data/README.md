# Benchmark instances

Instance files from the **Lawrence (1984)** family of the JSPLib benchmark
library: <https://scheduleopt.github.io/benchmarks/jsplib/>

Download the following files into this folder (plain text, JSPLib format):

| Category | Files          | Size              |
| -------- | -------------- | ----------------- |
| Small    | `la01`, `la02` | 10 jobs x 5 machines  |
| Medium   | `la16`, `la17` | 10 jobs x 10 machines |
| Large    | `la31`, `la32` | 30 jobs x 10 machines |

Each file looks like:

```
10 5
1 21 0 53 4 95 3 55 2 34
0 21 3 52 4 16 2 26 1 71
...
```

First line: number of jobs and number of machines. Every following line is one
job, given as `machine time` pairs in the order the operations must run.
Machine numbering is 0-based.
