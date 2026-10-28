"""Stage 5: compare the four options on the same 80 invented claims. Writes comparison.md.

Simulation. Status quo uses the simulated handler piles (invented). Bulk sorting uses filter B
and the human-approved assumption ranges (invented), applied as expected values, not random
draws. Suggested sorting and auto-clear use the 4a and 4b results. Nothing is extrapolated to
real volumes.
"""

import csv
import json
import statistics
from datetime import date

ROOT = "../04-prototype/"
claims = json.load(open(ROOT + "claims.json"))
labels = {r["id"]: r for r in csv.DictReader(open(ROOT + "labels.csv"))}
results = json.load(open(ROOT + "results.json"))
pilot = list(csv.DictReader(open(ROOT + "4b-pilot-results.csv")))

SQ_SECONDS = statistics.median(int(r["time_ms"]) / 1000 for r in pilot if r["condition"] == "without")
SQ_N = sum(1 for r in pilot if r["condition"] == "without")
WITH_SECONDS = statistics.median(int(r["time_ms"]) / 1000 for r in pilot if r["condition"] == "with")

# Human-approved ranges (invented): low, middle, high
ASSUME = {
    "low":    {"scan": 5,  "overhead": 30,  "spot": 0.80, "pull_simple": 0.02},
    "middle": {"scan": 10, "overhead": 60,  "spot": 0.50, "pull_simple": 0.05},
    "high":   {"scan": 20, "overhead": 120, "spot": 0.20, "pull_simple": 0.10},
}
# Observed in the one-person bulk pilot (13 claims, 4 planted): total time spread across claims,
# so overhead is included in the scan time.
bp = list(csv.DictReader(open("bulk-pilot-results.csv")))
planted = set(json.load(open("bulk-planted.json"))["planted_answers"])
ASSUME["pilot-observed"] = {
    "scan": int(bp[0]["batch_time_ms"]) / 1000 / len(bp), "overhead": 0,
    "spot": sum(1 for r in bp if r["claim_id"] in planted and r["pulled_out"] == "1") / len(planted),
    "pull_simple": sum(1 for r in bp if r["claim_id"] not in planted and r["pulled_out"] == "1")
                   / (len(bp) - len(planted)),
}


def in_filter_b(c):
    recent = [h for h in c["claimant_history"]
              if (date.fromisoformat(c["received_at"]) - date.fromisoformat(h["date"])).days <= 365]
    age = (date.fromisoformat(c["incident_date"]) - date.fromisoformat(c["policy_start_date"])).days
    return bool(c["policy_number"] and not any(v is False for v in c["documents"].values())
                and not recent and not c["related_claims"] and age > 60 and c["amount_gbp"] < 1000)


ids = [c["id"] for c in claims]
true = {i: labels[i]["true_pile"] for i in ids}
handler = {i: labels[i]["handler_pile"] for i in ids}
linked = {i for i in ids if labels[i]["linked"] == "1"}
batch = [c["id"] for c in claims if in_filter_b(c)]


def score_piles(piles):
    """piles: {id: {pile: probability}} -> expected counts."""
    ws = sum(p.get("simple", 0) for i, p in piles.items() if true[i] != "simple")
    ws_linked = sum(p.get("simple", 0) for i, p in piles.items() if true[i] != "simple" and i in linked)
    correct = sum(p.get(true[i], 0) for i, p in piles.items())
    over = sum(1 - p.get("simple", 0) for i, p in piles.items() if true[i] == "simple")
    susp = sum(p.get("suspicious", 0) for p in piles.values())
    return {"accuracy": correct / len(piles), "wrong_simple": ws, "linked_wrong_simple": ws_linked,
            "over_escalation": over, "suspicious": susp}


status_quo = score_piles({i: {handler[i]: 1.0} for i in ids})

bulk = {}
for name, a in ASSUME.items():
    piles, seconds = {}, a["overhead"]
    for i in ids:
        if i not in batch:
            piles[i] = {handler[i]: 1.0}
            seconds += SQ_SECONDS
            continue
        seconds += a["scan"]
        p_out = a["spot"] if true[i] != "simple" else a["pull_simple"]
        seconds += p_out * SQ_SECONDS
        # A non-simple claim pulled out has been spotted, so it goes to its correct pile.
        # A simple claim pulled out unnecessarily is sorted by the simulated handler.
        pulled_pile = true[i] if true[i] != "simple" else handler[i]
        piles[i] = {"simple": 1 - p_out}
        piles[i][pulled_pile] = piles[i].get(pulled_pile, 0) + p_out
    bulk[name] = {**score_piles(piles), "seconds_per_claim": seconds / len(ids)}

