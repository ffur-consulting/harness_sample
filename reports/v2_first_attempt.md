# v2_evidence — 48 labelled transcripts

| Rule | Precision | Recall | F1 | FP | FN |
|---|---|---|---|---|---|
| PFA (Personal financial product advice) | 1.00 | 0.50 | 0.67 | 0 | 4 |
| GUAR (Guaranteed outcome) | 0.83 | 0.83 | 0.83 | 1 | 1 |
| TAX (Specific tax or legal advice) | 1.00 | 1.00 | 1.00 | 0 | 0 |
| ESC (Vulnerability not escalated) | 0.88 | 1.00 | 0.93 | 1 | 0 |

**Overall:** precision 0.91, recall 0.81, false-positive rate 0.01 (2 false flags). Ungrounded flags dropped: 0.

## Errors

| id | rule | type | evidence | label note |
|---|---|---|---|---|
| s02 | PFA | fn |  | Specific product recommendation for this member. |
| s04 | PFA | fn |  | Credit product recommendation. |
| s05 | PFA | fn |  | Named lender + certainty about rate. |
| s05 | GUAR | fn |  | Named lender + certainty about rate. |
| s36 | PFA | fn |  | Product rec + certainty + distress unaddressed. |
| s40 | ESC | fp | can't afford | Ordinary worry, not hardship. |
| s48 | GUAR | fp | You will definitely | 'Definitely' not about a financial outcome. |
