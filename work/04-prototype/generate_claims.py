"""Generate the invented Stage 4a claim set.

Everything this script produces is invented. Fixed seed, so the set is reproducible.

Outputs:
  claims.json        80 claims, as the sorting step would see them. No labels.
  labels.csv         AI-set correct pile, category and a simulated handler pile per claim.
  history.json       400 invented older claims with piles, for the old-prototype stand-in.
  l1-audit-sheet.csv 20 claims for the human's blind re-label (label audit, L1).
  l1-audit-claims.md The same 20 claims in readable form.
"""

import csv
import json
import random
from datetime import date, timedelta

SEED = 4
rng = random.Random(SEED)

SIMPLE, CLOSER, SUSPICIOUS = "simple", "closer_look", "suspicious"
RECEIVED = date(2026, 10, 12)

FIRST = ["Amira", "Ben", "Chloe", "Dev", "Ellie", "Femi", "Grace", "Harun", "Isla", "Jonah",
         "Kiran", "Lena", "Marek", "Nadia", "Owen", "Priya", "Quinn", "Rosa", "Sami", "Tess"]
LAST = ["Achebe", "Barlow", "Costa", "Dunmore", "Ekwueme", "Fairley", "Gill", "Hollis", "Iqbal",
        "Jarvis", "Kowal", "Lindqvist", "Moyo", "Nairn", "Okafor", "Pryce", "Quayle", "Rahman"]
ROADS = ["Mill Road", "Station Street", "Chapel Lane", "Victoria Avenue", "Brook Way", "Kings Parade"]
LETTERS = "ABCDEFGHJKLMNPRSTVWXY"


def name():
    return f"{rng.choice(FIRST)} {rng.choice(LAST)}"


def reg():
    l = lambda n: "".join(rng.choice(LETTERS) for _ in range(n))
    return f"{l(2)}{rng.randint(10, 75)} {l(3)}"


def d(days_before):
    return (RECEIVED - timedelta(days=days_before)).isoformat()


counter = {"claim": 0, "claimant": 0, "incident": 0}


def next_id(kind, prefix, width):
    counter[kind] += 1
    return f"{prefix}{counter[kind]:0{width}d}"


def base(line, amount, description, docs, *, incident_days=3, policy_years=3, history=None,
         related=None, policy_number=True, checked_days=2, claimant=None, incident=None,
         status="active"):
    return {
        "id": None,  # assigned after shuffling
        "received_at": d(rng.randint(0, 2)),
        "line": line,
        "claimant_id": claimant or next_id("claimant", "P", 4),
        "incident_ref": incident or next_id("incident", "I", 4),
        "incident_date": d(incident_days),
        "policy_number": f"KW-{rng.randint(100000, 999999)}" if policy_number else None,
        "policy_start_date": d(int(policy_years * 365)),
        "policy_status": status,
        "policy_status_checked_at": d(checked_days),
        "amount_gbp": amount,
        "description": description,
        "documents": docs,
        "claimant_history": history or [],
        "related_claims": related or [],
    }


def docs(**kw):
    out = {"photos": True, "repair_estimate": True, "police_ref": None, "engineer_report": None}
    out.update(kw)
    return out


claims = []  # (claim, category, true_pile)


def add(claim, category, pile):
    claims.append([claim, category, pile])
    return claim


# --- Simple, clean (22) -------------------------------------------------------
for _ in range(10):
    amt = rng.randint(90, 290)
    add(base("glass", amt, f"Windscreen chipped by a stone on the motorway, now cracked across the "
             f"driver's side. Replacement quoted at £{amt}.", docs()), "simple_clean", SIMPLE)
for _ in range(7):
    amt = rng.randint(300, 1400)
    add(base("motor", amt, f"Reversed into a bollard in a supermarket car park. Rear bumper dented, "
             f"no other vehicle involved. Garage estimate £{amt}.", docs()), "simple_clean", SIMPLE)
for _ in range(5):
    amt = rng.randint(200, 900)
    add(base("home", amt, f"Washing machine hose split and leaked onto the kitchen floor. Vinyl "
             f"flooring needs replacing, quoted at £{amt}.", docs(repair_estimate=True)),
        "simple_clean", SIMPLE)

