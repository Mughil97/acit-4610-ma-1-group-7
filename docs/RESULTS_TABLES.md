## Required performance statistics

| instance   | category   | parameter_set   |   BKS |   best_Cmax |   worst_Cmax |   average_Cmax |   sample_std_Cmax |   BKS_hit_rate_percent |   average_convergence_generation |
|:-----------|:-----------|:----------------|------:|------------:|-------------:|---------------:|------------------:|-----------------------:|---------------------------------:|
| la01       | Small      | P1              |   666 |         666 |          706 |         674.60 |            11.486 |                     45 |                            30.30 |
| la01       | Small      | P2              |   666 |         666 |          678 |         666.60 |             2.683 |                     95 |                            16.55 |
| la01       | Small      | P3              |   666 |         666 |          666 |         666.00 |             0.000 |                    100 |                            12.25 |
| la02       | Small      | P1              |   655 |         671 |          741 |         697.45 |            17.337 |                      0 |                            30.75 |
| la02       | Small      | P2              |   655 |         655 |          687 |         667.95 |             8.338 |                     10 |                            77.35 |
| la02       | Small      | P3              |   655 |         655 |          672 |         660.95 |             4.454 |                     15 |                            89.60 |
| la16       | Medium     | P1              |   945 |         979 |         1008 |         988.20 |             8.612 |                      0 |                            19.40 |
| la16       | Medium     | P2              |   945 |         945 |          982 |         978.95 |             8.127 |                      5 |                            28.35 |
| la16       | Medium     | P3              |   945 |         954 |          982 |         977.25 |             6.735 |                      0 |                            74.00 |
| la17       | Medium     | P1              |   784 |         784 |          864 |         813.00 |            17.269 |                      5 |                            53.25 |
| la17       | Medium     | P2              |   784 |         784 |          804 |         793.00 |             6.806 |                     20 |                            62.85 |
| la17       | Medium     | P3              |   784 |         784 |          804 |         790.50 |             7.851 |                     45 |                           107.95 |
| la31       | Large      | P1              |  1784 |        1786 |         1866 |        1822.90 |            17.973 |                      0 |                            57.65 |
| la31       | Large      | P2              |  1784 |        1784 |         1784 |        1784.00 |             0.000 |                    100 |                            84.55 |
| la31       | Large      | P3              |  1784 |        1784 |         1784 |        1784.00 |             0.000 |                    100 |                            64.20 |
| la32       | Large      | P1              |  1850 |        1880 |         1941 |        1912.40 |            17.689 |                      0 |                            60.60 |
| la32       | Large      | P2              |  1850 |        1850 |         1868 |        1851.10 |             4.077 |                     90 |                           126.30 |
| la32       | Large      | P3              |  1850 |        1850 |         1850 |        1850.00 |             0.000 |                    100 |                           118.75 |

## Time-to-solution and total execution time

| instance   | category   |   BKS |   P1_avg_time_to_best_s |   P1_avg_execution_time_s |   P2_avg_time_to_best_s |   P2_avg_execution_time_s |   P3_avg_time_to_best_s |   P3_avg_execution_time_s |
|:-----------|:-----------|------:|------------------------:|--------------------------:|------------------------:|--------------------------:|------------------------:|--------------------------:|
| la01       | Small      |   666 |                  0.0455 |                    0.1468 |                  0.0528 |                    0.5970 |                  0.0808 |                    1.8320 |
| la02       | Small      |   655 |                  0.0458 |                    0.1445 |                  0.2320 |                    0.5931 |                  0.5487 |                    1.8186 |
| la16       | Medium     |   945 |                  0.0579 |                    0.2837 |                  0.1696 |                    1.1589 |                  0.8811 |                    3.5348 |
| la17       | Medium     |   784 |                  0.1532 |                    0.2849 |                  0.3686 |                    1.1566 |                  1.2876 |                    3.5472 |
| la31       | Large      |  1784 |                  0.7054 |                    1.2154 |                  2.1129 |                    4.9534 |                  3.2482 |                   14.9430 |
| la32       | Large      |  1850 |                  0.7510 |                    1.2308 |                  3.1565 |                    4.9840 |                  5.9909 |                   15.0263 |

## Notes

- `best_Cmax` = smallest best-so-far makespan observed across the 20 runs.
- `worst_Cmax` = largest best-so-far makespan observed across the 20 runs (worst observed, not a mathematical worst-case bound).
- `sample_std_Cmax` uses sample standard deviation (`ddof=1`).
- `BKS_hit_rate_percent` = percentage of runs that reached or improved on the stored JSPLib BKS.
- `average_convergence_generation` = mean generation in which the final global-best makespan was first found and remained the best thereafter.
- `average_time_to_best_seconds` = mean elapsed time at which the final best solution of each run was first found.
- `average_execution_time_seconds` = mean total runtime of the complete GA run.
- Timing is hardware- and system-load dependent.
