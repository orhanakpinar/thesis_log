> **Process history — econometrics strand.** Split out of
> `agent_note_econometrics_FSOI.md` on 2026-09-21 so fresh sessions stop loading it.
> Nothing here was deleted in the split. This is the dated record of *how* decisions were
> reached; the decisions themselves and their rationale live in Part 1 of the main note,
> which is current wherever the two disagree. Variable names here are often pre-rename.

# PART 3 — PROCESS HISTORY (dated record, superseded by Part 1)

*Kept for traceability of how decisions were reached. Where this contradicts Part 1, Part 1 is
current. Variable names in this part are often pre-rename — see the reorg entries.*

## 2026-09-18 (later) — translation fix, unit naming, household-size evidence, open water decision

**1. Water translation corrected (Orhan confirmed).** `Water_Refined_LitrePerPersonPerDay` was a
mistranslation and is now **`Water_Drainage_LitrePerPersonPerDay`**; derived indicators renamed
`water_refined_litre_daily_*` → **`water_drainage_litre_daily_*`**. The source reads "kişi başı
**çekilen** günlük su miktarı" — *çekilen* (drawn/withdrawn) is the same word behind
`Water_Drainage_1000m3PerYear`, whereas *arıtılan* (treated) is what `Water_Refined_1000m3PerYear`
measures. Convention now fixed and documented in the source-rename cell: çekilen → `Water_Drainage_*`,
arıtılan → `Water_Refined_*`. **The data independently confirms the fix** — annualized, this column
correlates r = 0.81 (perHousehold) with the annual *drawn* series but only r = 0.03 with the annual
*treated* series.

**2. Unit suffixes added to land-use indicators** (`landuse_harvested_km2_perArea`, etc., per
Orhan): the source is hectares/decares and the pipeline converts to km² itself, so the derived name
should state the unit rather than making the reader trace the conversion. Collapsed cluster outputs
(`landuse_core_*`, `greenhouse_intensity_*`, `water_supply_*`) deliberately carry **no** unit
suffix — they are means of min-max-scaled values, hence unitless, and `greenhouse_intensity` mixes
tonnage with area so no single unit would be correct.

**3. Household-size evidence (answers the confound flagged in the briefing below).** Ran the check:
- **It is a regional gradient, not a rural/urban one.** Highest 2024 mean household size: Şırnak 4.9,
  Şanlıurfa 4.6, Batman 4.5, Hakkari 4.4, Siirt 4.4, Ağrı 4.3, Mardin 4.3, Van 4.2 — all
  southeast/east. Lowest: Çanakkale 2.5, Giresun 2.5, Edirne 2.6, Balıkesir 2.6, Eskişehir 2.6.
  Urbanization does **not** separate them — Eskişehir (old-metropolitan, urban) sits at 2.6, the
  same as rural Çanakkale at 2.5; Diyarbakır (old-metropolitan) is still 4.1. So Orhan's
  rural-vs-urban hypothesis isn't what the data shows; it's a west–east demographic gradient.
- **The DiD confound is small against the main control group, larger against old-metropolitan.**
  Mean household size change, pre-treatment (2008→2012) vs post (2012→2024): Non-metro −0.373 →
  −0.878; New-metro (treated) −0.307 → −0.857; Old-metro −0.288 → −0.644. Treated-vs-non-metro
  difference-in-differences on household size is only **−0.045** (~1.4% of a ~3.2 base) — reassuring.
  Treated-vs-old-metro is **−0.19** (~6%) — non-trivial. **Implication: the perHousehold denominator
  is safe against the non-metropolitan control, but old-metropolitan comparisons carry a modest
  compositional drift that should be acknowledged.**

**4. Industrialization does NOT explain the perArea/perHousehold divergence.** `Electric_Energy_Use_Total_MWh`
is present in the raw data (656/738) but currently dropped from the main panel — usable as an
industrial/urban-activity proxy. Built a crude proxy (total minus agricultural electricity, per
household) and tested Orhan's industrial-use hypothesis: it correlates **−0.27** with water
perHousehold and **−0.25** with waste perHousehold — weak, and the *wrong sign* for the industrial
story (industrial cities would show higher, not lower, water per household). Also
`Mean_Household_Size` ~ proxy = −0.27, i.e. the same west–east development gradient is showing
through. Meanwhile water ~ waste at perHousehold level is **0.46** (moderate), not ~0 — so they are
related, just far less so than the 0.978 seen at perArea. **Reading: the perArea correlation is a
scale artifact, not industrial-use noise.** `perArea = quantity / km²`, and city area is an
administrative boundary that varies by ~50x (Konya vs Yalova) while being unrelated to the
indicator; any two roughly population-proportional quantities divided by it both collapse onto
population density and therefore onto each other. `perHousehold` divides by a
population-proportional denominator, which cancels that shared scale factor and leaves the
indicator-specific residual — which is why it discriminates and perArea doesn't.

