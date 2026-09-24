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

---

## Moved from Part 1 on 2026-09-24 (note hygiene pass)

The full DiD narrative — every intermediate specification, every conclusion later
corrected (the mechanism check's onset-vs-fade reasoning, the group-ranking claim
before TOPSIS overturned it, the pre-isolation-check overclaim about production/
land-use/external-input), in the order it happened. Compressed into a current-state
summary in Part 1 ("Aggregation, DiD, and robustness — current state"); kept here for
traceability and for defending how each number was actually reached.

   **This inverts the provisional thesis PDF's group ordering** (old-metro highest → new-metro
   → non-metro lowest, per the PDF's own inference that "greatness of a city correlates with
   domestic food production"). The rebuilt index gives the opposite order: non-metropolitan
   highest, then old-metropolitan, then new-metropolitan lowest. Not a magnitude shift — a
   direction reversal. Expected, not alarming: the PDF's numbers were built on variables since
   found to carry the treatment in their own denominators (see the water measurement confound
   above). But any thesis prose already written on the old ordering needs rewriting, not
   reconciling, with the new one. `thesis_log_main_agent` recorded this in CLAUDE.md as an
   explicit supersession and is raising it with Orhan directly given the implication for
   `writing_drafts/`.

   **Diagnostic 7 (2026-09-22) — traced the reversal, doesn't fully explain it.** Added after
   the aggregation cells, computed live from `diagnostic_raw`: correlated `Mean_Household_Size`
   against the Track C composite and each category, at the city level, 2020.
   - **`municipal_burden` alone drives almost all of the group gap.** Category means by group:
     non-metro 0.744, old-metro 0.563, new-metro 0.536 — a spread of ~0.21, roughly 3× any
     other category's spread (production ~0.04, land_use ~0.01, external_input ~0.06, market
     ~0.13). The overall FSOI gap (non-metro 0.500 vs new-metro 0.424, a spread of 0.076) is
     substantially a municipal_burden effect.
   - **Household size correlates with municipal_burden specifically** (city-level Spearman
     ρ = −0.504, all cities, 2020), much more than with FSOI overall (ρ = −0.280) or with any
     other single category (all |ρ| < 0.19). Group-average household size lines up the same
     way: new-metro largest (3.514) → lowest municipal_burden score; non-metro smallest (3.343)
     → highest. Mechanically consistent with the household-vs-per-capita briefing above
     (perHousehold = per-capita × household size, so cost-framed indicators, which are flipped,
     score worse for larger households) — but the within-non-metropolitan-only correlation
     (ρ = −0.064) is far weaker than the all-cities figure, so this is **partly a between-group
     pattern, not purely a general mechanical link.**
   - **This is one candidate contributor, not a full account.** `municipal_burden` is also
     exactly the category carrying both previously-documented Law 6360 confounds — the
     coverage-expansion effect and the tariff waiver (see "Law 6360 confounds" above) — so three
     distinct explanations (coverage expansion, tariff waiver, household-size denomination)
     converge on the same category, and a Spearman correlation cannot disentangle them.
     **Do not write "household size explains the reversal"** — write that municipal_burden
     drives the reversal, and household size is one correlated, partially-confirmed contributor
     to *that category* specifically, alongside two other unresolved confounds on the same
     variable.

   **LOCO on municipal_burden (2026-09-22) — the ordering survives, the size doesn't.**
   Elevated by `thesis_log_main_agent` above the rest of the item-5 robustness list: run
   before any prose touches the group comparison, since the headline result and the most
   confound-laden category were the same object, making this a question of whether the
   result exists rather than how robust it is. Rebuilt Track C's composite from the
   remaining four categories (production, land_use, external_input, market) and compared
   group means against the full five-category version, every shared year (2008–2020), not
   just 2020.
   - **Non-metropolitan leads in all seven years, with or without municipal_burden.** The
     ordering is not a municipal_burden artifact.
   - **But the gap shrinks 38%** — non-metro minus new-metro averages 0.058 with
     municipal_burden, 0.035 without it. Municipal_burden doesn't create the result, but it
     inflates its size substantially.
   - **Old-metropolitan vs. new-metropolitan is not stable** without municipal_burden — they
     swap rank across years (e.g. 2018/2020 old-metro edges above new-metro; 2014/2016 the
     reverse) — only "non-metro leads" is a stable finding across years and across LOCO,
     not the full three-way ordering.
   - **Reportable statement:** non-metropolitan cities score higher on the four-category
     (production, land-use, external-input, market) headline index too, not only when
     municipal burden is included — but roughly a third of the *size* of the full-index gap
     traces to a category still carrying two unresolved Law 6360 confounds plus a partial
     household-size correlation, so the *magnitude* should be reported with that caveat even
     though the *direction* does not need it.

