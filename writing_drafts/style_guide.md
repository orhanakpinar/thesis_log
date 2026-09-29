# Thesis style guide

One page of fixed decisions so every chapter reads the same, whoever drafts it. Change anything
here freely. Changing it here is the only place it needs changing.

## Language and voice

- American English. Prose is English; Turkish source quotes stay in Turkish with an English gloss.
- First person singular for my own choices ("I construct...", "I exclude..."). Passive only when
  the actor genuinely doesn't matter.
- Past tense for what was done ("I normalized..."), present tense for what results show ("the
  estimate is...").
- No internal project history: no dates of decisions, no "corrected on...", no agent names. The
  thesis states the final position and why it is justified.

## Terms (use exactly these)

| Term | Use | Not |
|---|---|---|
| province | the unit of analysis (*il*) | city |
| non-metropolitan / old-metropolitan / new-metropolitan provinces | the three groups | treated/untreated as group names in prose |
| Law No. 6360 (Metropolitan Municipality Law) | first mention, then "Law 6360" | Metropol Law, Büyükşehir Law |
| Food Sovereignty Index (FSOI) | first mention, then FSOI | FSoI |
| **full index** | five categories, 14 indicators, 2008–2020; the descriptive index | Track C |
| **long-panel index** | four categories, 9 indicators, 2008–2024; the causal estimator | Track A |
| per household / per area | the two denominators; per household is the headline | perHousehold, perArea (code names) |
| municipal burden | category: water + waste | water category, waste category |
| external input | category: fertilizer + agricultural electricity | energy |
| Official Gazette (*Resmî Gazete*) | first mention, then Official Gazette | RG, Resmi Gazete |
| Ministry of Agriculture and Forestry | the ministry-news source | TOB, tarimorman |

Code-style variable names (`municipal_burden`, `FSOI_A`) appear only in the appendix or code
listings, never in running prose.

## Numbers and statistics

- Coefficients to 3 decimals, always with a 95% confidence interval: "−0.037 (95% CI −0.062 to
  −0.012)". p-values in parentheses when useful, never alone.
- Never write "not significant" as a conclusion. Interpret the interval: what size of effect it
  rules out.
- Never write "no effect" from a non-significant test. Write "no detectable effect" plus the
  interval.
- Percentages to 1 decimal; counts exact.
- Every number traces to a row in `claims_ledger.md`.

## Turkish terms

Italic with an English gloss at first use: *köy tüzel kişiliği* (village legal personality),
*mahalle* (neighborhood). After first use, italic only.

## Citations and format

- APA 7. Every reference verified against the actual source before citing. Nothing cited from
  memory or from an AI suggestion unchecked.
- Figures: numbered, with a caption that stands alone (what, where, when, unit, source). Short
  axis labels.
- Each results chapter ends with a short summary of what it found.
- Equations in LaTeX math. Figures exported from the notebooks, linked by relative path.

## Open (decide when relevant, not now)

- Final submission format (Koç template: Word or LaTeX?). Chapters are drafted in markdown either
  way.
