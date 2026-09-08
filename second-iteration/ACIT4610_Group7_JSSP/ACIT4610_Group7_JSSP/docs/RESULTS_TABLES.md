# Results Tables — Factual Evidence

These tables are copied from the committed 20-run result CSVs. They are factual evidence for report analysis.

## Required performance statistics

| instance   | category   | parameter_set   |   BKS |   best_Cmax |   worst_Cmax |   average_Cmax |   sample_std_Cmax |   BKS_hit_rate_percent |   average_convergence_generation |
|:-----------|:-----------|:----------------|------:|------------:|-------------:|---------------:|------------------:|-----------------------:|---------------------------------:|
| la01       | Small      | P1              |   666 |         666 |          706 |         674.6  |            11.486 |                     45 |                            30.3  |
| la01       | Small      | P2              |   666 |         666 |          678 |         666.6  |             2.683 |                     95 |                            16.55 |
| la01       | Small      | P3              |   666 |         666 |          666 |         666    |             0     |                    100 |                            12.25 |
| la02       | Small      | P1              |   655 |         671 |          741 |         697.45 |            17.337 |                      0 |                            30.75 |
| la02       | Small      | P2              |   655 |         655 |          687 |         667.95 |             8.338 |                     10 |                            77.35 |
| la02       | Small      | P3              |   655 |         655 |          672 |         660.95 |             4.454 |                     15 |                            89.6  |
| la16       | Medium     | P1              |   945 |         979 |         1008 |         988.2  |             8.612 |                      0 |                            19.4  |
| la16       | Medium     | P2              |   945 |         945 |          982 |         978.95 |             8.127 |                      5 |                            28.35 |
| la16       | Medium     | P3              |   945 |         954 |          982 |         977.25 |             6.735 |                      0 |                            74    |
| la17       | Medium     | P1              |   784 |         784 |          864 |         813    |            17.269 |                      5 |                            53.25 |
| la17       | Medium     | P2              |   784 |         784 |          804 |         793    |             6.806 |                     20 |                            62.85 |
| la17       | Medium     | P3              |   784 |         784 |          804 |         790.5  |             7.851 |                     45 |                           107.95 |
| la31       | Large      | P1              |  1784 |        1786 |         1866 |        1822.9  |            17.973 |                      0 |                            57.65 |
| la31       | Large      | P2              |  1784 |        1784 |         1784 |        1784    |             0     |                    100 |                            84.55 |
| la31       | Large      | P3              |  1784 |        1784 |         1784 |        1784    |             0     |                    100 |                            64.2  |
| la32       | Large      | P1              |  1850 |        1880 |         1941 |        1912.4  |            17.689 |                      0 |                            60.6  |
| la32       | Large      | P2              |  1850 |        1850 |         1868 |        1851.1  |             4.077 |                     90 |                           126.3  |
| la32       | Large      | P3              |  1850 |        1850 |         1850 |        1850    |             0     |                    100 |                           118.75 |

## Time-to-solution and total execution time

| instance   | category   |   BKS |   P1_avg_time_to_best_s |   P1_avg_execution_time_s |   P2_avg_time_to_best_s |   P2_avg_execution_time_s |   P3_avg_time_to_best_s |   P3_avg_execution_time_s |
|:-----------|:-----------|------:|------------------------:|--------------------------:|------------------------:|--------------------------:|------------------------:|--------------------------:|
| la01       | Small      |   666 |                  0.0695 |                    0.2209 |                  0.0793 |                    0.8961 |                  0.1215 |                    2.7318 |
| la02       | Small      |   655 |                  0.0693 |                    0.2173 |                  0.3486 |                    0.8904 |                  0.8418 |                    2.8022 |
| la16       | Medium     |   945 |                  0.0908 |                    0.44   |                  0.2663 |                    1.8208 |                  1.3599 |                    5.4117 |
| la17       | Medium     |   784 |                  0.2319 |                    0.4292 |                  0.5625 |                    1.763  |                  1.9386 |                    5.3577 |
| la31       | Large      |  1784 |                  1.1954 |                    2.0566 |                  3.5371 |                    8.2967 |                  5.4578 |                   25.2352 |
| la32       | Large      |  1850 |                  1.2627 |                    2.0673 |                  5.2577 |                    8.3007 |                 10.0481 |                   25.2616 |

## Notes

- `best_Cmax` = smallest best-so-far makespan observed across the 20 runs.
- `worst_Cmax` = largest best-so-far makespan observed across the 20 runs (worst observed, not a mathematical worst-case bound).
- `sample_std_Cmax` uses sample standard deviation (`ddof=1`).
- `BKS_hit_rate_percent` = percentage of runs that reached the listed JSPLib BKS.
- `average_convergence_generation` = mean generation of the last global-best improvement.
- timing is hardware/system-load dependent.