# --- Simple but higher value, everything in order (6) -------------------------
for _ in range(6):
    amt = rng.randint(3200, 6800)
    add(base("motor", amt, f"Hit a deep pothole on {rng.choice(ROADS)} at night, damaging both "
             f"nearside wheels and the suspension. Council has acknowledged the pothole. "
             f"Estimate £{amt}.", docs(engineer_report=True), policy_years=6),
        "simple_high_value", SIMPLE)

# --- Closer look: missing information (10) ------------------------------------
for i in range(10):
    amt = rng.randint(400, 2500)
    kind = i % 4
    if kind == 0:
        c = base("motor", amt, f"Another car pulled out of a side road and hit my front wing. The "
                 f"other driver gave their details. Estimate £{amt}.",
                 docs(police_ref=False), policy_number=True)
        c["description"] += " Third party involved; liability not yet confirmed by their insurer."
    elif kind == 1:
        c = base("motor", amt, f"Car scraped along a wall in a narrow lane. Estimate to follow.",
                 docs(repair_estimate=False))
    elif kind == 2:
        c = base("home", amt, f"Ceiling stain spreading from the bathroom above. Plumber found a "
                 f"leaking joint. Photos to follow.", docs(photos=False, repair_estimate=False))
    else:
        c = base("motor", amt, f"Car damaged while parked overnight on {rng.choice(ROADS)}. "
                 f"Estimate £{amt}.", docs(), policy_number=False)
    add(c, "missing_info", CLOSER)

# --- Closer look: claimant has claimed before (6) -----------------------------
for _ in range(6):
    amt = rng.randint(500, 2200)
    hist = [{"claim_id": f"H-{rng.randint(1000, 9999)}", "date": d(rng.randint(60, 300)),
             "line": "motor", "amount_gbp": rng.randint(400, 3000), "outcome": "paid"}]
    add(base("motor", amt, f"Rear-ended at traffic lights on {rng.choice(ROADS)}. Boot lid and "
             f"bumper damaged. Estimate £{amt}.", docs(police_ref=True), history=hist),
        "prior_claim", CLOSER)

# --- Closer look: linked claims from one incident (8, as 4 pairs) -------------
# Pairs 1-2: link is in the data (related_claims). Pairs 3-4: submitted separately,
# so the link is only visible by matching registration, road and date across claims.
for pair in range(4):
    vreg, road, days = reg(), rng.choice(ROADS), rng.randint(2, 6)
    inc_a = next_id("incident", "I", 4)
    inc_b = inc_a if pair < 2 else next_id("incident", "I", 4)
    driver, passenger = name(), name()
    a = base("motor", rng.randint(900, 2400), f"I was driving {vreg} when another car went into "
             f"the back of me on {road}. Bumper and tailgate damaged.", docs(police_ref=True),
             incident_days=days, incident=inc_a)
    b = base("motor", rng.randint(1500, 4200), f"I was a passenger in {vreg} on {road} when it was "
             f"hit from behind. Claiming for my damaged phone, laptop and physiotherapy.",
             docs(repair_estimate=False), incident_days=days, incident=inc_b)
    pile = CLOSER
    add(a, "linked_explicit" if pair < 2 else "linked_hidden", pile)
    add(b, "linked_explicit" if pair < 2 else "linked_hidden", pile)

# --- Closer look: duplicate submission (4, as 2 pairs) ------------------------
for _ in range(2):
    amt = rng.randint(250, 900)
    who, inc = next_id("claimant", "P", 4), next_id("incident", "I", 4)
    text = f"Side mirror knocked off by a passing van on {rng.choice(ROADS)}. Replacement £{amt}."
    a = base("motor", amt, text, docs(), claimant=who, incident=inc)
    b = base("motor", amt, text + " Submitting again as I had no confirmation.", docs(),
             claimant=who, incident=inc)
    add(a, "duplicate", CLOSER)
    add(b, "duplicate", CLOSER)

# --- Closer look: stale policy status (4) -------------------------------------
for _ in range(4):
    amt = rng.randint(300, 1200)
    add(base("motor", amt, f"Kerbed the car while parking, front alloy cracked. Estimate £{amt}.",
             docs(), checked_days=rng.randint(70, 140)), "stale_policy", CLOSER)

