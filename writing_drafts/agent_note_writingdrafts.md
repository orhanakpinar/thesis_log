# Agent note: writing_drafts/ status (AI-authored)

> **Main rule (Orhan's gold rule), for every paragraph, every chapter:**
> **Do I agree? Can I defend it? Is that all there is to say?**

Working note for `thesis_log_writingdrafts_agent` sessions. Status and next steps only; no
thesis content lives here. `CLAUDE.md` governs anything about result validity.

**Writing rule (Orhan, 2026-10-02):** chapter drafts stay clean and focused. Process history,
data-problem explanations and side material go here (agent note) or into an appendix file, not
into chapter prose.

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

## Resolved 2026-10-05

Orhan's decisions: fertilizer per household with zeros kept (Hakkari discussed as a case);
log1p kept with approved wording; no larger bootstrap. Index unchanged. Ch. 4 skew text updated
(3.07 → 1.87, 14 of 26); Ch. 6 land-use breakdown added; **Ch. 5 rewritten as v2 on the rebuilt
13-indicator index** (HOLD lifted). Appendix B drafted with tables B.1/B.2.

**Appendix map (thesis letter → econometrics file):** Appendix A = 184-indicator table
(`writing_drafts/tables/indicator_attrition_draft.xlsx`); Appendix B = animal products
(`thesis_outputs/table_B1…`, `table_B2…`); **Appendix C, Table C.1 = skew by indicator, from
`thesis_outputs/table_B3_skew_by_indicator.csv`** (file name says B3; thesis calls it C.1 because
Appendix B is about animal products). Data appendix = `table_data_appendix_indicators.csv`. **Figure map:** thesis Figure 6.3 =
`thesis_outputs/fig_6_1b_event_study_full_index.png` (full-index DiD robustness).
**Sources for numbers (from 2026-10-05):** `econometric_models_and_vars/agent_note_econometrics_FSOI.md`
(rewritten as one verified current-state document) plus `CLAUDE.md`. Check new numbers there
first.
**Fade window rule (Orhan, 2026-10-07):** fades are always 2014–18 vs 2020–24; never drop 2020;
the 2022–24 window is retired. Log waste −3%, municipal-burden score −27%, composite −14%.
**Old export names deleted 2026-10-07:** only `fsoi_full_index_perHousehold.csv` and
`fsoi_long_panel_index_perHousehold.csv` exist now.
**Attribution rule (Orhan, 2026-10-05):** cite the Law 6360 critique as ZMO (Ziraat Mühendisleri
Odası, a TMMOB member chamber), never "TMMOB".

## (History) Open as of 2026-10-01: animal products dropped

Orhan dropped the animal-product value indicator (data break) and moved it to Appendix B. Ch. 4
text updated to 13 indicators. **The econometrics notebook must rebuild the full index without it
and re-export `fsoi_full_index_perHousehold.csv` (formerly `fsoi_track_C_perHousehold.csv`), Figures 5.1/5.2, the TOPSIS and rank-convergence
checks, and an Appendix B comparison (with vs. without).** Then rerun
`scripts/descriptive_tables.py` (its asserts on 0.500/0.433/0.424 and 0.744 will fail and must be
updated) and rewrite Ch. 5. Rebuild request sent to the main agent 2026-10-02 (five items:
rebuild + export, re-run descriptive checks, re-export Figs 5.1/5.2, Appendix B with/without
comparison, recompute skew figures for 26 columns).

**When rewriting Ch. 5 (after Hakkari/log1p decisions):** use the C1 wording in the ledger
("lowest in every 2020 and long-panel view; old-metro marginally lowest in the 2008–2020 full-index
average, by 0.004 EW / 0.010 flat"); move the animal-product decline story to Appendix B (file
exists, tables B.1/B.2 filled); add the Hakkari point (low input use ≠ sovereignty where there is
little agriculture). Check that the "two routes to the bottom" still holds with rebuilt numbers
(it does in the 2026-10-02 rerun).

## Chapter progress

- `chapters/04_measurement.md`: **complete draft v1** (~5,400 words, 4.1–4.3, Tables 4.1–4.4,
  Figure 4.2 as mermaid; Figures 4.1 and 4.3 pending). 9 `[VERIFY]` open. §4.3.2 was drafted by
  the agent at Orhan's request (2026-10-01), from his own stated position; he will rewrite it.
  Orhan's plan: agent drafts the whole thesis chapter by chapter, self-checking each; Orhan
  rewrites everything afterwards.
  Recommendation given to Orhan on B24: keep municipal burden inside the index (it predates the
  DiD; removing it post hoc is a forking-paths risk) and make the decomposition Chapter 6's
  headline. His decision, to take to Ali Hoca. Open `[VERIFY]` in
  §4.1.4: why health personnel, machinery, migration and organic production (on
  `turkstat_indicators_final_list.xlsx`) were not kept; why fertilizer came from the ministry. Orhan rewrites after the
  whole chapter is drafted. The Scopus search (1,502 / 1,170, 13 June 2024) was moved out of
  §4.1.2; it belongs in Chapter 2's search-method paragraph.
- `scripts/attrition_table.py` also computes the bloc table (Table 4.1). Bloc grouping is
  provisional, for Orhan to confirm.

- `chapters/05_descriptive.md`: **draft v1** (~1,600 words, Tables 5.1–5.4; Figures 5.1–5.2
  requested from econometrics). Numbers from `scripts/descriptive_tables.py`. New finding: the
  full index declines 2008–2020, driven by the USD market category, the other four roughly
  cancelling (ledger C10); reproduced by the main agent and noted in CLAUDE.md. Deflation check
  declined by Orhan ("it is probably the lira"); keep as a cited inference.
- `did_walkthrough.md`: plain-language DiD study aid for Orhan, written before Chapter 6. Orhan
  answered the three check questions well (gap noted: old-metro were partly treated).
- `chapters/06_causal.md`: **draft v1** (~2,900 words, Tables 6.1–6.3). 9 `[VERIFY]`, mostly
  pending econometrics (event-study profile and its fade vs. the 3% log-waste fade; Table 6.2
  rows; SD units). Figures 6.1–6.2 requested. §6.7 verdict is [INT] for Orhan to rewrite.
- Decisions 2026-10-01: municipal burden stays in the index (B0); §5.3 HOLD lifted, animal
  products stay with the break reported as a limitation. Figures 5.1/5.2 requested from econometrics.

**Econometrics requests: all answered 2026-10-01.** Figures 4.3, 5.1, 5.2 and the data
appendix table are in `econometric_models_and_vars/thesis_outputs/`; chapters link them.
Ch. 5 §5.3 (the decline) is marked HOLD for Orhan's review: the decline is USD conversion plus
an animal-product series break, not a sovereignty decline (ledger C10, C15).

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
