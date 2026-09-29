# Agent note: writing_drafts/ status (AI-authored)

Working note for `thesis_log_writingdrafts_agent` sessions. Status and next steps only; no
thesis content lives here. `CLAUDE.md` governs anything about result validity.

## How Orhan and this agent work

- Orhan takes an executive role: he briefs each chapter, the agent drafts from
  `claims_ledger.md`, and Orhan reviews for reasoning and rewrites in his voice.
- Orhan writes the argumentative parts himself: causal results chapter, legibility argument,
  discussion. The agent provides scaffolds and jury-style review there, not prose.
- Every interpretive move in an agent draft is marked `[INT]` for Orhan to accept, rewrite or
  reject.
- The agent acts as a mentor: push back on reasoning errors (e.g. reading a non-significant
  result as "no effect"), and keep him out of decision fatigue by proposing defaults he can
  change later.

## Files

| File | Role |
|---|---|
| `claims_ledger.md` | Source of truth for every claim, number, location, scope limit |
| `style_guide.md` | Fixed conventions (terms, numbers, citations) |
| `advisor_comments.md` | Ali Hoca's seven Jan-2025 comments, verbatim, with a status column |
| `scripts/attrition_table.py` | Computes the 184 → 88 → 24 indicator attrition table |
| `thesis_draft.md` | Orhan's original outline; to become the table of contents |
| `chapters/` | Not created yet |

`TezRapor/` was removed 2026-09-26 at Orhan's request (sent to the Recycle Bin; also in git
history).

## Plan

Ledger → measurement chapter → causal results (Orhan writes) → discourse → Law 6360 context →
literature review → discussion → introduction.

## Chapter progress

- `chapters/04_measurement.md`: §4.1.1–4.1.4 drafted (agent draft v1). Open `[VERIFY]` in
  §4.1.4: why health personnel, machinery, migration and organic production (on
  `turkstat_indicators_final_list.xlsx`) were not kept; why fertilizer came from the ministry. Orhan rewrites after the
  whole chapter is drafted. The Scopus search (1,502 / 1,170, 13 June 2024) was moved out of
  §4.1.2; it belongs in Chapter 2's search-method paragraph.
- `scripts/attrition_table.py` also computes the bloc table (Table 4.1). Bloc grouping is
  provisional, for Orhan to confirm.

## Next steps

1. Orhan reviews the ledger and ticks what he can defend.
2. Resolve the "verify/reconcile" items the agent can do (legal sources, locating code).
3. Orhan's brief for the measurement chapter; then the agent drafts it.
4. Ministry-news human validation (Orhan) before the discourse chapter.

## Finding to carry forward

The attrition table (`scripts/attrition_table.py`) shows several relational categories had a
matched source file yet were dropped (Land Security 5/6, Cooperative 5/6, Food Sovereignty 4/4).
So "the state doesn't publish control variables" may not be the whole reason. Elimination
reasons must be recorded (ledger B4) before the measurement chapter argues it.