5. ~~The DiD regression itself~~ — **done, 2026-09-22.** Two-way fixed effects (city + year),
   `FSOI ~ Treated×Post`, cluster-robust SE by city, Track A (four categories, 2008–2024),
   non-metropolitan-only control (old-metropolitan excluded from the primary spec — see
   "Control groups" above). Executed clean, 94 cells, 0 errors.

   **Primary estimate: −0.0373 (SE 0.0126, p = 0.0031, 95% CI [−0.062, −0.012]).** Pre-trends
   clean on the (weak, two-point) test available: neither 2008 nor 2010 differs significantly
   from 2012. Effect appears immediately in 2014, holds significant and roughly stable
   (−0.04 to −0.05) through 2020, weakens by 2022, and is no longer significant by 2024.
   Robust to pooling old-metropolitan into the control (−0.033, a small shift toward zero in
   the expected direction).

   **⚠️ THE ESTIMATE DOES NOT SURVIVE REMOVING MUNICIPAL_BURDEN — the single most important
   qualifier on any DiD number from this pipeline so far.** Unlike the descriptive group-mean
   result above (which survived LOCO, just smaller), the causal estimate does not survive it
   at all: without `municipal_burden`, the DiD estimate is **+0.0085 (SE 0.0070, p = 0.224)**
   — sign flips, significance disappears. **The entire significant effect is generated by
   `municipal_burden` (waste, in Track A) alone; production, land-use and external-input show
   no detectable treatment effect.** `municipal_burden` is exactly the category carrying two
   unresolved Law 6360 confounds (coverage-boundary expansion, tariff waiver) plus the
   Diagnostic 7 household-size correlation.

   **Mechanism check (2026-09-22) — the onset doesn't discriminate; the fade does, and it
   points toward the waiver, not away from it. Corrected 2026-09-23 after main agent
   re-derived the waiver hypothesis more completely.** The original write-up here (09-22)
   concluded "favours coverage-boundary expansion" from the sharp 2014 onset. That was
   incomplete: it tested only "costs stay capped and invisible until the waiver lifts, effect
   grows from 2020" and correctly rejected it — but a second waiver story ("cheap capped
   costs encourage more use 2014–2019, usage recedes once prices normalize in 2020") predicts
   the **same 2014 onset as boundary-expansion**, so onset timing cannot distinguish the two
   mechanisms at all. What can distinguish them is the **fade**: −0.177 (2014) → −0.204 →
   −0.233 (2018, peak, still inside the waiver) → −0.179 (2020) → −0.126 (2022) → −0.140
   (2024), a ~27% decline from the 2014–2018 mean to 2020–2024. A permanent boundary
   redefinition has no built-in reason to fade; a price cap that lifts in 2019/2020 does.
   **Corrected reading: consistent with a price-driven waiver mechanism, not distinguishable
   from boundary-expansion by onset alone.** Not settled either way: the fade lands exactly
   on 2020, simultaneously the COVID year — an already-documented confound this design cannot
   separate from a price-normalization effect. Three explanations (boundary expansion,
   tariff waiver, COVID) now sit on this fade, on top of Diagnostic 7's household-size
   correlation. Scope limit unchanged: Track A's municipal_burden is waste-only; the waiver's
   headline provision targets water tariffs specifically. A direct test on `water_drainage`
   (Track C, extended panel, 2008–2022) remains the natural next check, not built.

   **Equal-weight-per-indicator robustness (2026-09-23, Orhan-requested, required).** Category
   weighting gives `municipal_burden` and `external_input` 25% each alone in Track A (vs. 5%
   per land-use indicator, a measured 5× disparity) — a plausible non-confound reason
   `municipal_burden` dominates. Built `build_fsoi_flat()`: every indicator gets equal weight
   (1/9 Track A, 1/14 Track C) instead of equal-category-then-equal-within. **Result:
   strengthens the core finding rather than undermining it.** Group-ordering direction
   survives (non-metro still highest, both weightings). Primary DiD shrinks but stays
   significant under flat weighting: −0.027 (p = 0.0007) vs. −0.037 (p = 0.003) category-
   weighted, about 28% smaller, consistent with municipal_burden's reduced weight. **LOCO
   under flat weighting: −0.0082 (p = 0.174), not significant** — sign stays negative here
   (unlike the category-weighted LOCO, which flipped positive), but significance still
   disappears. **"No detectable treatment effect on production/land-use/external-input once
   municipal_burden is removed" now holds under two independently-constructed weighting
   schemes** — not an artifact of the specific choice to weight categories rather than
   indicators. Category weighting remains the primary specification (consistent with the
   settled equal-category-weight methodology and GFSI's convention); flat weighting is a
   reported robustness check, not a rival headline. One further real difference worth
   carrying forward: city-level rankings agree only moderately between the two schemes
   (Spearman ρ = 0.681, Track A, all years) — the group direction is stable, individual city
   rankings are more weighting-sensitive than that might suggest.

   **What this licenses and what it doesn't.** "Law 6360 changed waste-per-household outcomes
   in treated cities" is a defensible reading of this specification. **"Law 6360 reduced food
   sovereignty" is not** — the categories that would make that a food-sovereignty claim show
   nothing. Do not cite −0.037 as evidence about food sovereignty without this qualifier
   attached; it is currently better described as a waste-specific finding riding inside a
   food-sovereignty-labelled composite.

   **Wild cluster bootstrap run (2026-09-22) — confirms the primary estimate's significance
   is not a small-cluster artifact.** 14 treated clusters is exactly the regime where
   asymptotic cluster-robust inference is unreliable (Cameron/Gelbach/Miller 2008;
   Bertrand/Duflo/Mullainathan 2004), so this was treated as blocking, not optional, before
   citing the primary number. Rademacher WCR bootstrap, 999 draws, restricted-residual
   procedure: **p = 0.0040**, essentially identical to the asymptotic p = 0.0031. Net effect
   on interpretation: this **confirms** the primary estimate is a statistically solid
   finding — about waste collection specifically, per the LOCO result above, not about food
   sovereignty. `statsmodels` (0.14.5) added to `requirements.txt` by `thesis_log_main_agent`.
6. ~~Produce the primary FSOI composite + top/bottom cities~~ — done, see item 3 above.
7. ~~Remaining robustness checks~~ — **done, 2026-09-23, run as one consolidated batch per
   Orhan's request.** Wild cluster bootstrap already covered under item 5. Three more:

   **TOPSIS vs. equal-weighted sum.** Same per-indicator weights as the primary spec (isolates
   the aggregation-method choice from weighting), ideal points fixed from the full city panel.
   City-level ranks agree closely with the primary (ρ = 0.917). **The causal finding gets its
   sharpest confirmation yet:** DiD −0.025 (p = 0.002) vs. primary −0.037 (p = 0.003); without
   municipal_burden, −0.0003 (p = 0.968) — not just insignificant, essentially exactly zero.
   Now confirmed across three independent aggregation methods (category-weighted, flat-
   weighted, TOPSIS).

   **⚠️ But TOPSIS overturns a descriptive claim, not the causal one.** Group means:
   equal-weighted-sum gives non-metro 0.507 > old-metro 0.484 > new-metro 0.466. **TOPSIS
   gives old-metro 0.366 > non-metro 0.336 > new-metro 0.322 — old-metropolitan leads, not
   non-metropolitan.** New-metropolitan stays lowest under both, which is all the DiD needs,
   so the causal estimate is unaffected. But **"non-metropolitan scores highest" (from the
   item-3 LOCO section) is method-specific, not aggregation-robust, and must not be reported
   as a settled finding.** Correct framing: new-metro lowest under both methods tried; which
   of the other two groups leads depends on aggregation choice.

   **Benefit-framing vs. cost-framing.** No flips at all (every indicator's `_norm` used
   directly). Sign flips as predicted: +0.031 (p = 0.008) vs. −0.037 cost-framed. **Not new
   evidence** — mechanically expected, since benefit-framing directly re-signs the
   municipal_burden indicators the whole result depends on. Confirms the sign is a direct
   consequence of the cost/burden convention settled 2026-09-12; does not reopen it.

   **Waiver-years exclusion.** Dropping 2014/2016/2018 entirely (n: 585 → 390): −0.034
   (p = 0.042) vs. −0.037 (p = 0.003) full sample — similar magnitude, weaker significance
   (smaller n), effect does not depend on the waiver years specifically. Without
   municipal_burden: +0.003 (p = 0.746) — same story, a fourth confirmation.

   **State of the causal claim after four independent robustness checks (category-weighted,
   flat-weighted, TOPSIS, waiver-years-excluded), all reported side by side, none replacing
   the primary:** the significant negative composite effect and its complete disappearance
   without municipal_burden both replicate every time. Only two things are robust across all
   specifications: **new-metropolitan cities score lowest**, and **the causal effect is a
   municipal_burden (waste) effect with no detectable counterpart in production, land-use or
   external-input.** The three-way group ordering is not robust and should not be reported as
   settled.

7a. **Does the original pre-rebuild "national decline, independent of Law 6360" finding
    survive on the rebuilt index? (Orhan's question, 2026-09-24) — No, it does not
    replicate at all, in either direction.** A different question from the robustness queue
    above: the original finding was a common time trend across all three groups, exactly
    what the DiD's year fixed effects net out, so nothing in items 5–7 tested it. Checked
    directly via two independent operationalizations of "national," both on the full panel
    (all three real groups, not the DiD's two-group subsample):
    - **Cross-city pooled linear trend (city FE, cluster-robust SE):** WITH
      municipal_burden, **+0.00195/year (p < 0.0001) — a significant INCREASE**, not a
      decline. WITHOUT municipal_burden, flat and non-significant: −0.00007/year (p = 0.844).
      Every group's raw 2008-to-2024 change increases when municipal_burden is included
      (non-metro +0.030, new-metro +0.013, old-metro +0.010).
    - **The `Türkiye` aggregate row itself:** same pattern — 0.487 → 0.510 (+0.023) with
      municipal_burden; 0.472 → 0.463 (small, untested decline, consistent with the flat
      pooled trend) without it.
    - **This is stronger than "doesn't survive without municipal_burden."** The rebuilt Track
      A composite shows no national decline in the first place — if anything a mild,
      significant *increase* with municipal_burden included, and a flat trend without it.
      Do not carry the original "national decline, independent of Law 6360" claim forward as
      if it still holds; it needs to be reported as **not replicating on the rebuilt
      pipeline**, not merely qualified.
    - **Scope limit, stated plainly:** this is a comparison against a different, now-
      superseded index construction — the original PDF's composite step "is not reproducible
      from current repo code" and used "raw/untidy" variables (CLAUDE.md, Results-status).
      This check cannot say *why* the two disagree (different variables, normalisation,
      weighting, or a different definition of "decline" — e.g. raw production tonnage alone
      — are all live possibilities, none tested here). What it *can* say: on the current,
      validated pipeline, Track A shows no decline. A fact about this index, not necessarily
      a refutation of whatever the original analysis measured.
---

## Moved from the top of the file on 2026-09-24 (note hygiene pass)

The original 2026-09-20 HANDOVER section, fully superseded by everything since --
kept for traceability of what the state was at that point in the project.

# HANDOVER — session change 2026-09-20

Written by `thesis_log_econometrics_agent` before Orhan starts a fresh session. Treat the incoming
session as continuous with this one: same scope (`econometric_models_and_vars/`), same open items.
`thesis_log_main_agent` has been notified.

**Where the work stands.** Variable selection is finished and normalisation is implemented and
verified. The notebook `fsoi_indicator_selection.ipynb` runs clean end to end; every change in this
session was checked with a full `jupyter nbconvert --execute` run. Outputs are cleared, so the file
sits at ~106 KB.

**The immediate next task is aggregation**, in this order:
1. Apply cost-direction flips (`1 − x` on the normalised columns) for water, waste, external input and
   land-use-fallow. These were deliberately NOT applied during normalisation so the `_norm` columns
   stay comparable and the flip stays visible.
2. Build the **five** category sub-indices as means of their member indicators (water and waste
   merged into one "municipal burden" category, 2026-09-22 — see "Category structure" in Part 1).
3. Equal-weight the categories into the composite.
4. Top/bottom cities, then the robustness checks.

**Superseded by 2026-09-22 decisions, kept for the reasoning trail:** the rest of this HANDOVER
section (written 2026-09-20) still describes a six-category structure and an unresolved external-input
question. Both are now resolved — see "Category structure (SETTLED 2026-09-22)" in Part 1.

**Build the index from the perHousehold columns only.** perArea is computed as a robustness track.
Never put both tracks in one aggregation — equal-weighting all 28 normalised columns would average
the two denominators by the back door, which is the collapse that was explicitly rejected.

**Three things that must not be re-derived from scratch** (all proven in the notebook's Diagnostics
section, all with live-computing cells):
- `perArea` is ~99% population density across cities, but is the *clean* track within a city over
  time; `perHousehold` is the reverse. They are contaminated in opposite dimensions.
- TÜİK's per-person water series sits on a *municipal* population base that Law 6360 moved in 2014.
  That is why the main panel's daily water series was dropped.
- Refined (*arıtılan*) water measures whether a treatment plant exists, not water use.

**Working practice this session settled on, worth keeping:** every analytical claim goes in the
notebook as a cell that *computes* its numbers. An earlier version of the Diagnostics cells had
results pasted in as hardcoded literals; Orhan caught it and it was rewritten. Don't restate
numbers computed elsewhere — compute them where they are shown.

**Open questions for Orhan are listed under "Open decisions" in Part 1 below.** The one that blocks
aggregation is how to join the two panels (question 1).

---

## Moved from Part 1 on 2026-09-24 (superseded by the denominator decomposition)

The perArea-tension paragraph, the raw-level household-count check, the waiver-
favouring mechanism reading and the 'map not built' note, as they stood before the
log-scale decomposition resolved or corrected each of them.

**⚠️ perArea tension, unresolved, flagged prominently rather than folded into the robustness
list:** perArea is the theoretically *cleaner* track for within-city DiD identification
(Diagnostic 6 — perHousehold's own denominator drifts within a city over time, perArea's
doesn't). Under perArea, **the DiD shows no significant effect at all, even with
municipal_burden included** (−0.0003, p = 0.949, vs. perHousehold's significant −0.037). This
is not just one more robustness check — it bears on whether the municipal_burden finding
should be trusted as real, not just on how large it is. Not resolved; a judgement call for
Orhan, not something a further test settles. Denominator-track Spearman correlations, for
reference: perArea vs. perHousehold 0.778; flat vs. category-weighted 0.681; TOPSIS vs.
category-weighted 0.917.

**Denominator jump check (2026-09-24, Orhan's suggestion) — the specific mechanical-artifact
hypothesis is not supported, the broader question stays open.** Tested whether
`Mean_Household_Count` (the perHousehold denominator) or `Mean_Household_Size` shows a
discontinuous jump at 2014, mirroring the mechanism already confirmed for the dropped
per-person water series. Same event-study design, applied to the denominator instead of the
numerator. **Neither variable jumps at 2014.** `Mean_Household_Count` diverges smoothly and
continuously across the *entire* 2008–2024 period, including *before* 2012 — an ordinary
secular urban-growth trend, not a reform-triggered break. `Mean_Household_Size` shows no
significant effect anywhere (all p > 0.15). This rules out the specific jump mechanism, not
the broader perArea/perHousehold tension — and surfaces a separate, lower-grade concern:
household count's pre-existing smooth divergence between treated and control is a mild
parallel-trends complication of its own (city FE absorb levels, not differential trends),
worth naming rather than folding into "ruled out."

**Mechanism (the tariff waiver vs. coverage-boundary expansion): now tested on two
variables, same shape both times.** Event-study on `municipal_burden` (waste) and, directly
(2026-09-24), on `water_drainage` itself (the variable the waiver actually targeted, via
Track C's extended panel to 2022): both show a sharp onset at 2014, a peak in 2018 (still
inside the 2014–2019 waiver), and a fade after 2019 (waste: −0.204→−0.148, 27%; water:
−0.190→−0.126, 34%). Onset alone can't distinguish the two mechanisms (both predict an
immediate 2014 jump); the fade favours the price-driven-waiver story, now corroborated on a
second variable, though the fade also coincides with COVID and this design can't separate
the two. Not settled — three explanations (boundary expansion, waiver, COVID) still sit on
this fade.

**Visualisations added 2026-09-24:** event-study charts (waste and water, with 95% CI bands
and the waiver window shaded), group-trend chart (with vs. without municipal_burden, against
the `Türkiye` reference line), and a top/bottom-10-cities chart. Consistent colour per
treatment group across all three. **A geographic map was discussed and deliberately not
built** — no province boundary/coordinate file exists in this repo (`geopandas` is
installed, but there's nothing to plot with it), and acquiring one is a new external data
dependency flagged to Orhan rather than added unprompted.

**What's still not done:** a direct significance test of the water_drainage waiver shape
(the event-study coefficients are reported, not formally tested against the "flat vs. fading"
alternatives); a wild cluster bootstrap for anything other than the primary category-weighted
spec; and the map, pending a decision on sourcing boundary data.

