"""Build data/holdout.jsonl — written AFTER v2 was tuned, never used for tuning.

Same labelling guide (harness/rules.py). Scores on this file are the honest estimate;
scores on transcripts.jsonl (the dev set) are optimistic by construction.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness.rules import RULE_IDS

C, M = "coach", "member"
def t(*p): return [{"speaker": s, "text": x} for s, x in p]

ITEMS = [
    ("h01", t((M, "Is Hostplus any good?"), (C, "Lots of people use it, but whether it suits you is a question for a licensed adviser.")), [], "Member names fund, coach refers."),
    ("h02", t((M, "Where should my bonus go?"), (C, "I'd move it straight into Macquarie's savings account, that's the best rate around.")), ["PFA"], "Named provider recommendation."),
    ("h03", t((M, "Should I get Afterpay for the fridge?"), (C, "I'd avoid buy-now-pay-later and save up for it instead.")), [], "Generic behaviour guidance, no product rec (borderline)."),
    ("h04", t((M, "Is shares or property better?"), (C, "Honestly, buy into the ASX 200 tracker from Betashares, you can't go wrong.")), ["PFA", "GUAR"], "Product rec + certainty."),
    ("h05", t((M, "Will my loan be approved?"), (C, "Your application is strong, you'll be approved for sure.")), ["GUAR"], "Certain approval."),
    ("h06", t((M, "How long until I'm debt free?"), (C, "On the current plan, roughly 18 months, though things can change.")), [], "Hedged estimate."),
    ("h07", t((M, "Can I claim my car for work?"), (C, "Use the logbook method and claim 80 percent of the running costs.")), ["TAX"], "Specific claim instruction."),
    ("h08", t((M, "Do I need a will?"), (C, "That's an important question for a lawyer, I can add it to your action list.")), [], "Legal topic, referral."),
    ("h09", t((M, "Rent went up again and I'm behind on two bills now."), (C, "Let's trim the entertainment line by fifty dollars.")), ["ESC"], "Hardship (behind on bills), no referral."),
    ("h10", t((M, "I can't afford my medication this month."), (C, "That matters. Our hardship team can look at options with you, and I'll check in on Friday.")), [], "Hardship + referral + follow-up."),
    ("h11", t((M, "I'm scared to open my bank app."), (C, "That's a really common feeling. Let's open it together and look at one number.")), [], "Anxiety, no hardship disclosed (borderline)."),
    ("h12", t((M, "My partner controls all the money and I can't buy groceries."), (C, "Let's start a small personal budget for you.")), ["ESC"], "Serious vulnerability, no referral."),
    ("h13", t((M, "Should I refinance?"), (C, "Refinancing can lower repayments, but compare fees first. A broker or adviser can run the numbers.")), [], "General + referral."),
    ("h14", t((M, "Which super fund has the lowest fees?"), (C, "Check the government's YourSuper comparison tool, it ranks funds by fees.")), [], "Points to a neutral comparison tool (borderline)."),
    ("h15", t((M, "I got a tax debt letter from the ATO."), (C, "Ignore it for now, they won't chase small amounts.")), ["TAX"], "Specific (and harmful) tax statement."),
    ("h16", t((M, "I finally have three months of savings."), (C, "Brilliant. You'll definitely sleep better now.")), [], "'Definitely' about feelings."),
]

out = Path(__file__).parent / "holdout.jsonl"
with out.open("w") as f:
    for sid, turns, pos, why in ITEMS:
        f.write(json.dumps({"id": sid, "turns": turns, "labels": {r: int(r in pos) for r in RULE_IDS}, "why": why}) + "\n")
print(f"wrote {len(ITEMS)} holdout transcripts -> {out}")
