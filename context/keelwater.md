# Keelwater: context

The facts from the brief, and the working metric definitions. Anything in the first section is from the brief. Anything else is mine, and labelled.

## From the brief

### The company and the users

- Keelwater makes claims-handling software for insurance companies. Around 180 enterprise customers.
- A claim is a request to the insurer to pay, for example after a car is damaged.
- A handler looks at each new claim and puts it in one of three piles. This is sorting.
- Handlers spend most of their day in Keelwater. Any change to sorting changes their day, and how fast people get paid.

### The three piles

| Pile | Meaning |
|---|---|
| Simple | Pay it quickly. |
| Needs a closer look | Check the details first. |
| Suspicious | Send it for investigation. |

### The signal

- More customers have asked, over the last few months, for sorting to happen automatically. Several large customers have asked directly.
- Sales: six open deals mention it, worth £2.3M a year between them. One is the biggest deal in the pipeline. Sales says it is blocking deals.
- Customer Success: three important accounts have raised it in review meetings. One is a top-ten customer whose contract renews in five months.
- Support: around 40 tickets in the last six months mention sorting.
- Competition: a competitor launched automatic sorting last quarter.

### The product data

| Measure | Value | Period |
|---|---|---|
| Claims sorted | 2.1M | Last 12 months |
| Median time from claim arriving to being sorted | 11 minutes | Last 12 months |
| Claims taking more than four hours to be sorted | 15% | Last 12 months |
| Claims moved to a different pile within 30 days | 3.4% | Last 12 months |

The brief calls this data "mixed". The four-hour figure measures time to *sort*, not time to pay.

### Constraints and existing work

- **Explainability:** insurance companies must be able to explain every decision about a claim, to the customer and to their regulator.
- **Predictive prototype:** the data team built an early prototype that predicts which pile a claim belongs in. It was put on hold 18 months ago when the team moved to other work.
- **Bulk sorting:** the squad is halfway through building it. It lets a handler sort many claims at once, and is due to ship in six weeks.
- **Squad:** a designer, a tech lead and five engineers. I have just taken ownership of this area.

### What the task asks for

- The problem, and how confident I am.
- What I'd need to find out before committing the squad, and how to find it out quickly.
- Prioritisation: what first, what waits, what I wouldn't do, including the squad's current work.
- First signal to decision, then validation, delivery and measurement. Where AI changes the work, where it doesn't, and what stays my responsibility.
- How I'd decide something is safe and valuable enough to automate.
- What I'd tell Sales and Customer Success, and when.
- At the end of the recording, five minutes combined: how I used AI (including where I overrode it and one thing I rejected), and how the lifecycle is changing for AI-native teams.

### Rules from the brief

- Invent whatever data, quotes or organisational detail is needed, and flag it.
- No more than three hours. If I cut something, say what and why.
- Recording no more than 20 minutes, plus one or two pieces of working material.
- Panel: a product manager, an engineer, a designer and a member of the commercial team.

## Not in the brief

These are invented, or my own working definitions. Label them wherever they're used.

- **The 40 tickets, sales notes and CS notes** that Stage 1 codes. The brief gives counts, not the text. Any ticket text is invented.
- **The 80-claim synthetic set** (Stage 4a) and **the 60-claim time sample** (Stage 3). Invented.
- **Thresholds** in the assumptions register. Set by me at the Stage 3 gate.

### Metric definitions (working, mine)

| Metric | Working definition |
|---|---|
| Time to correct payment | From the claim arriving to the claim being paid on its final pile. Not measured in the brief, which only gives time to sort. |
| Handler minutes | Handler time spent on a claim's sorting decision. |
| Wrong-pay rate | Share of claims paid that should not have been, or paid on the wrong pile. Always reported separately for linked claims. |
| Reversal rate | Share of sorting decisions changed after the fact. The brief's 3.4% moved within 30 days is the baseline proxy. |
| Override rate | Share of automated suggestions a handler changes. |
| Compliance acceptance of reason codes | Share of sampled reason codes that compliance accepts as a sufficient explanation to a customer or regulator. |