**5. Structural issue found — main panel now violates its own full-coverage invariant.**
`water_drainage_litre_daily_perArea`/`perHousehold` are missing **all of 2024** (82 rows = 81 cities
+ the Türkiye row) — exactly the publication gap that `data_official_Türkiye_extended` exists to
quarantine. Promoting this leftover column into the main panel therefore breaks the main panel's
stated design rule ("full coverage, no NaN"). Not yet resolved — options are to move these two
columns to the extended panel, accept a documented exception, or drop them in favour of the
extended panel's water variables. (Separately: `fertilizer_use_*` shows 12 NaN, not the "3" recorded
further below — 3 is the genuine Hakkari gap, the other 9 are the Türkiye aggregate row, which is
absent from the fertilizer source file. Not a bug, just a more precise count.)

**6. Open decision — drawn vs. treated water (Orhan's three options).** Orhan framed it as: collapse
the two water types, keep both separate, or choose one — with perArea and perHousehold symmetric
either way. Evidence and reasoning to weigh:
- They are genuinely different constructs, not redundant: r = 0.26 at perHousehold (the perArea
  0.99 is the scale artifact described in point 4, so it should not be read as evidence of
  redundancy).
- **They point in opposite framing directions.** *Çekilen* (drawn) measures extraction pressure on
  the resource → fits the **cost/burden** framing locked in for water on 2026-09-12 ("lower is
  better"). *Arıtılan* (treated) measures treatment infrastructure/service capacity → that is a
  **benefit** indicator ("more treatment = better municipal service"). Putting them in one
  cost-framed category would score a city *worse* for treating more of its water, which is
  substantively wrong.
- **Therefore the recommendation is "choose one — drawn":** it matches the locked-in cost framing,
  avoids averaging two opposite-direction constructs, and resolves the perArea/perHousehold
  asymmetry cleanly (drawn_perArea + drawn_perHousehold is a symmetric pair). The treated variable
  would be better used, if at all, as a separate service-capacity indicator in a benefit-framed
  category, not inside cost-framed water.
- **Consequence if drawn is chosen:** drawn water is then measured *twice* — the main panel's daily
  series and the extended panel's annual series (r = 0.998 perArea / 0.81 perHousehold, identical
  656/738 coverage, both missing 2024). One of the two should go; this interacts directly with
  point 5 above.
Not implemented — Orhan's call.

## 2026-09-18 findings — water perArea/perHousehold asymmetry, cross-dataframe redundancy, leave-one-out

**Water perArea/perHousehold mismatch, confirmed (caught by Orhan).** The extended panel's water
cluster is asymmetric: `water_supply_perArea` is a single collapsed column (from
`water_drainage_perArea`/`water_refined_perArea`, r=0.99), but the perHousehold side is still two
separate, uncollapsed columns (`water_drainage_perHousehold`, `water_refined_perHousehold`) —
exactly the perArea/perHousehold weighting-symmetry gap flagged on 2026-09-13 and deferred
("extended panel comes later"). Not yet fixed. **Important number to weigh before collapsing for
symmetry alone:** `water_drainage_perHousehold` ~ `water_refined_perHousehold` only correlates
**r = 0.26** — collapsing them would be justified by symmetry with the perArea track, not by
statistical redundancy (unlike every other collapse in this pipeline, which was correlation-driven
first). Orhan's call on whether symmetry alone is enough justification here.

**Cross-dataframe verification test (run 2026-09-18, per Orhan's request):** does the main panel's
`water_refined_litre_daily` (daily-rate-sourced), annualized (`x365`, converted litre→1000m³),
correlate with the extended panel's yearly water variables? Merged both dataframes on
Year+Location_Name (738/738 rows matched). Results:
- perArea: r = 0.9981 vs. `water_drainage_perArea` (raw), r = 0.9850 vs. `water_refined_perArea`
  (raw), r = 0.9947 vs. the already-collapsed `water_supply_perArea`. **Near-total redundancy** —
  all three perArea water measures, from two structurally different TÜİK source tables (a daily
  per-person survey stat vs. annual city totals), are essentially the same signal.
- perHousehold: r = 0.8056 vs. `water_drainage_perHousehold`, but only r = 0.0294 vs.
  `water_refined_perHousehold` — **not redundant, and the two extended-panel perHousehold
  variables don't even agree with each other** (consistent with their own r=0.26 above).

**Reading this together with the waste finding below:** this is now the *third* case where a
perArea version of a water/waste "total-like" indicator turns out to be near-perfectly correlated
with an entirely different-source indicator that measures something only loosely related in
principle (waste_daily_perArea ~ wasteCollected_1000ton_perArea = 0.999; water_daily_perArea ~
waste_daily_perArea = 0.978 cross-category; and now water_daily_perArea ~ extended water = up to
0.998 cross-dataframe) — while the matching perHousehold pairs consistently do *not* show this
(0.71, 0.03–0.81). This looks like a general pattern, not three isolated coincidences: **perArea
versions of these TÜİK city-total-style indicators may be dominated by city scale/density almost
regardless of what they nominally measure, while perHousehold versions carry more genuine,
indicator-specific signal.** Worth treating as a standing consideration for any future
perArea indicator in this pipeline, not just a one-off fix for water/waste.

**Waste symmetric-drop question (Orhan, 2026-09-18):** given the perArea/perHousehold
weighting-symmetry rule above, dropping `waste_daily_perArea` alone (as previously suggested,
2026-09-17) would itself break that same rule — the real choice is drop-both or keep-both, not
drop-perArea-only. `waste_daily_perHousehold` ~ `wasteCollected_1000ton_perHousehold` = 0.71
(moderate, likely-independent signal) vs. `waste_daily_perArea` ~ `wasteCollected_1000ton_perArea`
= 0.999 (near-total redundancy). Not yet decided.

**Leave-one-out robustness check — noted for later (Orhan, 2026-09-18):** once the composite is
built, add "drop one *category* (not one raw variable), rebuild the FSOI, recheck the DiD
estimate" to the robustness-check list alongside TOPSIS-vs-equal-weight, cost-vs-benefit framing,
and the waiver-years exclusion. Category-level, not variable-level — with only 6 categories this
is a small, interpretable set of checks (6 reruns); variable-level leave-one-out across ~20+
indicators would be excessive and harder to interpret substantively. Not started — this is a
post-composite step, still in variable cleanup as of this note.

## Reorg + rename (2026-09-17, later same day, per Orhan) — supersedes some naming below

The leftover-column step described below was moved earlier in the notebook (right after the
"Transformations" cell that first computes `Mean_Household_Count`, before "Extended Indicators"),
using `Population_Total` directly instead of reconstructing it — simpler, and removes the need to
keep `Mean_Household_Size` alive past its original drop point. Also renamed the two per-person-rate
leftover derivations: `water_refined_perPersonPerDay_perArea`/`perHousehold` →
**`water_daily_perArea`/`perHousehold`**, `waste_collected_perPersonPerDay_perArea`/`perHousehold` →
**`waste_daily_perArea`/`perHousehold`** — once scaled to a population total and re-denominated,
"per person" no longer describes the derived indicator (only the source unit did), so keeping it
in the name was misleading. Re-verified via full notebook execution; correlation numbers are
numerically identical to before (confirms the reconstruction and the direct approach are the same
math). **Anywhere below still says `_perPersonPerDay_perArea`/`perHousehold` or describes
`population_total_reconstructed` — read it as the pre-rename/pre-reorg history, not current code.**

Category variable counts as of this reorg (for the open collapse-candidate question just below):
main panel water = 2 (`water_daily_perArea`, `water_daily_perHousehold` only); main panel waste = 4
(`waste_daily_perArea`/`perHousehold`, `wasteCollected_1000ton_perArea`/`perHousehold`); extended
panel water = 3 real indicators (`water_drainage_perHousehold`, `water_refined_perHousehold`,
`water_supply_perArea`) plus 2 raw columns not yet promoted to indicators.

## Status & Forward Steps (updated 2026-09-17) — superseded by Part 1

**Verification pass (2026-09-17, per Orhan's request), before any of the changes below:**
`fsoi_indicator_selection.ipynb` executed clean end-to-end via `jupyter nbconvert --execute`
from the state left at the end of the 2026-09-13 session (after the electricity-collapse revert)
— zero errors. That confirmed baseline is what all the changes below were built on top of, each
re-verified with its own clean full-notebook execution afterward.

**2026-09-17 changes (all implemented and verified, per Orhan):**

1. **Renamed at the source, not just at the final indicator:** the crop-production-value column
   was ambiguously named `Agricultural_Production_1000TL`/`_1000USD` (vs. the clearly-named
   `_Livestock_1000TL` / `_AnimalProducts_1000TL`). Renamed to `Agricultural_Production_Crop_1000TL`/
   `_1000USD` at the very first rename mapping (the `data_TÜİK.rename(...)` cell, near the top of
   the notebook), so the naming is consistent through the whole derivation chain, not just at the
   end. Final indicator names: `agro_prod_1000USD_perArea`/`perHousehold` → `agro_crop_1000USD_perArea`/
   `perHousehold` (extended panel).
2. **Dropped the redundant bare per-capita columns** (`Agricultural_Production_PerCapita_Crops_USD`,
   `_Livestock_USD`) — these correlate 0.94/0.93 with `agro_crop_1000USD_perHousehold`/
   `agro_livestock_1000USD_perHousehold` (see the new correlation section below), close enough that
   keeping both isn't adding independent signal. **Pairing note (asked for by Orhan):** dropping
   these does *not* leave a perArea/perHousehold pair with a missing side — per-capita is a
   fundamentally different normalization basis with no meaningful perArea equivalent (you'd have to
   go back through population and area, at which point you're just re-deriving
   `agro_crop_1000USD_perArea` from scratch), so the market category's perArea+perHousehold pair
   for crops/livestock was always fully supplied by the `agro_crop_1000USD_*`/`agro_livestock_1000USD_*`
   columns on their own; per-capita was only ever a second, non-paired way of looking at the same
   value, kept as a cross-check (see the redundancy-cleanup cell) and now retired.
3. **The 3 remaining leftover columns are now denominated.** `Population_Density_PeoplePerKm2` is
   dropped outright (0.995-correlated with `wasteCollected_1000ton_perArea`; confirmed *not*
   related to `Mean_Household_Count`'s construction — that uses `Population_Total`, unrelated
   despite the similar name). `Total_Agricultural_Production_Ton` gets the standard
   Total/Area, Total/Household split → `total_agro_production_ton_perArea`/`perHousehold`.
   `Water_Refined_LitrePerPersonPerDay` and `Waste_Collected_KgPerPersonPerDay` (both per-person
   rates) are scaled up to a reconstructed city total (`rate x Population_Total`, recovering
   `Population_Total = Mean_Household_Count x Mean_Household_Size` since the raw column was
   already dropped upstream) and then split into the standard perArea/perHousehold pair, per
   Orhan's explicit direction to extend rather than special-case these two — → `total_agro_production_ton_perArea`/
   `perHousehold`, `water_refined_perPersonPerDay_perArea`/`perHousehold`,
   `waste_collected_perPersonPerDay_perArea`/`perHousehold`. Required a small ordering fix:
   `Mean_Household_Size` is no longer dropped from the main panel in the "Extended Indicators"
   cell (only from the extended panel there) — it's dropped later, at the end of the main
   "Transformations" cell, once the leftover-column step has used it.
4. **New "Detailed high-correlation-pairs table" section added**, right after the existing
   perArea/perHousehold self-check, as a live re-runnable notebook cell (not an offline script)
   — see below for what it surfaced.

**Two things the new correlation table surfaced that need Orhan's attention, not yet acted on:**

- **New near-exact duplicate:** `waste_collected_perPersonPerDay_perArea` (from the just-resolved
  leftover column) correlates **0.9990** with the existing `wasteCollected_1000ton_perArea` —
  higher than the 0.99 that triggered the land-use harvested/sowed collapse. On the surface this
  looks like a genuine collapse candidate. **But see the next point before treating it as one.**
- **Population-density confound in the "scale to total, then divide by Area" approach itself:**
  `water_refined_perPersonPerDay_perArea` also correlates strongly with
  `waste_collected_perPersonPerDay_perArea` (0.9784) and with `wasteCollected_1000ton_perArea`
  (0.9773) — a *cross-category* correlation (water vs. waste), which is suspicious. Reasoning
  through why: `perArea = (rate_per_person x Population_Total) / Area_km2 = rate_per_person x
  Population_Density`. Since population density varies far more across cities than the
  underlying per-person rate does, **any indicator built this way (rate × reconstructed
  population, divided by area) is mathematically dominated by population density**, not by the
  behavior the rate is meant to capture — so it's expected to correlate highly with *any other*
  area-based indicator that's also secretly density-driven (like `wasteCollected_1000ton_perArea`,
  which is also just "more people → more collected waste per km²"), regardless of whether the two
  variables measure related things at all. **This means the perArea forms of these two new
  leftover indicators may be adding population-density noise rather than genuine
  water/waste-behavior signal** — worth Orhan's explicit call on whether to keep them as normal
  indicators, treat them with caution/exclude from the perArea track, or address density as a
  separate control. Note the perHousehold forms of these same two variables do **not** have this
  problem — algebraically, `perHousehold = rate_per_person x Mean_Household_Size` (population
  cancels out entirely), so they're clean; the population-density issue is specific to the perArea
  reconstruction. Flagging both points to Orhan directly rather than deciding unilaterally.

## Status & Forward Steps (updated 2026-09-13) — superseded by the 2026-09-17 update above

**Correction (2026-09-13, same day):** the electricity collapse described just below
(`electricity_agriculture_combined`) was flagged by Orhan as wrong — it blended a variable's own
perArea and perHousehold forms, which this pipeline treats as two permanently separate tracks —
and was reverted in code the same day. `electricity_agriculture_mwh_perArea` and
`_perHousehold` are two separate, uncollapsed columns in the actual notebook; ignore the
`electricity_agriculture_combined` references below.

**2026-09-13 update:** forward-plan step 1 (collapse-candidate sub-indices) is now implemented
and verified in `fsoi_indicator_selection.ipynb`, in a new "Collapsing correlated indicator
clusters into sub-indices" section right after the "## Food Sovereignty Index" header. Ran the
full notebook end-to-end via `jupyter nbconvert --execute` — no errors; the four new columns
land in [0, 1] with no unexpected NaNs introduced (verified by extracting the executed cells to
a plain script and checking `.describe()`/`.isna().sum()` on the new columns).

- **Method:** each cluster's constituent columns are independently min-max scaled to [0, 1]
  (pooled across all rows, Türkiye aggregate row included, matching how the correlation checks
  elsewhere in the notebook already treat the panel), then simple-averaged — implements the
  2026-09-11 "simple mean of standardized values" decision. **Open question, not yet confirmed
  by Orhan: min-max vs. z-score for this within-cluster standardization step** — min-max was
  chosen to keep the combined value non-negative/bounded ahead of the later `log1p` + winsorized
  min-max pipeline step, but this specific choice was never pinned down explicitly before now,
  so flag it before treating it as settled.
- **Main panel (`data_official_Türkiye`):** `landuse_harvested_perArea`/`landuse_sowed_perArea`
  → `landuse_core_perArea` (and the `_perHousehold` pair → `landuse_core_perHousehold`);
  `agro_greenhouse_prod_ton_perArea`/`landuse_greenhouse_perArea` → `greenhouse_intensity_perArea`
  (and the `_perHousehold` pair → `greenhouse_intensity_perHousehold`). perArea/perHousehold
  split is preserved — the redundancy resolved is between the two *source* variables, not
  between area/household normalization forms of one variable.
- **Extended panel (`data_official_Türkiye_extended`):** `water_drainage_perArea`/
  `water_refined_perArea` → `water_supply_perArea` (perArea only — perHousehold forms weren't
  correlated, kept separate/uncollapsed). `electricity_agriculture_mwh_perArea`/
  `electricity_agriculture_mwh_perHousehold` → `electricity_agriculture_combined` — this one
  collapses the *same* variable's own perArea/perHousehold forms into each other (structurally
  different from the other three clusters), so the result has no further perArea/perHousehold
  split.
- Note: this note's own earlier spelling `electricty_agriculture_mwh_perArea` (see "Variable
  Redundancy Map" section below) was a typo — the actual notebook code spells it
  `electricity_agriculture_mwh_perArea` correctly; used the code's spelling when implementing.

## Status & Forward Steps (updated 2026-09-12) — superseded by the 2026-09-13 update above

**Done:** main/extended dataframe split; `Treated` 4-category categorical + labels; correlation/
redundancy groundwork on both dataframes; methodology grounded in Yilmaz (2025, Entropy-TOPSIS)
and GFSI (2022) — simple-mean sub-indices over PCA, pooled+per-year winsorized min-max over
z-score; FSOI positioned as a critical comparative index to GFSI; cross-strand categorical
question resolved (**FSOI stays at 6 categories**, no political category).

**Both former blockers are now resolved (2026-09-12):**
- **Aggregation: equal-weighted sum is primary**; TOPSIS is an appendix-level robustness check,
  not co-equal (see "Comparison scope" note below on why this isn't 4 co-equal models).
- **Benefit/cost direction: cost/burden framing** for water, waste, energy, and land-use fallow
  (Orhan, 2026-09-12) — i.e. the primary model treats these as "lower is better." Capacity/
  benefit framing becomes the robustness-check alternative, not the primary reading.
- **Land-use fallow: kept, not eliminated.** Checked correlation against harvested/sowed first
  (r = 0.32–0.65 — moderate, well below the >0.9 bar used for actual collapse candidates), so
  elimination wasn't statistically justified. Orhan's framing: fallow is conceptually the
  *negative* of harvested land (unused vs. used) — fits the cost framing directly, not
  eliminated.
- **New indicator added: fertilizer use, folded into `energy` (cost)** — see "New Data —
  Fertilizer Use" section below for full detail. `data_official_Türkiye` is now (738, 26).

**Forward plan** (full detail in "Synthesized pipeline plan" below — steps renumbered to match
current status; step 4 below was step 1 there and remains the next open implementation item):
1. ~~Build simple-mean sub-indices for the remaining collapse candidates (land-use
   harvested/sowed, greenhouse cluster, water drainage/refined, electricity perArea/perHousehold).~~
   **Done 2026-09-13** — see update above.
2. `log1p` skewed indicators, then normalize (pooled + per-year, winsorized min-max).
3. Aggregate into the 6 category sub-indices, documented inline, applying cost-direction flips
   where decided above.
4. Normalize the 4 leftover columns in main (`Total_Agricultural_Production_Ton`,
   `Water_Refined_LitrePerPersonPerDay`, `Waste_Collected_KgPerPersonPerDay`, drop
   `Population_Density_PeoplePerKm2`) — plan agreed earlier, still not coded as of 2026-09-12.
5. Produce the primary FSOI composite (equal-weight, cost-framed) + top/bottom example cities.
6. Robustness checks: TOPSIS vs. equal-weight; benefit-framing vs. cost-framing — report as
   appendix-level sensitivity analysis, not additional co-equal headline results.
7. That composite (step 5) is the "durable result" that triggers reporting back to
   `thesis_log_main_agent` for its CLAUDE.md Results-status update.

Not this session's work: Gazette/Ministry-news become a national-level companion analysis, not
a composite input (see "Cross-strand note" below).


---

## Moved from Part 2 on 2026-09-21 (trim, step 3)

These were working material in Part 2 that is now spent: the redundancy map guided a
variable selection that is complete, and the pipeline plan and the open benefit/cost item
were both superseded by decisions recorded in Part 1 and in Part 2's "Resolved" section.
Kept for traceability and for defending how each choice was reached.

## Variable Redundancy Map (2026-09-11)

Correlation analysis of the two dataframes' *final* indicator columns only — raw/intermediate
columns (`Area_km2`, `Mean_Household_Count`, un-normalized USD/water/energy amounts) excluded
from these correlations since they're dominated by city-size and would drown out genuine
indicator-to-indicator redundancy. Not decisions — a map to work from before choosing an index
formula. Main and extended analysed separately, per Orhan's request.

### `data_official_Türkiye` — 16 final indicators, 4 unused leftover raw columns

**Collapse candidates (r > 0.9, near-duplicate signal):**
- `landuse_harvested_*` ≈ `landuse_sowed_*` (0.99 both perArea and perHousehold) — harvested
  and sowed land area are almost the same thing agronomically; 4 variables carrying ~2
  independent signals.
- Greenhouse cluster — `agro_greenhouse_prod_ton_perArea/perHousehold` and
  `landuse_greenhouse_perArea/perHousehold` are all mutually correlated 0.89–0.96; 4 variables,
  ~1 latent "greenhouse intensity" factor.

**perArea vs perHousehold genuinely diverge (keep both, don't collapse):**
- `wasteCollected_1000ton_perArea` vs `perHousehold`: r = 0.19 — different pictures.
- `landuse_vegetables_perArea` vs `perHousehold`: r = 0.70 — moderate, defensible to keep both.

**Unused leftover raw columns — need an explicit keep/drop call, not yet indicators:**
- `Total_Agricultural_Production_Ton` — correlates weakly (< 0.07) with everything currently
  in the indicator set. An independent signal if promoted, not redundant with anything.
- `Population_Density_PeoplePerKm2` — correlates 0.995 with `wasteCollected_1000ton_perArea`.
  If promoted to an indicator, pick one or the other, not both.
- `Water_Refined_LitrePerPersonPerDay` — weak correlation with everything (< 0.23). Note this
  is a *different* water-refined variable than the one in the extended dataframe
  (per-person-per-day here vs. total-1000m³-per-year there) — don't conflate the two when
  deciding what to do with it.
- `Waste_Collected_KgPerPersonPerDay` — string dtype (not yet cleaned to numeric), so not
  checked here at all. **Cleaning gotcha, verified 2026-09-13**: values use Turkish
  comma-decimals (`'1,15'`, same pattern `Mean_Household_Size` needed `.str.replace(',', '.')`
  for) — but at least one value additionally has a **leading non-breaking space**
  (`'\xa01,15'`, U+00A0, not a regular space). A plain `.str.replace(',', '.').astype(float)`
  will raise on that row — strip whitespace (`.str.strip()`, which handles `\xa0` too, or
  explicit `.str.replace('\xa0', '')`) before the comma replacement, not after assuming it's
  already clean.

### `data_official_Türkiye_extended` — 14 final indicators, 8 intermediate/raw columns kept only as denominators/reference

**Collapse candidates:**
- `water_drainage_perArea` ≈ `water_refined_perArea` (r = 0.99) — nearly redundant with each
  other in the per-Area form specifically (their perHousehold forms don't show this).
- `electricty_agriculture_mwh_perArea` ≈ `perHousehold` (r = 0.88).

**Resolved (2026-09-11) — dropped as near-exact duplicates:**
- Derived `Agricultural_Production_PerCapita_Crops_USD_perHousehold` /
  `..._Livestock_USD_perHousehold` (via `PerCapita_*_USD × Mean_Household_Size`, since
  `Mean_Household_Count = Population_Total / Mean_Household_Size` by construction) to see
  whether TÜİK's own per-capita figure agreed with the total÷household-count derivation
  already in the pipeline. Result: r = 0.9999999 against `agro_prod_1000USD_perHousehold` /
  `agro_livestock_1000USD_perHousehold` respectively — not a cross-check, effectively the same
  variable. Dropped the newly-derived ones, kept the existing total-derived ones (naming
  already matches the `_perArea`/`_perHousehold` convention). The bare `PerCapita_Crops_USD` /
  `PerCapita_Livestock_USD` (pure per-capita, no household-size multiplication) stay — that's
  a genuinely different normalization basis, not redundant.
  (Earlier version of this note logged this same pair at r = 0.94 as an "internal-consistency
  check, not a problem" — that number was per-capita vs per-household on mismatched unit
  bases, before the household-size correction; 0.9999999 is the corrected comparison and the
  one that actually mattered.)

**perArea vs perHousehold genuinely diverge (keep both):**
- `agro_prod_1000USD`, `agro_livestock_1000USD`, `agro_animalproducts_1000USD`: r = 0.39–0.59
  between their own perArea/perHousehold forms — meaningfully different normalizations.

**Not yet resolved:** whether the raw (non-normalized) `Agricultural_Production_1000USD` /
`_Livestock_1000USD` / `_AnimalProducts_1000USD` and `Water_Drainage_1000m3PerYear` /
`Water_Refined_1000m3PerYear` / `Electric_Energy_Use_Agriculture_MWh` should be dropped
entirely now that their per-Area/per-Household versions exist (they're ~0.97–0.999 correlated
with `Area_km2`/`Mean_Household_Count`, i.e. mostly just city-size proxies on their own) — kept
for now since they're needed to derive the normalized versions, but not themselves meaningful
FSOI indicators.

**Still open** (unlike the per-capita/per-household pair above, not yet decided): the main
dataframe's `landuse_harvested_*`≈`landuse_sowed_*` and greenhouse-cluster collapse
candidates, and this dataframe's `water_drainage_perArea`≈`water_refined_perArea` and
`electricity_agriculture_mwh_perArea`≈`perHousehold` pairs.

**Checked in with `thesis_log_main_agent` (2026-09-11):** no `CLAUDE.md` update needed for
redundancy-pair resolutions like the one above — the existing "raw/untidy, being reworked,
see this note" text already covers it. It wants to hear back only when (a) composite index
construction actually starts/produces something durable (the real trigger for the
Results-status paragraph), or (b) resolving a collapse candidate eliminates one of the six
stated FSOI categories entirely — **market, production, water, waste, energy, land-use** —
rather than just reducing variable count within one. None of the still-open collapse
candidates above look category-eliminating on their own (each is a within-category
reduction), so check against this list before assuming a resolution needs reporting.

### Methodological option for correlated clusters — decided 2026-09-11

Considered PCA/factor grouping vs. a simple mean of standardized values for the collapse
candidates (land-use harvested/sowed, greenhouse cluster, water drainage/refined, electricity
perArea/perHousehold). **Decision: simple mean, not PCA/factor.** PCA rejected as "too
mathematical... we need to be open" (Orhan, 2026-09-11) — components are hard to name/justify
in a thesis. Factor analysis is close to degenerate on our 2-variable clusters anyway (no
meaningful separation of shared vs. unique variance with only 2 indicators). A simple mean of
standardized values is transparent, works uniformly across 2- and 4-variable clusters, and
needs only one sentence to justify ("combined because they measure the same underlying
activity"). Not yet implemented in the notebook as of 2026-09-11 — blocked on the benefit/cost
direction decision below, since you can't average standardized values meaningfully until you
know which direction "better" points for each one.


### Synthesized pipeline plan, in order

1. Resolve the 4 unused leftover columns in main (`Total_Agricultural_Production_Ton` →
   divide by `Mean_Household_Count` *before* that column gets dropped; `Water_Refined_
   LitrePerPersonPerDay` and `Waste_Collected_KgPerPersonPerDay` → multiply by
   `Mean_Household_Size` to get per-household, same identity as the per-capita→per-household
   conversion already done; `Population_Density_PeoplePerKm2` → drop, not promoted, per Orhan
   — it's 0.995 correlated with `wasteCollected_1000ton_perArea` and adds nothing). **Not yet
   implemented as of 2026-09-11.**
2. Build the simple-mean sub-indices for the correlated clusters (previous section). **Not yet
   implemented — blocked on step 4 (benefit/cost direction).**
3. Pre-process: `log1p` (not raw `log`, some city-years may have zero values) on right-skewed
   money/volume indicators, before any normalization. **Full rationale (added 2026-09-14, asked
   by Orhan):** most indicators here are right-skewed — a handful of large cities (İstanbul,
   Konya) produce/consume far more than the median city, so on a raw or linear min-max scale
   those outliers compress every other city into a narrow band near 0. A log transform pulls in
   the long right tail, making the distribution closer to symmetric before any mean-based step
   (cluster-averaging, later min-max) runs on it. `log1p` specifically (not plain `log`) because
   `log(0)` is undefined and several indicators have genuine zero values in some city-years (e.g.
   zero greenhouse production for a small city in a given year); `log1p(x) = log(1+x)` is defined
   at `x=0` and behaves like `log(x)` for large `x`, so true zeros don't need an arbitrary added
   constant.
4. **Benefit/cost direction per category — the open item, see below. Blocks steps 2 and 5.**
5. Normalize: **both pooled (2008–2024, fixed thresholds, GFSI-style) and per-year (min-max)**
   side by side — pooled is what supports the DiD comparison (a score change has to mean the
   city actually changed, not that it moved relative to whoever else was measured that year);
   per-year is for descriptive "who's leading in year X" / treated-vs-control-by-year snapshots,
   which Orhan also explicitly wants. Winsorize (cap at ~1st/99th percentile) before min-max for
   outlier robustness, rather than switching to z-score — keeps the 0–100 scale GFSI-style. Both
   z-score and TOPSIS's vector normalization remain available as secondary/robustness
   comparisons, not primary — z-score doesn't naturally bound to 0–100, and vector normalization
   is really TOPSIS-internal machinery rather than a general-purpose alternative to min-max.
6. Aggregate into the 6 category sub-indices, with inline notebook comments documenting each
   indicator's rationale (GFSI convention) — mirror into this note and thesis text as written.
7. Compare **equal-weighted sum vs. TOPSIS** at the category level (GFSI's neutral-weights
   option vs. Yilmaz's Entropy-TOPSIS approach) — if rankings diverge meaningfully, that's a
   reportable finding about compensability, not just a robustness footnote.
8. As a further robustness axis: compare rankings **under alternative benefit/cost direction
   assignments** for the ambiguous categories (water/waste/energy — see below), the same way
   step 7 compares aggregation methods. Answers Orhan's "will there be a ratio for comparison?"
   — yes, this sensitivity check is that ratio/comparison.


### Open item — benefit/cost direction per category (superseded by "Resolved" above, kept for its reasoning)

TOPSIS-style indices require every criterion marked as **benefit** (higher = better) or
**cost** (lower = better) before normalization. This isn't just bookkeeping — get it backwards
and a genuinely *worse* city scores *better*. Orhan's concern, stated directly: could a "lower
= better" framing make small cities look artificially good just because they use/produce less
in absolute terms? Since our indicators are already `_perArea`/`_perHousehold` ratios (not raw
totals), pure city-size shouldn't drive this the way it would for unnormalized data — but the
risk re-appears wherever a ratio itself is ambiguous about what "more" means. Category by
category:

| Category | Direction | Reasoning |
|---|---|---|
| Market (crop/livestock/animal value) | **Benefit** (clear) | More agricultural economic value per unit land/household = more food-sovereignty capacity. |
| Production (greenhouse) | **Benefit** (clear) | More local production intensity = more food produced locally. |
| Land-use — harvested/sowed/vegetables/longtermCrops/greenhouse | **Benefit** (clear) | More land under active cultivation = more capacity. |
| Land-use — **fallow** | **Ambiguous, needs a call** | Could read as cost (under-utilized land) *or* benefit (crop rotation / soil rest — a sustainability practice the lit review's agroecological framing would likely value, not penalize). |
| Water (drainage/refined) | **Ambiguous, needs a call** | Benefit reading: irrigation/resource *access* and capacity (GFSI treats water/irrigation infrastructure as straightforwardly good). Cost reading: consumption pressure on a scarce resource (Yilmaz treats energy/water-linked intensity as a sustainability cost). Which framing fits FSOI's theoretical stance is Orhan's call, not a statistical one. |
| Waste (collected) | **Ambiguous, needs a call — this is the specific case Orhan asked about** | If `wasteCollected` measures **municipal collection infrastructure/coverage** (a service-capacity signal), it should be a benefit — more collection = better municipal capacity, analogous to GFSI's food-safety-net-program indicators being scored as straightforwardly positive. If it measures **waste generated** (a resource-efficiency signal), it should be a cost, matching Yilmaz's fertilizer/pesticide-intensity-as-cost logic — and in that reading, yes, a city with lower per-household waste generation would score better for that reason alone, independent of anything else about its food sovereignty. Need to check TÜİK's exact definition of this indicator before deciding — the two readings point in opposite directions. |
| Energy (agricultural electricity) | **Ambiguous, needs a call** | Benefit reading: mechanization/irrigation-pump capacity, farm technology access. Cost reading: input-intensity/environmental footprint (Yilmaz's explicit framing). Same tension as water. |

**Recommendation:** don't force a single answer — resolve Market/Production/Land-use (mostly
settled above) now, and for the four ambiguous rows (fallow, water, waste, energy) build the
composite under **both** readings and compare (step 8 above), the same way step 7 compares
equal-weight vs. TOPSIS. If the ranking is stable either way, direction didn't matter much for
your results. If it isn't, that instability is itself worth reporting — it would mean FSOI's
verdict on a city depends on whether you frame resource use as capacity or as burden, which is
exactly the kind of thing a sovereignty-vs-security framing debate should surface.
