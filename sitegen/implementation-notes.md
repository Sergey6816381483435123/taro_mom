# Implementation notes

- Confirmed contract: exactly 20 locales in the order in `sitegen/locales.json`.
- Confirmed product contract: four Premium readings with 7, 7, 10 and 12 cards.
- Five route keys are `home`, `daily-card`, `yes-no`, `three-card`, and `relationships`.
- Live bot catalog / PostgreSQL / n8n was not available from this repository; user-confirmed contract is used and no external system is changed.
- Baseline: branch `main`, commit `ae75039434661a01602de53483d33dbe48d13a81`; existing user edits in the master description and handoff file are preserved.