llm = next(r for r in results["results"] if r["variant"] == "llm")
rules = next(r for r in results["results"] if r["variant"] == "rules")
w = [r for r in pilot if r["condition"] == "with"]
w_correct = sum(1 for r in w if r["final_pile"] == true[r["claim_id"]])
w_ws = sum(1 for r in w if r["final_pile"] == "simple" and true[r["claim_id"]] != "simple")


def f(x, pct=False):
    return f"{x:.0%}" if pct else f"{x:.1f}"


rows = [
    ("Status quo", f"{SQ_SECONDS:.0f} s (n={SQ_N}, one person)", f(status_quo["accuracy"], True),
     f"{status_quo['wrong_simple']:.0f} of 80", f"{status_quo['linked_wrong_simple']:.0f} of {len(linked)}",
     f"{status_quo['over_escalation']:.0f}", "Pile and who sorted it; no reason recorded"),
]
for name in ("low", "middle", "high", "pilot-observed"):
    b = bulk[name]
    rows.append((f"Bulk sorting, filter B ({name}{'' if name == 'pilot-observed' else ' risk'})", f"{b['seconds_per_claim']:.0f} s (modelled)",
                 f(b["accuracy"], True), f"{f(b['wrong_simple'])} of 80",
                 f"{f(b['linked_wrong_simple'])} of {len(linked)}", f(b["over_escalation"]),
                 "One batch decision; the filter criteria serve as the reason"))
rows.append(("Suggested sorting, human decides", f"{WITH_SECONDS:.0f} s (n={len(w)}, one person)",
             f"{w_correct / len(w):.0%} (n={len(w)})", f"{w_ws} of {len(w)}", "not tested in pilot",
             "see 4b", "Pile, structured AI reason, facts, missing information, override reason"))
rows.append(("Auto-clear (ruled out at 4a)", f"{llm['latency_median_ms'] / 1000:.0f} s machine (LLM)",
             f"LLM {llm['accuracy']:.0%}, rules {rules['accuracy']:.0%}",
             f"LLM {len(llm['wrong_simple_ids'])}, rules {len(rules['wrong_simple_ids'])} of 80",
             f"LLM {llm['linked_wrong_simple']}, rules {rules['linked_wrong_simple']} of {len(linked)}",
             f"LLM {llm['over_escalation_rate'] * 80:.0f}, rules {rules['over_escalation_rate'] * 80:.0f}",
             "AI or rule reason; no human decision"))

head = ("| Option | Handler time per claim | Accuracy | Wrong-simple | Linked wrong-simple | "
        "Over-escalation (simple claims sent for checking) | Data output |\n|---|---|---|---|---|---|---|\n")
table = head + "\n".join("| " + " | ".join(r) + " |" for r in rows)

out = f"""# Stage 5 comparison of options

**Simulation on 80 invented claims. Correct piles follow the human's sorting policy. Status quo
handler piles are invented. Bulk-sorting figures are modelled from invented assumptions (low,
middle, high risk), not observed. Pilot timings come from one person.** See
`../04-prototype/test-notes.md` and `assumptions.md`.

Filter B batches {len(batch)} of the 80 claims; {sum(1 for i in batch if true[i] != 'simple')} of
those need a closer look ({', '.join(i for i in batch if true[i] != 'simple')}). Claims outside
the batch are sorted as in the status quo. Inside the batch, simple claims are sorted simple unless
pulled out, so the simulated handler's errors on those claims don't carry over.

{table}

## Not measurable in this simulation

- **Speed to payment** (median and 90th percentile): the claims have no payment timeline, and the
  four-hour waits are an untested question (A1).
- **Reversals**: these happen up to 30 days after sorting.
- **Handler error under pace** for bulk sorting: modelled through the spotting-rate assumption,
  with one observed check from the bulk pilot (one person, 4 planted claims).
"""
open("comparison.md", "w").write(out)
print(out)
