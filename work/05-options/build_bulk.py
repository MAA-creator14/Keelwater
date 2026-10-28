"""Build the Stage 5 bulk-sorting pilot (bulk-pilot.html).

Invented claims. The batch is filter B (complete documents, policy number present, no claims
in the last 12 months, no related claims recorded, policy over 60 days old, under £1,000):
9 claims from the 80 the human hasn't seen, plus 4 new invented claims that pass the filter but
need a closer look under the human's sorting policy. Their ids and answers are kept in
bulk-planted.json, not in the page.
"""

import json
import random
from datetime import date, timedelta

RECEIVED = date(2026, 10, 12)
d = lambda n: (RECEIVED - timedelta(days=n)).isoformat()

claims = {c["id"]: c for c in json.load(open("../04-prototype/claims.json"))}
unseen_in_b = ["K039", "K041", "K045", "K046", "K053", "K062", "K064", "K072", "K080"]

docs = {"photos": True, "repair_estimate": True, "police_ref": None, "engineer_report": None}


def new(cid, line, amount, text, claimant, incident, police=None, incident_days=3):
    return {"id": cid, "received_at": d(1), "line": line, "claimant_id": claimant,
            "incident_ref": incident, "incident_date": d(incident_days),
            "policy_number": f"KW-{abs(hash(cid)) % 900000 + 100000}",
            "policy_start_date": d(1095), "policy_status": "active",
            "policy_status_checked_at": d(2), "amount_gbp": amount, "description": text,
            "documents": {**docs, "police_ref": police}, "claimant_history": [],
            "related_claims": []}


planted = [
    new("N01", "glass", 240, "Windscreen chipped by a stone on the motorway, now cracked across "
        "the driver's side. Replacement quoted at £240. Sending this again as I haven't heard "
        "back.", "P0091", "I0101"),
    new("N02", "motor", 640, "Reversed into a neighbour's garden wall and cracked two bricks. Left "
        "a note with my details. Builder's quote £640.", "P0092", "I0102"),
    new("N03", "motor", 870, "Rear-ended at traffic lights on Station Street by a van, LM19 KTR. "
        "Boot lid and bumper damaged. Estimate £870.", "P0093", "I0103", police=True),
    new("N04", "motor", 910, "My van LM19 KTR went into the back of a car at the traffic lights on "
        "Station Street. Front bumper and grille damaged. Estimate £910.", "P0094", "I0104",
        police=True),
]
answers = {"N01": "closer_look (P01: same claim submitted again)",
           "N02": "closer_look (P15: damage to a third party's property, no contact yet)",
           "N03": "closer_look (P08: linked to N04, same incident)",
           "N04": "closer_look (P08: linked to N03, same incident)"}
batch = [claims[i] for i in unseen_in_b] + planted
random.Random(61).shuffle(batch)
# Batch-local ids, so the new claims can't be told apart by their id
label = {c["id"]: f"B{n:02d}" for n, c in enumerate(batch, 1)}
json.dump({"batch_ids": label, "planted_answers": {label[k]: f"{k}: {v}" for k, v in answers.items()}},
          open("bulk-planted.json", "w"), indent=1)


def row(c):
    age = (date.fromisoformat(c["incident_date"]) - date.fromisoformat(c["policy_start_date"])).days
    return {"id": label[c["id"]], "line": c["line"], "amount": c["amount_gbp"],
            "description": c["description"], "incident": c["incident_date"],
            "received": c["received_at"], "policy_years": round(age / 365, 1)}


style = open("../04-prototype/4b-pilot.template.html").read().split("<style>")[1].split("</style>")[0]
html = open("bulk-pilot.template.html").read()
html = html.replace("/*__STYLE__*/", style).replace("/*__DATA__*/null",
                                                    json.dumps([row(c) for c in batch]))
open("bulk-pilot.html", "w").write(html)
print(len(batch), "claims in the batch")
