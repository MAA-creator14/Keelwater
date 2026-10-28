# Stage 4a results

**Simulation on 80 invented claims. Small sample. Not evidence about real claims.** The correct piles were set by the AI, which also wrote the claims and the rules variant. The handler baseline is invented.

A3a thresholds (locked at Stage 3): pass if wrong-simple rate ≤ half the handler baseline (3.1%) and zero on linked claims; fail if any wrong-simple on linked claims or a rate above the baseline (6.2%).

| Variant | Accuracy | Wrong-simple | Linked wrong-simple | Over-escalation | Reasons | Ungrounded facts | Median latency | A3a |
|---|---|---|---|---|---|---|---|---|
| handler baseline (simulated) | 89% | 6.2% (5) | 4 of 17 | 5.0% | 0/80 | 0/0 | - | - |
| rules | 92% | 5.0% (4) | 2 of 17 | 2.5% | 80/80 | 0/96 | 0 ms | fail |
| prototype stand-in | 50% | 28.7% (23) | 8 of 17 | 7.5% | 0/80 | 0/0 | 0 ms | fail |

## Label audit (L1)

Not complete, so every A3a verdict above is provisional.


Reason quality is not scored here. It needs the five-point rubric, scored by a human (Failure 3).

