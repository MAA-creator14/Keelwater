"""Stage 4a system test harness. Simulation on 80 invented claims.

Usage:
  python3 run_test.py              rules and prototype only (no API calls)
  python3 run_test.py --llm        also run the LLM variant (needs ANTHROPIC_API_KEY in .env)
  python3 run_test.py --reuse-llm  rescore the LLM's saved predictions from results.json, no API calls

Writes results.json and results.md.
"""

import csv
import json
import statistics
import sys
import time
from datetime import date

from variants import LLM, PILES, Prototype, load_env, rules

STALE_DAYS = 60


def load():
    claims = json.load(open("claims.json"))
    labels = {r["id"]: r for r in csv.DictReader(open("labels.csv"))}
    return claims, labels


def data_checks(claims):
    """Completeness, staleness and duplicates, per claim."""
    seen = {}
    flags = {}
    for c in claims:
        f = []
        if not c["policy_number"]:
            f.append("missing_policy_number")
        if any(v is False for v in c["documents"].values()):
            f.append("missing_documents")
        age = (date.fromisoformat(c["received_at"])
               - date.fromisoformat(c["policy_status_checked_at"])).days
        if age > STALE_DAYS:
            f.append("stale_policy_status")
        key = (c["claimant_id"], c["incident_ref"])
        if key in seen:
            f.append("duplicate")
            flags[seen[key]].append("duplicate")
        seen[key] = c["id"]
        flags[c["id"]] = f
    return flags


def grounded(claim, fact):
    """True if a cited fact's field exists in the claim and its value appears there."""
    field = fact["field"].split(".")[0].split("[")[0]
    value = fact["value"].strip()
    if field not in claim or not value:
        return False
    if value == "None":
        return claim[field] is None
    if claim[field] in ([], {}, None):
        return value.lower().startswith(("[]", "none", "empty"))
    return value.lower() in json.dumps(claim[field], ensure_ascii=False).lower()


def score(name, preds, labels, claims, flags, latencies):
    ids = [c["id"] for c in claims]
    by_id = {c["id"]: c for c in claims}
    n = len(ids)
    correct = sum(preds[i]["pile"] == labels[i]["true_pile"] for i in ids)
    wrong_simple = [i for i in ids if preds[i]["pile"] == "simple"
                    and labels[i]["true_pile"] != "simple"]
    linked = [i for i in ids if labels[i]["linked"] == "1"]
    linked_ws = [i for i in wrong_simple if i in linked]
    over = [i for i in ids if labels[i]["true_pile"] == "simple" and preds[i]["pile"] != "simple"]
    flagged = [i for i in ids if flags[i]]
    flagged_simple = [i for i in flagged if preds[i]["pile"] == "simple"]
    facts = [(i, f) for i in ids for f in preds[i].get("cited_facts", [])]
    ungrounded = [(i, f) for i, f in facts if not grounded(by_id[i], f)]
    confusion = {t: {p: 0 for p in PILES + ["refused", "no_answer"]} for t in PILES}
    for i in ids:
        confusion[labels[i]["true_pile"]][preds[i]["pile"]] += 1
    return {
        "variant": name,
        "n": n,
        "accuracy": correct / n,
        "wrong_simple_rate": len(wrong_simple) / n,
        "wrong_simple_ids": wrong_simple,
        "linked_n": len(linked),
        "linked_wrong_simple": len(linked_ws),
        "linked_wrong_simple_ids": linked_ws,
        "over_escalation_rate": len(over) / n,
        "data_flagged_n": len(flagged),
        "data_flagged_sorted_simple": flagged_simple,
        "cited_facts": len(facts),
        "ungrounded_facts": len(ungrounded),
        "ungrounded_examples": [{"id": i, **f} for i, f in ungrounded[:5]],
        "with_reason": sum(bool(preds[i]["reason"]) for i in ids),
        "latency_median_ms": statistics.median(latencies) * 1000 if latencies else None,
        "latency_p90_ms": (statistics.quantiles(latencies, n=10)[-1] * 1000
                           if len(latencies) >= 10 else None),
        "confusion": confusion,
        "latencies": latencies,
    }


def a3a_verdict(variant, baseline):
    """A3a thresholds, locked at the Stage 3 gate."""
    if variant["linked_wrong_simple"] > 0 or variant["wrong_simple_rate"] > baseline:
        return "fail"
    if variant["wrong_simple_rate"] <= baseline / 2:
        return "pass"
    return "investigate"


