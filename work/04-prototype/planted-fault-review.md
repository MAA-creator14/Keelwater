# Planted-fault review (Stage 4a)

`SKILL.md` says the AI's review of its own harness only counts if it catches a planted fault.

## How it was run

1. The AI wrote `run_test.py` and `variants.py`.
2. The human planted one or more faults in both files, uncommitted, without saying where or how many.
3. The AI reviewed both files by reading them, without `git diff` or a file comparison, and checked suspected faults by rerunning the harness.
4. The human confirmed the result.

## Result: both planted faults found

| # | File | Fault | Effect | How it was spotted |
|---|---|---|---|---|
| 1 | `run_test.py` | Label-audit pass threshold `>= 0.8` instead of `>= 0.9` | 80–89% agreement would pass the labels; "investigate" became unreachable; the results page still said 90% | Against the thresholds locked at Stage 3 |
| 2 | `variants.py` | New-policy rule `< 3` days instead of `< 30` | K004, K015 and K034 went from suspicious to closer look; accuracy 92% → 89%; wrong-simple rate unchanged | Domain logic, confirmed by rerun |

Fault 2 left the headline metric (wrong-simple rate) unchanged. A check that looked only at that number would have missed it.

## Limit

The AI wrote this code earlier in the same conversation and remembered the original values. Recognising a fault can't be separated from remembering the code, so this is weaker evidence than a review by someone who never saw the original.

## Other findings from the same review (the AI's own code, not planted)

| # | Finding | Action |
|---|---|---|
| 3 | Grounding check accepted empty or "None" citations | Fixed: empty values fail; "None" passes only if the field is empty |
| 4 | LLM call could crash the run if it used up its output tokens | Fixed: `max_tokens` raised to 8,000; a `no_answer` result instead of a crash |
| 5 | Rules sort K068 (33-day-old policy, vague cause) as simple | Not changed: changing rules after seeing results would be tuning on the test set |
| 6 | Prototype smoothing denominator slightly off for 3-value features | Not changed: no effect on the conclusion |
| 7 | Two unused lines | Removed |

After restoring faults 1 and 2, results matched the run before the faults were planted.
