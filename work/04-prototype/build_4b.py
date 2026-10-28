"""Build the Stage 4b pilot screen (4b-pilot.html) from the pilot set and saved suggestions.

The page holds no correct piles. Claims alternate between "with suggestion" and "without",
in a fixed shuffled order. Decisions are timed and saved in the browser, and can be
downloaded as a CSV for analyse_4b.py.
"""

import json
import random
from datetime import date

claims = {c["id"]: c for c in json.load(open("claims.json"))}
pilot = json.load(open("4b-pilot-set.json"))
suggestions = json.load(open("4b-suggestions.json"))

rng = random.Random(4)
with_ids, without_ids = pilot["with_suggestion"][:], pilot["without_suggestion"][:]
rng.shuffle(with_ids)
rng.shuffle(without_ids)
order = []
for a, b in zip(with_ids, without_ids):
    pair = [(a, "with"), (b, "without")]
    rng.shuffle(pair)
    order += pair


def view(cid):
    c = claims[cid]
    policy_days = (date.fromisoformat(c["incident_date"])
                   - date.fromisoformat(c["policy_start_date"])).days
    checked_days = (date.fromisoformat(c["received_at"])
                    - date.fromisoformat(c["policy_status_checked_at"])).days
    related = [{"id": r["claim_id"], "relation": r["relation"],
                "description": claims[r["claim_id"]]["description"],
                "amount": claims[r["claim_id"]]["amount_gbp"]} for r in c["related_claims"]]
    return {**{k: v for k, v in c.items() if k != "related_claims"},
            "policy_days_before_incident": policy_days,
            "policy_checked_days_before_claim": checked_days,
            "related": related}


data = {
    "order": [{"id": cid, "condition": cond, "claim": view(cid),
               "ai": suggestions[cid] if cond == "with" else None} for cid, cond in order],
}

html = open("4b-pilot.template.html").read().replace("/*__DATA__*/null", json.dumps(data))
open("4b-pilot.html", "w").write(html)
print("4b-pilot.html:", len(order), "claims,", " ".join(f"{c}:{k[0]}" for c, k in order))
