# Comparison of Substring Search Algorithms

Three substring search algorithms were compared:

- Boyer-Moore
- Knuth-Morris-Pratt
- Rabin-Karp

The files `1.txt` and `2.txt` were used for testing. For each file, two substrings were tested: one substring that exists in the text and one artificial substring that does not exist in the text. The execution time was measured using `timeit`: each case was run 1000 times, and then the average time of a single run was calculated.

## Tested Substrings

| File | Substring Type | Substring |
| --- | --- | --- |
| `1.txt` | Existing | `алгоритми та структури даних` |
| `1.txt` | Artificial | `вигаданий підрядок якого точно немає у першому тексті` |
| `2.txt` | Existing | `рекомендаційної системи` |
| `2.txt` | Artificial | `вигаданий підрядок якого точно немає у другому тексті` |

## Results for `1.txt`

| Substring | Algorithm | Time, sec | Index |
| --- | --- | ---: | ---: |
| existing | Boyer-Moore | 0.010992 | 468 |
| existing | Knuth-Morris-Pratt | 0.045267 | 468 |
| existing | Rabin-Karp | 0.081833 | 468 |
| artificial | Boyer-Moore | 0.150992 | -1 |
| artificial | Knuth-Morris-Pratt | 1.080278 | -1 |
| artificial | Rabin-Karp | 2.047412 | -1 |

For `1.txt`, the fastest algorithm was Boyer-Moore. It was the fastest both for the existing substring and for the missing substring.

## Results for `2.txt`

| Substring | Algorithm | Time, sec | Index |
| --- | --- | ---: | ---: |
| existing | Boyer-Moore | 0.004166 | 52 |
| existing | Knuth-Morris-Pratt | 0.008064 | 52 |
| existing | Rabin-Karp | 0.013205 | 52 |
| artificial | Boyer-Moore | 0.220598 | -1 |
| artificial | Knuth-Morris-Pratt | 1.617535 | -1 |
| artificial | Rabin-Karp | 2.958767 | -1 |

For `2.txt`, the fastest algorithm was also Boyer-Moore. It showed the lowest execution time in both search scenarios.

## General Conclusion

Based on the total execution time across two texts and two substring types, the results are as follows:

| Algorithm | Total Time, sec |
| --- | ---: |
| Boyer-Moore | 0.386748 |
| Knuth-Morris-Pratt | 2.751144 |
| Rabin-Karp | 5.101217 |

Within this test, Boyer-Moore was the most efficient algorithm overall. Knuth-Morris-Pratt was the second-fastest, while Rabin-Karp showed the highest execution time. The difference was especially noticeable when searching for an artificial substring that was not present in the text.

Boyer-Moore demonstrates high performance by using the bad character rule, which allows parts of the text to be skipped during the search. Knuth-Morris-Pratt works reliably and provides linear search complexity, but in this benchmark it was slower. Rabin-Karp uses hashing to compare substrings, but due to additional match verification checks, it showed the weakest result among the three algorithms.

## Run

```bash
python3 task_03.py
