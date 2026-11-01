# Compliance-classifier evaluation harness (sample)

A small, dependency-free harness for answering one question honestly: **did a change to a
compliance classifier reduce false flags without missing real breaches?**

Built as a work sample for a financial-coaching QA use case. **All transcripts are synthetic**
— invented for this repo, no real member or session data.

## What it does

1. **Labelled data** — 48 dev transcripts (`data/transcripts.jsonl`) and 16 held-out
   transcripts (`data/holdout.jsonl`), each labelled against four rules in
   [`harness/rules.py`](harness/rules.py):

   | Rule | Breach |
   |---|---|
   | PFA | Coach recommends a specific financial product or provider |
   | GUAR | Coach promises a financial outcome as certain |
   | TAX | Coach gives specific tax/legal advice |
   | ESC | Member discloses hardship/distress and coach doesn't refer or follow up |

   Every rule has an explicit **"not a breach"** list. That is where over-flagging comes from
   (topic words like *super*, *tax*, *definitely* that aren't breaches).

2. **Evidence or it didn't happen** — a flag only counts if its evidence is a **verbatim span
   of the transcript**. Ungrounded flags (e.g. an LLM paraphrasing or inventing a quote) are
   dropped and counted.

3. **Per-rule precision / recall / F1**, overall false-positive rate, and an error table with
   the evidence and the labeller's note for every miss — so you can see *why*, not just *how many*.

4. **Release gate** — `harness.compare` exits non-zero if the candidate loses recall on
   **any** rule. Cutting false positives only counts if real breaches are still caught.

## Results

| Classifier | Split | Precision | Recall | False flags |
|---|---|---|---|---|
| v1 keyword baseline | dev (48) | 0.38 | 0.81 | 34 |
| v2 evidence rules | dev (48) | 1.00 | 1.00 | 0 |
| v1 keyword baseline | **holdout (16)** | 0.36 | 0.50 | 7 |
| v2 evidence rules | **holdout (16)** | 1.00 | **0.38** | 0 |

What this shows:

- On the dev set, v2 removes all 34 false flags. **But v2 was tuned on that set**, so those
  numbers are optimistic by construction. The first v2 attempt even failed the gate on dev
  (it lost recall on PFA and GUAR) — see `reports/v2_first_attempt_gate.txt`.
- On the **held-out set, written after tuning**, v2 still removes every false flag (7 → 0) but
  misses 5 of 8 real breaches, and the gate **fails** on TAX. Hand-written rules don't
  generalise to new phrasing ("I'd move it straight into Macquarie's…", "my partner controls
  all the money").
- That is the case for an LLM classifier — and for scoring it on this harness before it ships.

## Running it

```bash
python data/build_dataset.py && python data/build_holdout.py
python -m harness.evaluate --classifier v1_keyword  --split holdout
python -m harness.evaluate --classifier v2_evidence --split holdout
python -m harness.compare reports/v1_keyword_holdout.json reports/v2_evidence_holdout.json
python -m pytest -q
```

### LLM classifier (optional)

`ClaudeClassifier` in `harness/classifiers.py` uses the Anthropic Messages API with:

- **tool use** to force structured output (`{flags: [{rule, evidence}]}`),
- **prompt caching** on the long, stable rule text,
- the same grounding check — a quote that isn't in the transcript is dropped.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...        # never commit keys
python -m harness.evaluate --classifier llm_claude --split holdout
```

## How labels were created

One labeller (me) applied `harness/rules.py` to each transcript and wrote a one-line `why`
for every item, especially borderline ones (e.g. `h03`, `h11`, `h14`). In production I'd add:
a second labeller on a sample, agreement measured per rule, disagreements resolved by the
compliance owner, and the rule text updated when a disagreement reveals ambiguity.

## Limits

Small synthetic dataset; one labeller; borderline items are judgement calls. The point is the
method — grounded flags, per-rule metrics, a held-out split and a recall gate — not the numbers.
