"""Analyse the Stage 4b pilot (4b-pilot-results.csv) against A3b. Writes 4b-results.md.

One-person pilot on 24 invented claims: a simulation with a very small sample.
"""

import csv
import statistics

labels = {r["id"]: r["true_pile"] for r in csv.DictReader(open("labels.csv"))}
rows = list(csv.DictReader(open("4b-pilot-results.csv")))
for r in rows:
    r["time_s"] = int(r["time_ms"]) / 1000
    r["true_pile"] = labels[r["claim_id"]]
    r["escalated"] = r["final_pile"] == "suspicious" or r["escalate"] == "1"

w = [r for r in rows if r["condition"] == "with"]
wo = [r for r in rows if r["condition"] == "without"]


def rate(xs, pred):
    return sum(1 for x in xs if pred(x)) / len(xs) if xs else 0


med_w = statistics.median(r["time_s"] for r in w)
med_wo = statistics.median(r["time_s"] for r in wo)
saved = 1 - med_w / med_wo
esc_w, esc_wo = rate(w, lambda r: r["escalated"]), rate(wo, lambda r: r["escalated"])
info_w, info_wo = rate(w, lambda r: r["request_info"] == "1"), rate(wo, lambda r: r["request_info"] == "1")
acc_w, acc_wo = rate(w, lambda r: r["final_pile"] == r["true_pile"]), rate(wo, lambda r: r["final_pile"] == r["true_pile"])
ws_w = [r["claim_id"] for r in w if r["final_pile"] == "simple" and r["true_pile"] != "simple"]
ws_wo = [r["claim_id"] for r in wo if r["final_pile"] == "simple" and r["true_pile"] != "simple"]
overrides = [r for r in w if r["action"] == "override"]
wrong_sugg = [r for r in w if r["ai_pile"] != r["true_pile"]]
accepted_wrong = [r["claim_id"] for r in wrong_sugg if r["action"] == "accept"]
right_sugg = [r for r in w if r["ai_pile"] == r["true_pile"]]
overrode_right = [r["claim_id"] for r in right_sugg if r["action"] == "override"]

if saved <= 0.10 or esc_w > esc_wo:
    verdict = "fail"
elif saved >= 0.30:
    verdict = "pass"
else:
    verdict = "between pass and fail"

out = f"""# Stage 4b pilot results

**One-person pilot on 24 invented claims (12 with an AI suggestion, 12 without). A simulation with a very small sample, not evidence about real handlers.** See `test-notes.md`.

| Measure | With suggestion | Without |
|---|---|---|
| Median time to decision | {med_w:.0f} s | {med_wo:.0f} s |
| Correct pile (against the policy labels) | {acc_w:.0%} | {acc_wo:.0%} |
| Wrong-simple decisions | {len(ws_w)} {ws_w} | {len(ws_wo)} {ws_wo} |
| Escalated (suspicious, or escalate ticked) | {esc_w:.0%} | {esc_wo:.0%} |
| Requested missing information | {info_w:.0%} | {info_wo:.0%} |

**Handler time saved with a suggestion: {saved:.0%}** (median, with against without).

## Trust in the AI suggestion

- Overrides: {len(overrides)} of {len(w)}.
- Wrong AI suggestions accepted: {len(accepted_wrong)} of {len(wrong_sugg)} {accepted_wrong}
- Correct AI suggestions overridden: {len(overrode_right)} of {len(right_sugg)} {overrode_right}

## A3b (thresholds locked at Stage 3)

Pass: 30% or more of handler time saved, with override, reclassification and escalation rates no higher than without. Fail: 10% or less saved, or any of those rates higher.

- Time saved: {saved:.0%}
- Escalations: {esc_w:.0%} with, {esc_wo:.0%} without
- Overrides: can only happen with a suggestion, so there is no "without" rate to compare. Reported above, not tested.
- Reclassifications: happen up to 30 days later, so they can't be measured in a pilot. Not tested.

**Verdict on what could be tested: {verdict}.**
"""
open("4b-results.md", "w").write(out)
print(out)
