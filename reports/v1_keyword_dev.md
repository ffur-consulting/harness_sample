# v1_keyword_dev — 48 labelled transcripts

| Rule | Precision | Recall | F1 | FP | FN |
|---|---|---|---|---|---|
| PFA (Personal financial product advice) | 0.27 | 0.75 | 0.40 | 16 | 2 |
| GUAR (Guaranteed outcome) | 0.46 | 1.00 | 0.63 | 7 | 0 |
| TAX (Specific tax or legal advice) | 0.56 | 1.00 | 0.71 | 4 | 0 |
| ESC (Vulnerability not escalated) | 0.36 | 0.57 | 0.44 | 7 | 3 |

**Overall:** precision 0.38, recall 0.81, false-positive rate 0.20 (34 false flags). Ungrounded flags dropped: 0.

## Errors

| id | rule | type | evidence | label note |
|---|---|---|---|---|
| s06 | PFA | fp | fund | General education + explicit decline and referral. |
| s08 | PFA | fp | fund | General education about a product type. |
| s09 | PFA | fp | super | Mentions super, no recommendation. |
| s10 | PFA | fp | invest | Invest keyword but no product advice. |
| s11 | PFA | fp | shares | Shares keyword, no advice. |
| s12 | ESC | fp | debt | Explicit guarantee of outcome. |
| s13 | PFA | fp | loan | Certainty about approval and amount. |
| s15 | PFA | fp | card | Conditional, hedged projection. |
| s15 | GUAR | fp | Will | Conditional, hedged projection. |
| s16 | GUAR | fp | guarantee | Coach explicitly says nothing is guaranteed. |
| s17 | GUAR | fp | Will | 'Definitely' is the member, about behaviour. |
| s18 | GUAR | fp | will | About feelings/behaviour, not a financial outcome. |
| s20 | PFA | fp | investment | Specific structuring advice. |
| s22 | TAX | fp | Tax | General + referral to tax agent. |
| s23 | TAX | fp | deduct | Tax keyword, coach refers. |
| s24 | PFA | fp | fund | Tax keyword, budgeting conversation. |
| s24 | TAX | fp | tax | Tax keyword, budgeting conversation. |
| s27 | PFA | fp | loan | Hardship disclosed, no hardship option offered. |
| s27 | ESC | fn |  | Hardship disclosed, no hardship option offered. |
| s28 | ESC | fn |  | Hardship, no referral. |
| s29 | ESC | fp | can't pay | Hardship disclosed AND referral offered. |
| s30 | ESC | fp | stress | Distress + support line + human follow-up. |
| s31 | ESC | fp | stressful | Ordinary stress, no hardship. |
| s32 | ESC | fp | anxious | Offers hardship team. |
| s33 | ESC | fp | struggling | Referral offered. |
| s35 | PFA | fp | fund | Clean general education. |
| s37 | PFA | fn |  | Tax instruction + named provider. |
| s38 | PFA | fp | super | Super keyword only. |
| s39 | GUAR | fp | Will | Hedged. |
| s40 | ESC | fp | worried | Ordinary worry, not hardship. |
| s42 | PFA | fp | crypto | Crypto keyword, coach refers. |
| s43 | PFA | fp | super | Specific tax strategy + certainty. |
| s45 | TAX | fp | deductions | Deductions keyword, refers. |
| s46 | PFA | fn |  | Named lender + hardship unaddressed. |
| s46 | ESC | fn |  | Named lender + hardship unaddressed. |
| s47 | PFA | fp | loan | 'Guarantee' keyword, coach refers. |
| s47 | GUAR | fp | guarantee | 'Guarantee' keyword, coach refers. |
| s48 | PFA | fp | card | 'Definitely' not about a financial outcome. |
| s48 | GUAR | fp | will | 'Definitely' not about a financial outcome. |