def l1_result():
    """Label audit: the human's blind re-label of 20 claims against the AI labels it audited
    (labels-v1-ai.csv). The current labels.csv was rebuilt from the human's sorting policy
    after the audit, so the audit is not re-scored against it."""
    labels = {r["id"]: r for r in csv.DictReader(open("labels-v1-ai.csv"))}
    try:
        rows = list(csv.DictReader(open("l1-audit-sheet.csv")))
    except FileNotFoundError:
        return None
    col = next(k for k in rows[0] if k.startswith("your_pile"))
    done = [r for r in rows if r[col].strip()]
    if len(done) < len(rows):
        return {"status": "not complete", "done": len(done), "of": len(rows)}
    agree = sum(r[col].strip() == labels[r["id"]]["true_pile"] for r in done)
    rate = agree / len(done)
    verdict = "pass" if rate >= 0.9 else "fail" if rate < 0.8 else "investigate"
    disagree = [{"id": r["id"], "human": r[col].strip(), "ai": labels[r["id"]]["true_pile"]}
                for r in done if r[col].strip() != labels[r["id"]]["true_pile"]]
    return {"status": "complete", "agreement": rate, "verdict": verdict, "disagreements": disagree}


def run_variant(fn, claims):
    preds, lat = {}, []
    for c in claims:
        t = time.perf_counter()
        preds[c["id"]] = fn(c)
        lat.append(time.perf_counter() - t)
    return preds, lat


def main():
    claims, labels = load()
    flags = data_checks(claims)
    handler = {i: {"pile": labels[i]["handler_pile"], "reason": "", "cited_facts": []}
               for i in labels}

    results = [score("handler baseline (simulated)", handler, labels, claims, flags, [])]
    preds_all = {}
    variants = [("rules", rules), ("prototype stand-in", Prototype())]
    if "--llm" in sys.argv:
        load_env()
        variants.append(("llm", LLM()))
    saved = None
    if "--reuse-llm" in sys.argv:
        old = json.load(open("results.json"))
        saved = (old["predictions"]["llm"],
                 next(r for r in old["results"] if r["variant"] == "llm"))
    for name, fn in variants:
        preds, lat = run_variant(fn, claims)
        preds_all[name] = preds
        results.append(score(name, preds, labels, claims, flags, lat))
    if saved:
        preds_all["llm"] = saved[0]
        r = score("llm", saved[0], labels, claims, flags, saved[1].get("latencies", []))
        if not r["latencies"]:  # results saved before per-claim latencies were kept
            r["latency_median_ms"] = saved[1]["latency_median_ms"]
            r["latency_p90_ms"] = saved[1]["latency_p90_ms"]
        results.append(r)

    baseline = results[0]["wrong_simple_rate"]
    for r in results[1:]:
        r["a3a"] = a3a_verdict(r, baseline)
    l1 = l1_result()

    json.dump({"results": results, "l1": l1, "predictions": preds_all,
               "data_flags": flags}, open("results.json", "w"), indent=1)
    write_md(results, l1, baseline)
    for r in results:
        print(f"{r['variant']:30} acc {r['accuracy']:.0%}  wrong-simple {r['wrong_simple_rate']:.1%}"
              f"  linked wrong-simple {r['linked_wrong_simple']}  A3a {r.get('a3a', '-')}")
    print("L1:", l1)


def write_md(results, l1, baseline):
    out = ["# Stage 4a results\n",
           "**Simulation on 80 invented claims. Small sample. Not evidence about real claims.** "
           "The AI wrote the claims and the rules variant. The correct piles follow the human's "
           "sorting policy (`sorting-policy.csv`), applied to all 80 claims and spot-checked by "
           "the human. The handler baseline is invented. See `test-notes.md`.\n",
           f"A3a thresholds (locked at Stage 3): pass if wrong-simple rate ≤ half the handler "
           f"baseline ({baseline / 2:.1%}) and zero on linked claims; fail if any wrong-simple on "
           f"linked claims or a rate above the baseline ({baseline:.1%}).\n",
           "| Variant | Accuracy | Wrong-simple | Linked wrong-simple | Over-escalation | "
           "Reasons | Ungrounded facts | Median latency | A3a |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        lat = f"{r['latency_median_ms']:.0f} ms" if r["latency_median_ms"] is not None else "-"
        out.append(f"| {r['variant']} | {r['accuracy']:.0%} | {r['wrong_simple_rate']:.1%} "
                   f"({len(r['wrong_simple_ids'])}) | {r['linked_wrong_simple']} of "
                   f"{r['linked_n']} | {r['over_escalation_rate']:.1%} | {r['with_reason']}/"
                   f"{r['n']} | {r['ungrounded_facts']}/{r['cited_facts']} | {lat} | "
                   f"{r.get('a3a', '-')} |")
    out.append("\n## Label audit (L1), against the original AI labels\n")
    if not l1 or l1["status"] != "complete":
        out.append("Not complete, so every A3a verdict above is provisional.\n")
    else:
        out.append(f"Agreement {l1['agreement']:.0%}: **{l1['verdict']}** "
                   f"(pass ≥ 90%, fail < 80%).\n")
        for d in l1["disagreements"]:
            out.append(f"- {d['id']}: you {d['human']}, AI {d['ai']}")
    out.append("\nReason quality is not scored here. It needs the five-point rubric, "
               "scored by a human (Failure 3).\n")
    open("results.md", "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
