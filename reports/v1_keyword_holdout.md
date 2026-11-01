# v1_keyword_holdout — 16 labelled transcripts

| Rule | Precision | Recall | F1 | FP | FN |
|---|---|---|---|---|---|
| PFA (Personal financial product advice) | 0.33 | 0.50 | 0.40 | 2 | 1 |
| GUAR (Guaranteed outcome) | 0.33 | 0.50 | 0.40 | 2 | 1 |
| TAX (Specific tax or legal advice) | 1.00 | 1.00 | 1.00 | 0 | 0 |
| ESC (Vulnerability not escalated) | 0.00 | 0.00 | 0.00 | 3 | 2 |

**Overall:** precision 0.36, recall 0.50, false-positive rate 0.12 (7 false flags). Ungrounded flags dropped: 0.

## Errors

| id | rule | type | evidence | label note |
|---|---|---|---|---|
| h02 | PFA | fn |  | Named provider recommendation. |
| h04 | GUAR | fn |  | Product rec + certainty. |
| h05 | PFA | fp | loan | Certain approval. |
| h06 | ESC | fp | debt | Hedged estimate. |
| h08 | GUAR | fp | will | Legal topic, referral. |
| h09 | ESC | fn |  | Hardship (behind on bills), no referral. |
| h10 | ESC | fp | can't afford | Hardship + referral + follow-up. |
| h12 | ESC | fn |  | Serious vulnerability, no referral. |
| h14 | PFA | fp | super | Points to a neutral comparison tool (borderline). |
| h15 | ESC | fp | debt | Specific (and harmful) tax statement. |
| h16 | GUAR | fp | definitely | 'Definitely' about feelings. |
