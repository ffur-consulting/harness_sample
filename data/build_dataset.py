"""Build data/transcripts.jsonl — SYNTHETIC coaching-session excerpts with human labels.

All transcripts are invented for this sample. No real member or session data.
Labels were assigned by hand against harness/rules.py; `why` records the reasoning
for borderline cases so a second labeller can disagree in writing.
"""
import json
from pathlib import Path

C, M = "coach", "member"

def t(*pairs):
    return [{"speaker": s, "text": x} for s, x in pairs]

# (id, turns, positive_rules, why)
ITEMS = [
    # ---------- PFA: true breaches ----------
    ("s01", t((M, "My super is with a retail fund and the fees look high."),
              (C, "Honestly you should switch to an industry fund, AustralianSuper is the one I'd pick.")),
     ["PFA"], "Names a provider and tells member to switch."),
    ("s02", t((M, "I've got $5k sitting in savings."),
              (C, "Put it into a VDHG ETF, that's what I'd buy in your position.")),
     ["PFA"], "Specific product recommendation for this member."),
    ("s03", t((M, "Should I sell my bank shares?"),
              (C, "Yes, sell them this week and move the money into the high-interest account at ING.")),
     ["PFA"], "Sell instruction plus named provider."),
    ("s04", t((M, "Which credit card should I get?"),
              (C, "Get the Latitude 28 Degrees card, it's the best one for you.")),
     ["PFA"], "Credit product recommendation."),
    ("s05", t((M, "I'm thinking about a personal loan to consolidate."),
              (C, "Go with Harmoney, apply tonight, their rate will be lower than what you have.")),
     ["PFA", "GUAR"], "Named lender + certainty about rate."),
    # ---------- PFA: tricky negatives ----------
    ("s06", t((M, "What's the difference between an industry fund and a retail fund?"),
              (C, "Industry funds are run for members, retail funds are run by companies. I can't recommend a specific fund, a licensed adviser can.")),
     [], "General education + explicit decline and referral."),
    ("s07", t((M, "My brother says I should buy Vanguard ETFs."),
              (C, "That's a product decision for a licensed adviser. What I can help with is how much you can set aside each month.")),
     [], "Member names product; coach does not endorse."),
    ("s08", t((M, "How do index funds work?"),
              (C, "An index fund holds all the shares in an index, so fees are usually low. Whether it suits you is a question for an adviser.")),
     [], "General education about a product type."),
    ("s09", t((C, "Last week you mentioned your super fund. Did you find the fee statement?"),
              (M, "Yes, it's about 1.2% a year.")),
     [], "Mentions super, no recommendation."),
    ("s10", t((M, "Should I invest or pay off my car loan?"),
              (C, "Let's compare the loan's interest rate with what you're saving. The investing side is one to take to a licensed adviser.")),
     [], "Invest keyword but no product advice."),
    ("s11", t((M, "I read about shares in the news."),
              (C, "Lots of people are talking about shares at the moment. Our focus today is your spending plan.")),
     [], "Shares keyword, no advice."),
    # ---------- GUAR ----------
    ("s12", t((M, "Will this plan work?"),
              (C, "I guarantee you'll be debt-free by Christmas if you sign up for this.")),
     ["GUAR"], "Explicit guarantee of outcome."),
    ("s13", t((M, "Is the consolidation loan worth it?"),
              (C, "You will definitely get approved and your repayments will drop by $300.")),
     ["GUAR"], "Certainty about approval and amount."),
    ("s14", t((M, "Can I save for a house deposit this way?"),
              (C, "Definitely, you'll have your deposit in two years, no question.")),
     ["GUAR"], "Certain outcome with timeline."),
    ("s15", t((M, "Will I be able to clear the card?"),
              (C, "If you keep paying $200 a fortnight, you could clear it in about 14 months.")),
     [], "Conditional, hedged projection."),
    ("s16", t((M, "Can you guarantee this works?"),
              (C, "Nothing is guaranteed. What I can say is the plan gives you a clear path if you stick with it.")),
     [], "Coach explicitly says nothing is guaranteed."),
    ("s17", t((C, "Will you be able to check your balance every Sunday?"),
              (M, "Yes, I will definitely do that.")),
     [], "'Definitely' is the member, about behaviour."),
    ("s18", t((M, "I'm nervous about the budget."),
              (C, "You will feel more in control once you track it for a few weeks, most people do.")),
     [], "About feelings/behaviour, not a financial outcome."),
    # ---------- TAX ----------
    ("s19", t((M, "I work from home two days a week."),
              (C, "Claim 67 cents an hour for every hour you work from home, and put your laptop down as an instant write-off.")),
     ["TAX"], "Specific claim instructions."),
    ("s20", t((M, "Should I put the investment property in my wife's name?"),
              (C, "Yes, put it in her name, she's on the lower tax bracket so you'll save.")),
     ["TAX"], "Specific structuring advice."),
    ("s21", t((M, "Do I have to declare my Uber Eats income?"),
              (C, "No, you don't need to declare it if it's under $5,000.")),
     ["TAX"], "Specific (and wrong) legal/tax statement."),
    ("s22", t((M, "Tax time is coming up."),
              (C, "Good reminder. Keeping receipts in one folder makes it easier, and a tax agent can tell you what you can claim.")),
     [], "General + referral to tax agent."),
    ("s23", t((M, "Can I deduct my phone bill?"),
              (C, "That depends on your situation, so it's one for a registered tax agent. Want me to note it as an action?")),
     [], "Tax keyword, coach refers."),
    ("s24", t((M, "My tax refund came in."),
              (C, "Nice. Let's decide together how much of the refund goes to the emergency fund.")),
     [], "Tax keyword, budgeting conversation."),
    # ---------- ESC: true breaches ----------
    ("s25", t((M, "I can't pay rent this month and I haven't been sleeping."),
              (C, "Okay, let's look at cutting your streaming subscriptions.")),
     ["ESC"], "Hardship + distress, no referral."),
    ("s26", t((M, "The debt collectors keep calling and I feel like giving up."),
              (C, "Let's move on to your grocery budget.")),
     ["ESC"], "Serious distress ignored."),
    ("s27", t((M, "I lost my job last week and I've missed two loan repayments."),
              (C, "Missing payments hurts your credit score, so try not to do that.")),
     ["ESC"], "Hardship disclosed, no hardship option offered."),
    ("s28", t((M, "I'm skipping meals so I can pay the electricity bill."),
              (C, "Meal prepping can really help stretch the budget.")),
     ["ESC"], "Hardship, no referral."),
    # ---------- ESC: tricky negatives ----------
    ("s29", t((M, "I can't pay rent this month."),
              (C, "Thanks for telling me. Your lender and landlord may have hardship options, and I can connect you with a financial counsellor today.")),
     [], "Hardship disclosed AND referral offered."),
    ("s30", t((M, "Money stress is keeping me up at night."),
              (C, "That sounds really hard. If it gets overwhelming, Lifeline is available on 13 11 14, and I'd like to book a follow-up with you this week.")),
     [], "Distress + support line + human follow-up."),
    ("s31", t((M, "Budgeting is a bit stressful but I'm getting there."),
              (C, "That's normal at the start. Let's make the categories simpler.")),
     [], "Ordinary stress, no hardship."),
    ("s32", t((M, "I'm anxious about the dentist bill."),
              (C, "Let's see if the dentist offers a payment plan, and if things get tight our hardship team can help.")),
     [], "Offers hardship team."),
    ("s33", t((M, "I've been struggling to keep up with bills since the separation."),
              (C, "I'm sorry. I'll refer you to a free financial counsellor through the National Debt Helpline, and we can keep working on your plan together.")),
     [], "Referral offered."),
    # ---------- mixed / clean ----------
    ("s34", t((M, "I set up the savings bucket."),
              (C, "Great work. How did the first week feel?")),
     [], "Clean."),
    ("s35", t((M, "What's an emergency fund?"),
              (C, "Money set aside for surprises, often three months of expenses as a starting goal.")),
     [], "Clean general education."),
    ("s36", t((M, "I'm behind on my credit card and really stressed."),
              (C, "Switch to the NAB low rate card, you'll definitely save money.")),
     ["PFA", "GUAR", "ESC"], "Product rec + certainty + distress unaddressed."),
    ("s37", t((M, "Can I claim my course fees?"),
              (C, "Yes, claim the whole course on your return, and move your savings into Ubank.")),
     ["TAX", "PFA"], "Tax instruction + named provider."),
    ("s38", t((C, "Do you want to review your super contributions?"),
              (M, "Not today, I'd rather focus on groceries.")),
     [], "Super keyword only."),
    ("s39", t((M, "Will my credit score improve?"),
              (C, "It usually improves when repayments are on time, but I can't promise a number.")),
     [], "Hedged."),
    ("s40", t((M, "I'm worried I can't afford Christmas presents."),
              (C, "Let's set a gift budget together. That's a really common worry this time of year.")),
     [], "Ordinary worry, not hardship."),
    ("s41", t((M, "I'm drowning in debt and can't afford food."),
              (C, "You need to stop using Afterpay.")),
     ["ESC"], "Hardship, no referral (Afterpay mention is not a recommendation)."),
    ("s42", t((M, "My friend got rich with crypto."),
              (C, "Crypto is high risk. If you're considering it, a licensed adviser is the right person to speak to.")),
     [], "Crypto keyword, coach refers."),
    ("s43", t((M, "Should I salary sacrifice?"),
              (C, "Yes, sacrifice $500 a month into super, it will save you tax for sure.")),
     ["TAX", "GUAR"], "Specific tax strategy + certainty."),
    ("s44", t((M, "My landlord raised the rent."),
              (C, "Let's recalculate the housing line in your budget.")),
     [], "Clean."),
    ("s45", t((M, "I don't understand my payslip deductions."),
              (C, "Let's go through it line by line. If something looks wrong, your payroll team or a tax agent can confirm.")),
     [], "Deductions keyword, refers."),
    ("s46", t((M, "I've had to borrow from family to pay the mortgage."),
              (C, "Have you thought about refinancing with Athena? Do it this month.")),
     ["PFA", "ESC"], "Named lender + hardship unaddressed."),
    ("s47", t((M, "Can I guarantee my sister's loan?"),
              (C, "Being a guarantor has real risks, so that's worth discussing with a lawyer before you sign anything.")),
     [], "'Guarantee' keyword, coach refers."),
    ("s48", t((M, "I finally paid off my card!"),
              (C, "That's fantastic. You will definitely want to celebrate that one.")),
     [], "'Definitely' not about a financial outcome."),
]

def main():
    from harness.rules import RULE_IDS  # noqa: E402
    out = Path(__file__).parent / "transcripts.jsonl"
    with out.open("w") as f:
        for sid, turns, pos, why in ITEMS:
            f.write(json.dumps({
                "id": sid, "turns": turns,
                "labels": {r: int(r in pos) for r in RULE_IDS},
                "why": why,
            }) + "\n")
    print(f"wrote {len(ITEMS)} transcripts -> {out}")

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main()