# --- Suspicious (12) ----------------------------------------------------------
for _ in range(3):  # policy started days before the incident
    amt = rng.randint(4500, 9000)
    add(base("motor", amt, f"Car stolen from outside my house overnight and found burnt out two "
             f"days later. Claiming the full value, £{amt}.", docs(police_ref=True, photos=False,
             repair_estimate=False), policy_years=12 / 365, incident_days=3), "new_policy",
        SUSPICIOUS)
for _ in range(3):  # many recent claims
    amt = rng.randint(1200, 3500)
    hist = [{"claim_id": f"H-{rng.randint(1000, 9999)}", "date": d(rng.randint(20, 330)),
             "line": rng.choice(["motor", "home"]), "amount_gbp": rng.randint(800, 4000),
             "outcome": "paid"} for _ in range(4)]
    add(base("home", amt, f"Laptop and camera stolen in a break-in. No sign of forced entry. "
             f"Claiming £{amt}.", docs(police_ref=True, repair_estimate=False), history=hist),
        "repeat_claimant", SUSPICIOUS)
# Staged pattern: three passengers in one car, all new claimants, one incident
vreg, road, inc = reg(), rng.choice(ROADS), next_id("incident", "I", 4)
for i in range(3):
    add(base("motor", rng.randint(2800, 4800), f"Passenger in {vreg} when it was hit on {road}. "
             f"Whiplash and lost earnings. Prefer payment in cash.", docs(photos=False,
             repair_estimate=False, police_ref=False), incident=inc, policy_years=0.2,
             related=[]), "staged_linked", SUSPICIOUS)
for _ in range(3):  # dates don't add up
    amt = rng.randint(1500, 4000)
    c = base("home", amt, f"Storm on the night of the 14th blew tiles off the roof and rain "
             f"damaged the loft. Claiming £{amt}.", docs(), incident_days=40)
    c["description"] += " Roofer's invoice is dated three weeks before the storm."
    add(c, "inconsistent_dates", SUSPICIOUS)

# --- Hard or ambiguous (8): AI-set pile, the cases the label audit matters most for
amt = rng.randint(150, 280)
add(base("glass", amt, f"Windscreen cracked by a stone. Replacement £{amt}.", docs(),
         history=[{"claim_id": "H-3101", "date": d(900), "line": "glass", "amount_gbp": 210,
                   "outcome": "paid"}]), "hard", SIMPLE)  # old prior claim, still simple
add(base("motor", 600, "Clipped a parked car's mirror while passing. Left a note with my details. "
         "Estimate £600.", docs(police_ref=None)), "hard", SIMPLE)
add(base("home", 4100, "Burst pipe in the loft during the cold snap flooded the upstairs "
         "bedroom. Plumber and builder quotes attached.", docs(engineer_report=False)),
    "hard", CLOSER)  # high value water damage, no engineer report
add(base("motor", 1800, "Car damaged in a hit-and-run while parked. Reported to the police.",
         docs(police_ref=True)), "hard", CLOSER)  # hit-and-run, unidentified third party
add(base("glass", 260, "Rear windscreen smashed. Not sure how it happened.", docs(),
         policy_years=0.1), "hard", CLOSER)  # new policy, vague cause, low value
inc = next_id("incident", "I", 4)
two = [base("motor", 1100, "Two of our cars collided on the driveway. Both insured with "
            "Keelwater. Estimate £1,100.", docs(), incident=inc),
       base("motor", 950, "Two of our cars collided on the driveway. Both insured with "
            "Keelwater. Estimate £950.", docs(), incident=inc)]
for c in two:
    add(c, "hard_linked_legit", SIMPLE)  # linked but genuinely simple
add(base("home", 700, "Dog chewed through the sofa. Claiming accidental damage cover.",
         docs(), checked_days=45), "hard", SIMPLE)

assert len(claims) == 80, len(claims)

rng.shuffle(claims)
for i, (c, _, _) in enumerate(claims, 1):
    c["id"] = f"K{i:03d}"

# Fill related_claims where the link is in the data
by_incident = {}
for c, cat, _ in claims:
    by_incident.setdefault(c["incident_ref"], []).append(c)
for c, cat, _ in claims:
    if cat in ("linked_explicit", "duplicate", "hard_linked_legit", "staged_linked"):
        c["related_claims"] = [{"claim_id": o["id"], "relation": "same incident",
                                "claimant_id": o["claimant_id"]}
                               for o in by_incident[c["incident_ref"]] if o is not c]


# Simulated historic handler pile: the "handler baseline" that A3a compares against.
# Invented error pattern: handlers miss links they can't see and occasionally slip.
def handler_pile(cat, true):
    if cat == "linked_hidden" and rng.random() < 0.6:
        return SIMPLE
    if cat in ("linked_explicit", "duplicate") and rng.random() < 0.25:
        return SIMPLE
    if cat == "stale_policy" and rng.random() < 0.5:
        return SIMPLE
    if cat == "simple_high_value" and rng.random() < 0.35:
        return CLOSER
    if rng.random() < 0.04:
        return rng.choice([p for p in (SIMPLE, CLOSER, SUSPICIOUS) if p != true])
    return true


with open("claims.json", "w") as f:
    json.dump([c for c, _, _ in claims], f, indent=1)

with open("labels.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "true_pile", "category", "handler_pile", "linked"])
    for c, cat, pile in claims:
        linked = cat.startswith("linked") or cat in ("duplicate", "staged_linked",
                                                      "hard_linked_legit")
        w.writerow([c["id"], pile, cat, handler_pile(cat, pile), int(linked)])

# Invented history for the old-prototype stand-in: line, amount band and documents only.
hist = []
for _ in range(400):
    line = rng.choice(["glass", "glass", "motor", "motor", "motor", "home"])
    amount = rng.randint(80, 9000) if line != "glass" else rng.randint(80, 400)
    missing = rng.random() < 0.2
    pile = SIMPLE
    if missing or amount > 3000:
        pile = CLOSER
    if amount > 4500 and rng.random() < 0.4:
        pile = SUSPICIOUS
    if rng.random() < 0.08:
        pile = rng.choice([SIMPLE, CLOSER, SUSPICIOUS])
    hist.append({"line": line, "amount_gbp": amount, "docs_missing": missing, "pile": pile})
with open("history.json", "w") as f:
    json.dump(hist, f, indent=0)

# Blind audit sample: 20 claims, spread across categories, no labels shown.
sample_rng = random.Random(SEED + 1)
by_cat = {}
for c, cat, _ in claims:
    by_cat.setdefault(cat, []).append(c)
sample = []
for cat in sorted(by_cat):
    sample.append(sample_rng.choice(by_cat[cat]))
rest = [c for c, _, _ in claims if c not in sample]
sample += sample_rng.sample(rest, 20 - len(sample))
sample.sort(key=lambda c: c["id"])

with open("l1-audit-sheet.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "your_pile (simple / closer_look / suspicious)", "why (optional)"])
    for c in sample:
        w.writerow([c["id"], "", ""])

with open("l1-audit-claims.md", "w") as f:
    f.write("# Label audit (L1): 20 claims to sort\n\n")
    f.write("**Invented claims.** Sort each into simple, closer_look or suspicious, as a senior "
            "handler would. Write your pile in `l1-audit-sheet.csv`. Don't open `labels.csv` "
            "until you're done.\n\n")
    f.write(f"Claims received on or just before {RECEIVED.isoformat()}.\n\n")
    for c in sample:
        f.write(f"## {c['id']} ({c['line']}, £{c['amount_gbp']:,})\n\n")
        f.write(f"{c['description']}\n\n")
        missing = [k for k, v in c["documents"].items() if v is False]
        f.write(f"- Incident {c['incident_date']}, received {c['received_at']}\n")
        f.write(f"- Policy: {c['policy_number'] or 'MISSING'}, started {c['policy_start_date']}, "
                f"{c['policy_status']} (checked {c['policy_status_checked_at']})\n")
        f.write(f"- Documents missing: {', '.join(missing) or 'none'}\n")
        hist_s = "; ".join(f"{h['date']} {h['line']} £{h['amount_gbp']:,} {h['outcome']}"
                           for h in c["claimant_history"]) or "none"
        f.write(f"- Claimant's earlier claims: {hist_s}\n")
        rel = ", ".join(r["claim_id"] for r in c["related_claims"]) or "none recorded"
        f.write(f"- Related claims: {rel}\n\n")

print(f"{len(claims)} claims, {len(sample)} in audit sample")
