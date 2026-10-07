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



---

## 2026-09-28 — notebook correction banners removed

Per Orhan, the markdown in `fsoi_indicator_selection.ipynb` and `fsoi_map.ipynb` now states
final positions only, and "Track C / Track A" became "full index / long-panel index" in all
visible text. The in-notebook "SUPERSEDED / CORRECTED" banners were deleted. The correction
trail they summarised is recorded in the sections above: the mechanism-check onset-vs-fade
reversal, the "no detectable effect" overclaim and its isolation-check fix, the TOPSIS
group-ranking correction, and the perArea tension resolved by the log decomposition.


---

# Archived 2026-10-05 — previous body of the main agent note

Moved here when the main note was rewritten as a single current-state document. Kept for
traceability only — **do not cite numbers from this section; use the main note.** Known to be
out of date below:
- Full-index (Track C) numbers before 2026-10-02 use the original 14-pair definition **with**
  animal-product value (e.g. 2020 group means 0.500 / 0.433 / 0.424, rank convergence 0.778,
  TOPSIS 2020 0.313 / 0.306 / 0.276, decline −0.021). Correct for that definition, superseded now.
- "New-metro lowest or tied-lowest in every view" — superseded: on the full index pooled
  2008–2020, old-metro is lowest under both weightings.
- Mean |skew| 3.25 → 1.81 and "14 of 28" — computed on all 28 columns; the index uses 26.
- Open items listed in the handoff and update sections — all closed by 2026-10-05.
- One table (winsorising schemes) contained wrong numbers and was deleted rather than archived.


# HANDOFF — session change 2026-09-28

Written by `thesis_log_econometrics_agent` at ~88% context, before Orhan starts a fresh session.
The incoming session is continuous with this one: same scope (`econometric_models_and_vars/`),
same open items. Per CLAUDE.md, notify `thesis_log_main_agent` when you pick this up.

**State at handoff.** Analysis is complete and verified. Orhan has started writing the
econometrics section. `fsoi_indicator_selection.ipynb` (168 cells) and `fsoi_map.ipynb` (13 cells)
both run clean end to end (0 errors, 4 figures each), with outputs cleared. Every number in the
summary below was checked against a fresh run on 2026-09-28. The history file is final.

**Open items (none blocking):**
1. **More maps.** Orhan said there may be a few more and will specify them. They go in
   `fsoi_map.ipynb`, which reads `fsoi_track_C/A_perHousehold.csv`. Re-run the main notebook
   first if the index changes, since its last cells export those CSVs.
2. **Wild cluster bootstrap for non-primary specifications** (flat, TOPSIS, waiver-excluded,
   per capita). It has been run only for the primary and size-matched specs. Optional; it won't
   change a conclusion.
3. **Requests from the writing strand** come relayed through `thesis_log_main_agent`. Confirm
   with Orhan in your own chat before acting on a second-hand request.

**Working habits that paid off here, keep them:**
- Compute every number in the cell that shows it; scan print strings for hard-typed literals.
- Verify before claiming: re-run, then read the output. Several of this strand's corrections came
  from re-checking its own earlier readings (raw-level vs log scale, normalised vs raw, mismatched
  objects in comparisons).
- Anchor-assert every scripted edit (exactly one match) and re-read a file before editing it.
  Other sessions edit shared files.
- Notebooks: edit through JSON scripts (the Read tool can't open the main notebook, it's too
  large), execute with `jupyter nbconvert --execute --inplace`, then clear outputs.

# Update 2026-10-01 (new session; notebook section "Further checks and thesis outputs")

New session took over 2026-10-01 (previous one is `_old_03`, agreed not to edit). Full re-run and
review of both notebooks: **0 errors, every headline number reproduced.** Main notebook now 179
cells, map notebook 15. Added cells, all computing in place:

1. **Wild cluster bootstrap for every spec** (Orhan approved): primary 0.004, size-matched 0.016,
   flat 0.002, TOPSIS 0.005, per capita 0.007, waiver-years-excluded **0.025** (asymptotic 0.042).
   6 of 6 significant. Open item 2 of the handoff is closed.
2. **Market currency check** (Orhan approved; result not yet reviewed with him).
   - **Coverage break in TÜİK provincial animal-product value:** the 81 provinces sum to the
     national total in 2008/2010 but only 38–60% of it from 2012 on. Crop and livestock value sum
     exactly, as do all other summable series. This break produces the 2010 "peak" in market.
   - Full-index decline 2008→2020: USD as built −0.021; USD without animal products −0.014;
     relative-to-national (currency- and inflation-free) −0.003; relative without animal products
     +0.004. **The decline is a national-level USD movement plus the series break, not provincial
     divergence.** National crop value 2012→2020: nominal TL 280, USD 77 (2012 = 100).
   - New-metro is lowest in 2020 under all four versions.
   - A real-terms TL version needs a price index that isn't in the repo.
3. **Data quality:** one-year spike scan. Animal products 26 cases in 2010 (= the break); fallow,
   greenhouse and agricultural electricity are noisy near zero; waste has 1 case (Kırıkkale 2012:
   128, 133, **41**, 74; Kırşehir 2012 **143** looks off too). Kırıkkale's fertiliser per household
   rises 6.5× 2008→2024. Hakkari's 2020–24 fertiliser is zero-filled. Dropping Kırıkkale,
   Kırşehir and Hakkari (all controls): DiD −0.0370 vs −0.0373. No effect on the causal result.
4. **Writing-strand answers:** r 0.988/0.048 = **drawn water**, Pearson, raw levels, pooled
   province-years n = 648 (2008–2022); waste gives 0.995/0.163. Greenhouse 85.3%/79.0% = share of
   **province-years** (n = 729) with normalised per-household value < 0.05. Exchange rates: the code
   uses a hand-typed table, one rate per year; it cannot verify the first/last-day derivation.
   Data appendix → `thesis_outputs/table_data_appendix_indicators.csv` (TÜİK columns asserted
   against the CSV header).
5. **Thesis figures** in `thesis_outputs/`: `fig_4_3_per_area_vs_per_household.png`,
   `fig_5_1_full_index_2020_map.png` (from `fsoi_map.ipynb`), `fig_5_2_group_means_over_time.png`.

**Second round, same day (cells "Chapter 6 outputs and the animal-product break"; 186 cells, 0
errors):**
- **Figures and tables:** Figure 6.1 (event study, long-panel index) with
  `table_6_1_event_study_long_panel.csv`; Figure 6.2 (log waste vs log coverage, coverage derived
  from water, said on the figure) with `table_6_2_...csv`.
- **Why the composite fades while log waste doesn't** (exact decomposition: the FSOI event
  coefficients equal the sum of the category contributions, asserted):
  - From 2014–18 to 2022–24 the composite moves +0.0117 toward zero (27%). Municipal burden alone
    contributes +0.0178; production and land use drift further negative (−0.0124); external input
    adds +0.0062.
  - Within municipal burden, the score effect fades 35% but log waste only 7% over those windows
    (3% if 2020 is included in the late window, as in the decomposition cell). The cause is that
    `log1p` is effectively linear at these units (max gap from x is 0.13%), and treated waste per
    household fell (0.00144 → 0.00118). The same percentage jump therefore becomes a smaller
    absolute score gap.
- **`log1p` is ~linear (Pearson > 0.99 with raw) for 14 of 28 normalised columns.** Skew is
  essentially unchanged for all the per-household land-use columns and for waste. The methods text
  must not claim the log step reduces skew across the board. Whether to change units or use
  `log(x)` is Orhan's call; it is rank-preserving either way.
- **Animal-product break:**
  - The PROVINCIAL series is the one that breaks. 2010→2012: national ×1.06 and live animals
    ×1.12, but the provincial sum ×0.41.
  - Lead (unverified on TÜİK itself): Kırklareli Governorate yearbook footnote, citing TÜİK, says
    that from 2011 animal-product value excludes red meat, white meat, eggs and hides.
  - The break is not uniform: per-province ratio p10 0.25 to p90 0.57. Hardest hit are poultry
    provinces (Bolu 0.05, Manisa 0.10, Sakarya 0.13, Bilecik, Balıkesir). Groups differ (Kruskal–
    Wallis p = 0.025): old-metro mean 0.36, new-metro 0.43, non-metro 0.46.
- **Figure 1 retitled** (it was the superseded "fade after 2019" reading).

**DECISION (Orhan, 2026-10-02): animal-product value DROPPED from the full index.** Market = crop
+ livestock value; full index = 13 indicator pairs. Animal products are still built and normalised
and appear only in the annex comparison cell at the end of the notebook. Full-index results now:
- 2020 group means: non 0.511 / old 0.446 / new 0.439 (was 0.500 / 0.433 / 0.424).
- Pooled 2008–2020, equal-weighted: non 0.521 / new 0.466 / old 0.462 (old lowest by 0.004, still a
  near-tie). TOPSIS 2020: old 0.322 / non 0.318 / new 0.289.
- Decline 2008→2020: −0.014 (was −0.021). C-vs-A rank convergence: mean ρ 0.761 (was 0.778).
- Descriptive LOCO gap shrink: 42% (was 38%).
- Province ranks agree 0.983–0.989 (Spearman) between the old and new definitions.
- **Long-panel index, the DiD and every bootstrap are unchanged** (the long-panel index never
  contained market).

**Appendix B and flat weighting on the rebuilt full index (2026-10-02; notebook 192 cells, 0 errors):**
- `thesis_outputs/table_B1_...csv` (with/without comparison) and `table_B2_animal_products_break.csv`.
- 2020 top-10 overlap between the definitions is 9/10 (Antalya in, Gümüşhane out); bottom-10 overlap
  is 10/10.
- Flat vs category-weighted full index: province ρ 0.934–0.952 by year, 0.953 pooled (vs 0.681 on the
  long-panel index); 2020 top-10 overlap 7/10. Non-metro highest and new-metro lowest in 2020 under
  both.
- **Qualifier:** pooled 2008–2020, old-metro is lowest under BOTH weightings (equal-weighted 0.462 vs
  new 0.466; flat 0.428 vs new 0.438). "New-metro lowest" holds for 2020 and the long-panel views,
  not for full-index pooled.

**DECISIONS (Orhan, 2026-10-05):**
- **Fertiliser stays per household**, zeros kept; Hakkari's top external-input score is treated as
  a real, discussable case, not a fix.
- **log1p kept**, described as: "log1p is applied; for indicators in small units it is close to
  linear, so for those the scaling is effectively min-max on winsorised raw values." Skew on the 26
  index columns: mean |skew| 3.07 → 1.87; near-linear (Pearson > 0.99) for 14 of 26 (8 of 13 per
  household).
- **9,999-draw bootstrap not needed:** the borderline p = 0.025 has Monte Carlo error of about ±0.005.

  Per-column table for the appendix: `thesis_outputs/table_B3_skew_by_indicator.csv` (26 rows).
  log1p does real work only where values are large (production, market, agricultural electricity,
  water per area); it is near-linear for every land-use column and for waste per household.
- **Attribution:** the 6360 critique was published by **ZMO** (Ziraat Mühendisleri Odası, a member
  chamber of TMMOB). Cite ZMO, not "TMMOB".

**Land-use zoom (2026-10-05, notebook 197 cells):**
- The −0.0226 category DiD splits exactly across its five indicators: fallow −0.0108 (about half;
  the only indicator significant alone, score p = 0.021), vegetables −0.0068, long-term crops
  −0.0039, greenhouse −0.0021, core cropland +0.0009 (null).
- On raw logs nothing is significant: fallow +26% (p = 0.31, 38 zero rows dropped), vegetables −11%
  (p = 0.24), core harvested area −3% (p = 0.67).
- Reading: no sign of farmland loss; a small, diffuse shift toward fallow and away from vegetables.
  Too weak to support the TMMOB argument on its own.

**Superseded, raised by Orhan 2026-10-02 and decided 2026-10-05 as above:**
- **Hakkari** is 14th of 81 in the 2020 full index on an external-input score of 0.999 (rank 1),
  built from zero-filled fertiliser years.
- Cost-framed external input per household rewards provinces with little agriculture.
- Candidate fixes: missing → NaN instead of 0; or fertiliser per km² of cultivated land.
- Also open: the `log1p` / units question, whether to decompose the land-use effect by indicator,
  and a 9,999-draw bootstrap for the borderline waiver-excluded spec.

**Correction to this note:** the "Winsorising: why 1st/99th" table below gives 74.6% (1/99) for
greenhouse output *per area*. The current notebook prints 49.4% for that indicator; 74.6% is
*waste* per area. The table is stale and mislabelled; the notebook cell "Choosing the winsorising
bounds" is authoritative.

**Still open:** more maps (Orhan: later, during writing); whether the thesis keeps animal products
in market given the break (Orhan's call); Figure 1's title in the main notebook still says "fade
after 2019", the superseded score-scale reading. Fine as a working figure, not for the thesis.

# Writing-ready summary (verified 2026-09-28)

Full end-to-end run of `fsoi_indicator_selection.ipynb` on 2026-09-28: **168 cells, 0 errors,
4 figures**; every number below is printed by a notebook cell. Details and caveats for each are
in Part 1; this is the map.

**Names used in the thesis:** Track C = **full index** (5 categories, 14 indicator pairs,
2008–2020); Track A = **long-panel index** (4 categories, 9 pairs, 2008–2024). Code keeps
`FSOI_C` / `FSOI_A`. Categories: production, municipal burden (water + waste), external input
(fertiliser + agricultural electricity), market, land use. Headline denominator: per household.

1. **Descriptive:** new-metropolitan provinces score lowest or tied-lowest in every view
   tried. Which of non-metro / old-metro leads depends on the aggregation method (equal-weighted
   sum: non-metro; TOPSIS: old-metro).
2. **Causal (long-panel, DiD):** −0.0373 (p = 0.003; wild-cluster bootstrap p = 0.004), carried
   entirely by municipal burden. Production: tight null, 95% CI [−0.022, +0.022]. Land use −0.023
   and external input +0.048: small, opposite, real.
   *Suggested thesis sentence (approved by Orhan, 2026-09-29):* "Because only 14 provinces are
   treated, conventional cluster-robust standard errors may overstate significance (Bertrand,
   Duflo & Mullainathan, 2004); inference is therefore confirmed with a wild cluster bootstrap
   with restricted residuals and Rademacher weights (Cameron, Gelbach & Miller, 2008), 999
   replications, which yields p = 0.004."
3. **Mechanism:** raw waste collected +30% in treated provinces, equal to the jump in municipal
   coverage (log DiD 0.260 vs 0.259). Law 6360's clearest footprint is the extension of municipal
   service coverage — not household burden, not food sovereignty.
4. **Robust to:** flat weighting, TOPSIS, waiver-years exclusion, per-capita denominator,
   size-matched controls (though no true size overlap exists).
5. **Does not replicate:** the provisional PDF's "national decline" — the long-panel index rises
   slightly with municipal burden included and is flat without it.
6. **Limitations to state:** three pre-treatment points; small population-growth differential;
   treated and control never overlap in size; normalised per-area is unusable for DiD (scale
   compression); water fades 23% in logs, so the tariff waiver remains possible for water only.

**Notebook text (2026-09-28, per Orhan):** both notebooks now say "full index" / "long-panel
index" in all visible text (markdown, printed output, plot titles, labels); code identifiers
are unchanged. Markdown states final positions only, with no correction narration. The full
trail of how each result was reached lives in `agent_note_econometrics_FSOI_history.md`.
This note still uses "Track C/A" in places; the mapping above applies.

**Two things never to re-derive:** (a) per area ≈ population density across cities but clean
within a city; per household the reverse — never combine them in one aggregation. (b) Every
claim is computed by the cell that shows it — no pasted numbers.

# PART 1 — CURRENT STATE (read this first)

*Structure of this file (reorganised 2026-09-19, per Orhan): **Part 1** is the live picture —
open decisions and the current variable inventory. **Part 2** is stable reference material that
is still true. **Part 3** is the dated process record, kept for traceability but not current.
When these disagree, Part 1 wins.*

## Where things stand (2026-09-19)

**Water is settled.** Refined (*arıtılan*) dropped — it records whether a treatment plant exists
(27/81 cities reported exactly zero in 2008, 9/81 by 2022; drawn water has 0 zeros in 648
city-years), so in a cost-framed category it would also point the wrong way. The main panel's
per-person daily series is dropped too: TÜİK computes it per person *in municipalities*, and Law
6360 moved that base for treated cities in 2014 (+0.226 vs −0.020 for non-metros), so it carried
the reform in its own denominator. **Water is now the extended panel's annual drawn series alone,
as a symmetric `water_drainage_perArea` / `water_drainage_perHousehold` pair.** This costs no
coverage — both series were missing exactly 2024 — and it restores the main panel to **zero gaps**.
Consequence: the main panel carries no water column; water sits in extended, as market already did.
**Terminology: always "refined", never "treated"** (collides with the `Treated` status variable).

**Process failure worth recording.** The first version of the Diagnostics cells contained numbers
computed in an external scratch script and pasted in as hardcoded literals, with a static
"CONFIRMED" string — the cells checked nothing and would have gone stale silently. Caught by Orhan,
2026-09-19. They now compute everything from `diagnostic_raw`, a snapshot taken before the raw
columns are dropped. Recomputed values matched. Both correlation heatmap cells were also deleted
outright (not just their outputs) since the printed table carries the same information.

**What `implied municipal population` is, and is not.** It inverts TÜİK's own published per-person
rate — `annual total ÷ (daily rate × 365)` — to recover the population base TÜİK used, then
expresses it as a share of provincial population. Validity checks pass: the share never exceeds
1.003 (0 of 648 values above 1.05), and pre-reform it reads sensibly as a municipal-population
share (non-metro 0.713, old-metro 0.888 — the more urbanised group is higher). **It says nothing
about tariffs, and nothing about informal or private water use** (wells, boreholes, irrigation
outside the municipal network), which sit outside both series entirely. Its usefulness as an
urbanisation control is limited to the pre-2014 period: after the reform, metros saturate at ~1.0
and it becomes purely a coverage indicator.

**Household-count algebra — a correction worth keeping.** `Mean_Household_Count ~
Mean_Household_Size` is only **−0.11** across the panel, not the ≈−0.99 the construction
`Count = Population / Size` suggests: population varies 214× across cities while household size
varies 3.4×, so Count tracks population (r = 0.992) and the inverse link is swamped. **But within a
single city over time it *is* ≈−0.99** (Konya −0.991, Şırnak −0.990, Çanakkale −0.987). That matters
because a DiD identifies off within-city variation, so the household-size trend is the dominant
driver of the denominator in exactly the dimension the estimate uses — which is why the
treated-vs-control household-size trend check mattered (gap −0.045, small; see Part 2 briefing).

**The per-capita equity objection, measured and accepted.** Spearman between perHousehold and
perCapita rankings: greenhouse output 0.996, crop production 0.965, harvested land 0.959 — but
**waste collected 0.640, water drawn 0.752**. So the objection has little force for land/production
indicators (where the household is anyway the farming unit) and real force for municipal-service
indicators, which are consumption quantities experienced per person. **Agreed with Orhan
(2026-09-19): keep perHousehold as the structural denominator and add a perCapita variant for
water/waste to the robustness-check list.** Implemented 2026-09-24 as a full per-capita
track; it replicates per household almost exactly (DiD −0.0369 vs −0.0373).

## Denominators: the two tracks are contaminated in opposite dimensions (2026-09-19/20)

The single most important structural fact for interpreting the index. `Area_km2` is **constant
within a city** (0 of 81 vary; merged from HGM on name with no year key). `Mean_Household_Count`
is **not** — households multiply as household size shrinks.

| | across cities (ranking) | within a city over time (DiD) |
|---|---|---|
| **perArea** | ≈ population density, r = **0.988** ✗ | pure numerator, r = **1.000** with the raw total (100% of cities) ✓ |
| **perHousehold** | free of density, r = **0.048** ✓ | drifts, r = **0.72** with the total (only 1% of cities above 0.99) ✗ |

Population density spans 288× across cities while the behaviour measured spans ~5×, which is why
perArea collapses onto density. Within a city, density barely moves (CV 0.046) — it separates
cities, not years.

**Which track for what.** In a DiD with city fixed effects, the between-city density that spoils
perArea is *absorbed* by the fixed effects, whereas perHousehold's within-city denominator drift is
*not* — so perArea is mechanically the cleaner causal track. But perArea is close to meaningless as
a published level (it would rank cities by density), and food sovereignty is a household-level
construct.

**Recommendation (revised 2026-09-20, supersedes an earlier lean toward perArea):** use
**perHousehold as the headline index** and perArea as the robustness track. The reason this is
affordable is that perHousehold's one weakness has been *measured* and is small — the treated-vs-
control differential in household-size trend is −0.045 on a base of ~3.2, about 1.4%. Taking the
mechanically-cleaner track at the cost of an uninterpretable headline number would be a bad trade.
**Settled with Orhan (2026-09-22): per household is the headline.**

**Never put both tracks into one aggregation.** Equal-weighting all 28 normalised columns together
would average the two tracks by the back door — the same collapse that was rejected explicitly
(Orhan spotted this, 2026-09-20). Each index is built from its own 14 columns.

## Normalisation implemented (2026-09-20)

`log1p` → winsorise (1st/99th) → pooled min-max, each indicator independently, raw columns kept and
normalised versions written with a `_norm` suffix. Thresholds computed from **cities only** (the
`Türkiye` aggregate is placed on the scale, not used to define it) and **pooled across 2008–2024**,
not per-year, so a score change means the city changed rather than its peers being different that
year. Cost-direction flips are deliberately deferred to aggregation (`1 − x`) so these columns stay
comparable and the flip stays visible.

- 28 indicators normalised (18 main, 10 extended). Verified: every `_norm` column lies in [0, 1],
  Spearman rank within each indicator is preserved (log1p and min-max are both monotonic), and NaN
  counts are unchanged.
- `log1p` applied to all 28 via `LOG1P_SKEW_THRESHOLD = 0.0`; raising that parameter switches to
  selective transformation. Uniform was chosen to avoid an arbitrary cutoff needing defence, and it
  is harmless since log1p is monotonic — it never reorders a city within an indicator, it only
  changes how much weight extremes carry when indicators are averaged. Mean |skew| fell 3.25 → 1.81
  *(all 28 columns incl. animal products — superseded 2026-10-05: on the 26 index columns it is
  3.07 → 1.87, and log1p is near-linear for 14 of them; see the Update 2026-10-01 section and
  `thesis_outputs/table_B3_skew_by_indicator.csv`)*.
- No indicator contains negative values, so log1p is safe throughout.

**Open issue found during normalisation — floor-bunching.** `log1p` cannot fix zero-inflation, and
four indicators still have most cities pressed against the floor: `landuse_greenhouse_km2_perHousehold`
85.3% below 0.05, `landuse_greenhouse_km2_perArea` 85.2%, `agro_greenhouse_prod_ton_perHousehold`
79.0%, `wasteCollected_1000ton_perArea` 74.6%. Greenhouse is genuinely concentrated (Antalya/Mersin)
and ~12% of city-years are exact zeros; waste-perArea is the density skew again (0% exact zeros).
Consequence: in an equal-weighted mean these contribute almost no discrimination — near-constants
plus a couple of outliers. Options: accept and document; widen `WINSOR_LIMITS` to (0.05, 0.95) to
spread the middle; or rank-normalise those indicators specifically. **Decided 2026-09-20: keep
1/99 and document it** (see "Winsorising: why 1st/99th").

## Variable selection is COMPLETE (2026-09-19)

All open variable decisions are resolved. Final list — 14 indicator pairs, every one a symmetric
`_perArea` + `_perHousehold` pair, 28 columns total. **Grouped into five categories, not six** — see
"Category structure (SETTLED 2026-09-22)" below for the current grouping; the table historically
shown here listed water and waste as separate categories, since merged.

Final resolutions (all per Orhan, 2026-09-19 unless noted):
- **Waste `_kg_daily` dropped**, both forms together (symmetry rule). The annual total already
  supplies waste; the daily derivation was 0.999-correlated with it in perArea form. Waste is now a
  single clean pair.
- **Greenhouse split rather than collapsed.** `agro_greenhouse_prod_ton_*` → production,
  `landuse_greenhouse_km2_*` → land-use. Its two inputs belonged to different categories, so a
  combined index belonged cleanly to neither and mixed tonnes with km². They keep their units.
  Consequence to note in the write-up: the two remain ~0.94 correlated, so greenhouse activity is
  reflected in two of the five categories — defensible (a greenhouse-heavy city genuinely has both
  more output and more land under glass) but worth stating rather than leaving implicit.
- **Water and waste are separate *indicators*, merged into one *category* (revised 2026-09-22).**
  At perHousehold they correlate only ~0.2 — correctly ruling out *indicator-level collapse* (folding
  them into one variable, the way harvested/sowed were collapsed below). That is a different question
  from *category-level grouping*: equal category weighting gave each of these two lone-indicator
  categories up to 5x the per-indicator weight of land-use's 5-indicator category, an artifact of how
  categories were carved rather than a judgement of importance. Grouping them as "municipal burden"
  fixes the weight without touching either indicator, and the category has a real construct behind
  it: both are municipal household services (not agricultural), both cost-framed, both inside the
  Law 6360 coverage confound. See "Category structure" below.
- **`landuse_core_*` remains the one collapsed indicator** (harvested ≈ sowed, r = 0.99 in *both*
  tracks — a genuine same-construct case, unlike the perArea-artifact ones).

**Structural fact to settle before construction: the categories do not span the same years.**
Main panel is gap-free 2008–2024. Extended is missing 2024 (water, agricultural electricity) and
2022 + 2024 (market). **Resolved 2026-09-21/22 — see "Two-track index structure" in Part 1.**

**Do not impute the missing years.** They are publication gaps, not random missingness, and
fabricating post-treatment observations is precisely where invented data does most damage in a
causal design. The main/extended split exists to quarantine them.

## Standing measurement concerns (not blocking, but must reach the thesis text)

- **Law 6360 boundary expansion (2026-09-19, the most serious one).** From 2014 metropolitan
  municipalities serve the whole province, so municipal-service statistics may cover populations
  they did not before. Waste per household shows a +19.7% treated-vs-control DiD gap and the annual
  water total +17.6%, while the per-person water rate moves −9.6% and a non-municipal control
  (harvested land) moves −21.4%. A coverage change explains that split (totals rise as territory
  grows; per-head rates fall as lower-usage rural population is absorbed). **Confirmed 2026-09-24:**
  the log DiD on waste collected (+0.260) equals the log DiD on municipal coverage (+0.259) — see
  "Correction 2 RESOLVED" below. Affects municipal burden (water and waste).
- **Law 6360 water-tariff waiver (2014–2019).** An open confound on water only — the earlier
  "volume, not price" dismissal was wrong (the variable is household drinking water, exactly what
  the waiver capped). In logs waste shows no waiver-shaped fade; water fades 23%. See Part 2.
- **perHousehold denominator and household size.** Safe against the non-metropolitan control (DiD
  gap −0.045 on a ~3.2 base) but drifts ~6% against old-metropolitan. Household size is a **west–east
  regional gradient, not a rural/urban one** (Şırnak 4.9 … Eskişehir 2.6, with urban and rural cities
  at both ends). Distributional consequence worth documenting: for equal per-capita resources, large
  household cities score *higher* on perHousehold benefit indicators and *worse* on cost-framed ones,
  so the bias does not run in one direction across categories.
- **perArea is largely a scale artifact.** `perArea = quantity / km²`, and city area is an
  administrative boundary varying ~50× that is unrelated to the indicator, so any two
  population-proportional quantities correlate at r > 0.95 in that form (water ~ waste: 0.977
  perArea vs 0.208 perHousehold). Tested and rejected the alternative explanation that
  industrialisation drives it — a non-agricultural-electricity proxy correlates only −0.27 with
  water per household, the wrong sign for that story. **A high perArea correlation is therefore weak
  evidence of redundancy; the perHousehold number is the informative one.**

## Current variable inventory (corrected 2026-09-21 — the 09-19 version was stale)

*The previous version of this section listed `greenhouse_intensity_*`, `waste_collected_kg_daily_*`,
`water_drainage_litre_daily_*`, `water_supply_perArea` and `water_refined_perHousehold`, all of
which were subsequently dropped or split. Verified against a live notebook run.*

**`data_official_Türkiye`** (main, 738 rows, 22 columns pre-normalisation, **no gaps**) — 9
indicator pairs, each with a `_perArea` and a `_perHousehold` form:
`agro_greenhouse_prod_ton_*`, `total_agro_production_ton_*`, `landuse_core_*`,
`landuse_fallow_km2_*`, `landuse_greenhouse_km2_*`, `landuse_longtermCrops_km2_*`,
`landuse_vegetables_km2_*`, `wasteCollected_1000ton_*`, `fertilizer_use_*`
— plus `Year`, `Location_Name`, `Treated`, `Treated_Label`.
Categories present here: production, land-use, municipal burden (waste only), external input (fertiliser only).

**`data_official_Türkiye_extended`** — 5 indicator pairs: `agro_crop_1000USD_*`,
`agro_livestock_1000USD_*`, `agro_animalproducts_1000USD_*`, `water_drainage_*`,
`electricity_agriculture_mwh_*` — plus raw source columns and denominators (`Area_km2`,
`Mean_Household_Count`, `Water_Drainage_1000m3PerYear`, `Water_Refined_1000m3PerYear`,
`Electric_Energy_Use_*`) and the `nonagri_electricity_mwh_perHousehold` covariate, which is a
control, **not** an FSOI indicator (it is excluded via `EXTENDED_EXCLUDE`).
Categories present here: market, municipal burden (water), external input (agricultural electricity).

14 indicator pairs in total, 28 columns. After the normalisation cell each also has a `_norm`
twin, so the notebook carries both raw and normalised values throughout.

## Winsorising: why 1st/99th, evidenced (2026-09-20)

Four schemes were priced against real indicators rather than assumed (notebook: "Choosing the
winsorising bounds"). On greenhouse output perArea, the worst-behaved indicator:

*[Table removed 2026-10-05: its numbers were wrong — the row labelled greenhouse output per area carried other figures. The notebook cell "Choosing the winsorising bounds" is authoritative.]*

5/95 fixes the floor-bunching but at an unacceptable price: Antalya, Mersin, Adana and Muğla all
collapse to exactly 1.000 in greenhouse — indistinguishable in the one category where they are the
entire story. Rank-normalisation separates them but discards magnitude (Antalya lands 0.010 above
Mersin despite producing far more), the wrong thing to throw away in an index about quantity of
production.

**1/99 stands, and the floor-bunching is documented rather than engineered away.** It is
substantively real — most Turkish provinces genuinely have negligible greenhouse agriculture. The
consequence to state in the thesis: an indicator where most cities sit near the floor contributes
little discrimination to an equal-weighted mean, so its practical weight is below its nominal share
of its category. A property to disclose, not a fault to fix.

## Control groups: which is clean, and for which variables (2026-09-20)

Reading the old-metropolitan coverage finding as a blanket disqualification would throw away a
useful comparison group. Precisely: Law 6360 extended metropolitan boundaries to the whole province
for **existing** metros as well as new ones. Implied municipal coverage across 2012→2014:
non-metropolitan **−0.020** (flat), new-metropolitan **+0.226**, old-metropolitan **+0.089**.

- **Municipal-service variables (water, waste): non-metropolitan is the only clean control.**
  Old-metros received a weaker version of the same boundary treatment, so a treated-vs-old-metro
  comparison understates the effect — both groups moved.
- **Non-municipal variables (land use, production, fertiliser): old-metropolitan remains usable.**
  Agricultural statistics are collected province-wide regardless of municipal status, so the
  boundary change does not mechanically move harvested hectares or crop tonnage. Evidence already
  in the notebook: the harvested-land control moved −21.4% across the reform, the *opposite*
  direction to the municipal services.

Keep all three groups, but state which control serves which category. Do not report a single
treated-vs-old-metro estimate across all five categories as though it were uniformly valid.

## The two Law 6360 confounds — see CLAUDE.md

Both confounds, the distinction between them, and the rule against stating the tariff-waiver
story as a finding are specified in `CLAUDE.md` → **Law 6360 confounds**. That is canonical;
it is not restated here, because a restatement is a future stale copy.

One operational consequence for this folder: the measurement confound was **resolved by
deletion** — `Water_Drainage_LitrePerPersonPerDay` is dropped and must not be re-added, since
its denominator is municipal population, which the reform moved in 2014. Water is carried by
the extended panel's annual drawn series instead.

## Exact year coverage per category (verified 2026-09-21)

City rows with data, by year — measured, not assumed:

| Year | main panel | water (drawn & refined) | external input (agri. elec.) | market |
|---|---|---|---|---|
| 2008–2020 | 81 | 81 | 81 | 81 |
| 2022 | 81 | 81 | 81 | **0** |
| 2024 | 81 | **0** | **0** | **0** |

**No water variable covers 2024 at all** — drawn and refined both stop at 2022. Water is therefore
2008–2022 (8 points), market is 2008–2020 (7 points), the main panel is complete 2008–2024.

**The binding constraint on the full index is MARKET, not water.** Market is the only
category missing 2022.

2020 is the only post-waiver observation *for the full index*, which market caps at 2020. Water
itself has **two** post-waiver points, **2020 and 2022** (the waiver ran 2014–2019).

**Practical consequence worth carrying into the next session:** the tariff-waiver question is a
*water* question and does not need the composite. It can be studied directly on the water series
across 2008–2022 with two post-waiver observations, independent of whatever is decided about
joining the panels. Don't let the composite's year constraint truncate that analysis.

## Category structure (SETTLED 2026-09-22) — five categories, not six

Water and waste, previously separate categories, are merged into one: **municipal burden**.
Both indicators are unchanged — this is category-level grouping (shared weight), not
indicator-level collapse (folding into one variable); see the "Variable selection is
COMPLETE" section above for why that distinction matters. Motivated by weight, not just
construct: equal category weighting means a lone-indicator category gets the same share as
a five-indicator category, so water and waste alone were each carrying up to 5x the
per-indicator weight of land-use. Grouping them is also independently motivated: both are
municipal household services (not agricultural), both cost-framed, both sit inside the same
Law 6360 coverage confound.

**Five categories:** production, municipal burden (water + waste), external input
(fertiliser + agricultural electricity), market, land-use.

**Market and production were considered for a similar merge and explicitly kept separate.**
Both measure output (value vs. tonnage) but market is extended-panel (caps 2020) and
production is main-panel (runs 2024) — merging them would strip track A of its only output
category.

## Two-track index structure (SETTLED with Orhan 2026-09-21/22)

Supersedes the former "Open decision — joining the two panels". There is **no single FSOI
series** — do not write as if there were. Both tracks run the *same* pipeline: same 28
normalised columns, same cost flips, same equal-weighted mean. They differ only in the
category list passed in and the years kept. One set of code, two runs.

| | Track C — the index | Track A — the estimator |
|---|---|---|
| Years | 2008–2020 (7 points, 3 pre / 4 post) | 2008–2024 (9 points, 3 pre / 6 post) |
| Categories | **5** — all | **4** — main panel only |
| Indicator pairs | 14 | 9 |
| Answers | *what* food sovereignty is and how it is distributed | *did Law 6360 change it* |
| Used for | levels, city rankings, distribution — the descriptive core | the DiD regression |

**Track A's four categories** are production, municipal burden (waste only — water is
extended-panel and drops out), external input (fertiliser only — see resolution below),
land-use. Market (3 pairs) drops entirely; it has no main-panel component to fall back on,
unlike municipal burden and external input.

**Why two tracks rather than one.** The index definition is a theoretical claim; the
estimator is an empirical one, and they need not be the same object. Track C is the FSOI *as
the literature review defines it* — five categories because that is what the framework
argues food sovereignty consists of. Letting TÜİK's publication schedule pick the categories
would make the construct an artifact of data availability. But C is a weak estimator: its
post-treatment years are 2014/2016/2018/2020 and 2020 is COVID, leaving effectively three
clean post-treatment points — not enough for an event study with credible leads and lags. A
has six.

**The 2020 cap is market alone.** Crop, livestock and animal-product value in USD are
unpublished by TÜİK for both 2022 and 2024. Water is a separate, later constraint (runs to
2022); the main panel is complete to 2024. Verified by counting city rows per year per
category (table above). **Not** the water measurement confound — that was a separate matter
and cost no years, both water series having been missing exactly 2024 anyway.

**The pre-period is identical in both tracks** (2008, 2010, 2012). Nothing in this structure
improves the pre-trend, and three pre-treatment points is thin either way — a limitation of
the panel, not of the track choice. State it as such.

**A five-category 2008–2022 middle track was considered and explicitly dropped** as an index.
Water is instead analysed to 2022 **at variable level** — which is where the tariff-waiver
question gets answered, with two post-waiver observations (2020, 2022) — not as a third
index. Don't let the composite's year limit truncate that analysis.

**RESOLVED 2026-09-22 — external input is option (a).** Fertiliser-only in track A, mean of
fertiliser + agricultural electricity in track C. Each track is internally consistent across
its own years, which is the property a DiD needs — but the between-track difference (A
measures fertiliser alone, C measures the mean of two indicators) is real and must be stated
in the write-up, not smoothed over. This is the same asymmetric pattern now also used for
municipal burden (waste-only in A, water+waste in C) — not a one-off special case.

**No remaining open items in the category/track structure.** Everything above is settled;
what's left is implementation (see below).

## Next implementation steps

1. ~~Resolve open decisions 1–6 above~~ — done; see "Category structure" and "Two-track
   index structure" above.
2. `log1p` skewed indicators, then normalise — **pooled 2008–2024 only, no per-year variant**
   (Orhan, 2026-09-17), winsorised min-max. **Done, verified 2026-09-20.**
3. ~~Aggregate into the five category sub-indices, applying cost-direction flips~~ — **done
   and executed clean, 2026-09-22.** Cost flips, `CATEGORY_MAP_C`/`CATEGORY_MAP_A`, and
   `build_fsoi()` are now in the notebook (after the normalisation-verification cell), and
   both `FSOI_C` (5 categories, 2008–2020, 574 rows) and `FSOI_A` (4 categories, 2008–2024,
   738 rows) are built, along with their `_perArea` robustness mirrors, top/bottom-city
   tables, and a Track C vs. Track A rank-convergence check. Verified with a full
   `jupyter nbconvert --execute` run, zero errors across 78 cells, then outputs cleared.
   **First descriptive result:** in Track C 2020, mean FSOI by group is non-metropolitan
   0.500, old-metropolitan 0.433, new-metropolitan 0.424 — non-metros score highest on the
   headline index. This is a plain group-mean comparison, not a DiD estimate; don't cite it
   as a treatment effect. **Convergence check:** Track C and Track A ranks agree at Spearman
   ρ = 0.72–0.83 across the seven shared years (mean 0.778) — same direction, not identical,
   so Track A's 2022/2024 extension is reasonably licensed but the two are not
   interchangeable; report both trend and the divergence, don't quietly pick one.

## Aggregation, DiD, and robustness — current state (as of 2026-09-24)

*The full blow-by-blow (every intermediate specification, every corrected conclusion, in the
order it happened) moved to `agent_note_econometrics_FSOI_history.md` on 2026-09-24 — read
there only to reconstruct how a number was found or to defend the process. What follows is
the current, settled picture, corrections already folded in rather than narrated.*

**Track A's DiD-ready structure is built and stress-tested more than any other part of this
pipeline:** flips, `CATEGORY_MAP_C`/`CATEGORY_MAP_A`, `build_fsoi()`, both tracks, top/bottom
cities, and a full DiD section, all executed clean in `fsoi_indicator_selection.ipynb`
(168 cells as of 2026-09-28, zero errors, outputs cleared).

**Descriptive result.** Under the primary aggregation (equal-weighted sum), non-metropolitan
cities score highest (Track C 2020: non-metro 0.500, old-metro 0.433, new-metro 0.424).
**This is robust to removing any single category** (municipal_burden, production, land_use,
external_input, or market — all five tested) **but not to changing the aggregation method**:
under TOPSIS on the same object (full index, 2020), old-metropolitan leads instead (old 0.313,
non 0.306, new 0.276). What holds in every view tried is that **new-metropolitan provinces
score lowest or tied-lowest** (the one tie: full index pooled 2008–2020, equal-weighted, old
0.451 vs new 0.453). Do not report "non-metro scores highest" as settled.

**Causal result (primary): −0.0373 (SE 0.0126, p = 0.0031, 95% CI [−0.062, −0.012])**,
two-way fixed effects, Track A, non-metropolitan-only control (old-metropolitan is a
contaminated control for a composite containing `municipal_burden`). Pre-trends clean on a
weak two-point test. Confirmed by wild cluster bootstrap (p = 0.0040 vs. asymptotic 0.0031 —
not a small-treated-cluster artifact, 14 treated cities).

**The entire significant effect is generated by `municipal_burden` (waste)** — without it,
the estimate flips to +0.0085 (p = 0.224). Confirmed under **four independent
specifications** (category-weighted primary, flat-weighted 1/9-per-indicator, TOPSIS,
waiver-years-excluded) — every one shows the same pattern: significant with
municipal_burden, null without it. **Refined by isolation (2026-09-24):** `production` is
genuinely null (p = 0.98) but `land_use` (−0.023, p = 0.003) and `external_input` (+0.048,
p = 0.004) each carry their own small, significant, partly-offsetting effect — an order of
magnitude below municipal_burden's own −0.175 (p < 0.0001). "No detectable effect outside
municipal_burden" should read "no *large* effect outside it; small, mostly-offsetting effects
exist in land-use and external-input."

**Correction 2 RESOLVED (2026-09-24) — the effect is real, and it is municipal coverage
expansion.** Settled by a DiD on logs of the raw quantities (notebook: "Denominator
decomposition"), where no normalisation can interfere and every denominator is additive:
- **Raw waste collected rose +0.260 log (~30%)** in new-metro vs non-metro cities
  (p < 0.0001). Per household +27%, per capita +23%, both significant. Under city FE, waste
  per area *is* raw waste — so perArea's raw signal is the largest of all.
- **The denominator is not the story:** household count +2% (p = 0.37), household size +3%
  (p = 0.21). The per-capita track replicates perHousehold almost exactly (−0.0369 vs −0.0373).
- **The perArea null was scale compression.** Pooled min-max on perArea is dominated by the
  288× cross-city density spread: only **0.9%** of the perArea waste score's variation is
  within-city (vs 34% perHousehold). Within-city SD 10.7× smaller; the `municipal_burden`
  coefficient 10.9× smaller — the ratios match. `municipal_burden` alone is still significant
  under perArea (−0.016, p < 0.001). **Normalised perArea is not a usable DiD track**;
  Diagnostic 6 holds for *raw* perArea, the pooled normalisation removes the advantage.
- **Waste = coverage, one-for-one.** Log DiD on waste (+0.260) equals the log DiD on the
  implied municipal coverage share (+0.259), ratio 1.00, same year-by-year path (flat pre,
  ~+0.25 from 2014 on). Independent series. **Waste per covered resident did not change** —
  municipalities started recording waste from ~30% more people. Same mechanism as
  confound (a), which removed the per-person water series; now found in waste's numerator.
- **Headline, as it now stands:** Law 6360's clearest statistical footprint is the extension
  of municipal service coverage — administrative reach, not household burden, not food
  sovereignty. Production: no effect. Land-use (−0.023) and external input (+0.048): small,
  opposite, real, replicated under per-capita.

**Two of my own earlier readings, corrected by the same decomposition:**
- The household-count "smooth divergence" (and the parallel-trends concern drawn from it)
  came from an event study in raw levels, where large cities growing at the same *percentage*
  still show a widening absolute gap. In logs household count shows no significant
  differential trend in any year (all p > 0.3). Population shows a small (~5%) differential,
  with one significant pre-period coefficient (2008: −0.027, p = 0.004) — minor.
- The waiver-favouring "fade" (27% waste / 34% water) was largely the normalised scale. In
  logs waste fades **3%** — a permanent level shift, which is what coverage expansion predicts
  — and water fades 23%. Water's residual over coverage can't be cleanly tested, because the
  coverage share is derived from the water total. **Waiver: possible for water, no longer
  supported by waste.**


**The original pre-rebuild "national decline, independent of Law 6360" finding does not
replicate.** Checked directly (pooled linear trend, city FE, all three real groups, plus the
`Türkiye` aggregate row on its own): with municipal_burden, the trend is **positive and
significant** (+0.00195/year, p < 0.0001) — an increase, not a decline. Without it: flat,
not significant. This is a fact about the rebuilt index, not a verdict on the old one — the
two use different, non-comparable variable sets and constructions, and this check can't say
why they disagree. Orhan confirmed 2026-09-24 the old index mixed perHousehold/per-capita
with weak weighting; the current perHousehold-headline, equal-weighted-primary track is the
chosen path and doesn't need reconciling with it further.

**Visualisations (2026-09-24).** In `fsoi_indicator_selection.ipynb`: event studies with
95% CI bands, group trends vs the `Türkiye` reference line, top/bottom-10 cities. **Maps are in
a separate notebook, `fsoi_map.ipynb`,** which reads `fsoi_track_C_perHousehold.csv` /
`fsoi_track_A_perHousehold.csv` (exported by the main notebook's last cells) rather than
rebuilding the index. Four maps: treatment groups; Track C 2020 choropleth with new-metro
outlined; the same scores as province-centroid points (marker shape = group); raw FSOI change
2012→2024 on a zero-centred diverging scale, captioned as descriptive-only. Boundaries: HDX
`cod-ab-tur` admin-1, original source **Harita Genel Müdürlüğü** (same agency as the area
data), CC BY-IGO; downloaded, simplified (0.01°) and cached to `geo/tur_admin1_simplified.geojson`
(0.37 MB) by code inside the notebook, so the provenance is in the repo. Province names are
matched on a Turkish-folded key and asserted 81/81 both ways — the source's `adm1_name` is
ASCII and its Turkish column carries a broken dotted-i.

**Size-matched control check (2026-09-26, Orhan-approved; question relayed from
writingdrafts).** Answers "aren't treated provinces just bigger?": control group limited to
the 14 largest non-metros by 2012 population. **No size overlap exists** — the largest
non-metro (Afyonkarahisar, 704k) is below the smallest treated (Ordu, 741k); the median gap
narrows from 3.02× to 1.76×. With 28 clusters instead of 65: DiD **−0.0351 (p = 0.013)**
vs −0.0373; SE +12%; wild bootstrap p = 0.016. Coverage decomposition holds (log waste
+0.283 vs coverage +0.266, ratio 1.06). The ~5% population differential does not shrink
(+0.071 vs +0.051); its 2008 pre-coefficient keeps its size (−0.029) but loses significance
(p = 0.060), mostly from fewer clusters. **Size alone doesn't produce the result**, but a
true size-overlapping control group can't be built here — state that plainly.

**Claims-ledger checks (2026-09-26, notebook cell "Claims-ledger checks").** Thesis naming:
Track C = "full index", Track A = "long-panel index".
- Production-alone DiD: −0.0002, 95% CI **[−0.0225, +0.0220]** — half-width 0.18 SD of the
  production score, ~8× smaller than the municipal_burden effect. A reasonably tight null.
- The two group-mean sets are **different objects from the same build, both current**:
  0.500/0.433/0.424 (non/old/new) = full index, **2020**, equal-weighted; 0.507/0.484/0.466
  (non/old/new) = long-panel index, **pooled 2008–2024**, equal-weighted; the TOPSIS
  0.366/0.336/0.322 = long-panel pooled, in **old/non/new** order. The 09-23 TOPSIS
  correction therefore compared a different object from Result 1. Re-run like-for-like on
  full index 2020: TOPSIS still puts old-metro ahead (0.313 vs non 0.306, new 0.276) — the
  correction stands, but the margin is small.
- **"New-metro lowest in every specification" needs a qualifier:** in the full index pooled
  2008–2020, equal-weighted, old-metro (0.451) sits just below new-metro (0.453) — a
  0.002 tie. New-metro is lowest in the other five views.
- municipal_burden 2020 group means 0.744/0.563/0.536 (non/old/new): still current.

**Still not done:** a wild cluster bootstrap for specifications other than the primary and
size-matched ones. Nothing else in this section is open.



---

# PART 2 — REFERENCE (stable)

## Standing limitation — Law 6360 water-tariff transitional waiver (2026-09-13; reasoning corrected 2026-09-21)

**The waiver.** Reported by `thesis_log_main_agent` from a SETA analysis (Çelikyay, 2014):
villages converted to *mahalle* status under Law 6360 received a 5-year transitional waiver,
**2014–2019** — no taxes, fees or participation shares collected, and drinking/usage water
tariffs capped at **25% of the lowest municipal tariff**. In this panel's biennial years that
window covers **2014, 2016 and 2018**.

**Why it matters here.** Water is cost/burden-framed ("lower is better", 2026-09-12). If
converted villages in treated cities had artificially suppressed water costs across three
post-treatment panel years, a treated-vs-control comparison on water could partly reflect the
waiver rather than anything about food sovereignty.

**CORRECTION (2026-09-21) — the previous dismissal of this confound does not hold.** The
position recorded here from 2026-09-17 was that the waiver was probably not a real confound,
because our water indicators sit on the *production-cost* side (how much a city draws to serve
agricultural and municipal need) rather than the *household-billing* side, and so would not be
price-elastic in the relevant sense. **That argument rests on a misreading of what the variable
measures.** The raw TÜİK source column is:

> `İçme ve kullanma suyu şebekesi ve arıtma tesisleri : Toplam çekilen su miktarı (1000 m³/yıl)`

— *drinking and utility water network and treatment facilities*. This is **municipal household
supply**. It contains no irrigation water and no agricultural abstraction. The waiver capped
**drinking and usage water tariffs** specifically. The indicator therefore measures the volume
of exactly the water whose price was capped: the same category, not a different one. There is no
production-side/billing-side separation to appeal to.

**What is actually still open.** The correction removes the *dismissal*, not the question. A
household tariff cap plausibly raises metered volume, but by how much — and whether detectably
against a coverage change landing in the same year — is unmeasured. Two mechanisms remain, and
neither was ever addressed by the production-side argument:
- **Behavioural** — cheaper water, more use.
- **Metering/reporting** — a municipality not billing a waived village may meter and report it
  less diligently, biasing measured volume regardless of actual use.

**Working rule.** Treat the waiver as an **open, unquantified confound on the water category**,
not a dismissed one. Water can still proceed (it is not a hard blocker on the category or the
DiD), but thesis text must not assert that the waiver is irrelevant because the indicators are
production-side — that sentence is wrong and would not survive a reader who checks the source
column. See also `CLAUDE.md` → Law 6360 confounds (b), which carries the same correction.

**This is testable without the composite.** Water runs to **2022** with two post-waiver
observations (2020, 2022); only market caps the full index at 2020.

**Update (2026-09-24, log decomposition).** Waste tracks municipal coverage one-for-one and fades
only 3% after 2019 — no waiver signature. Water fades 23% in logs, so the waiver stays possible
for water specifically; water's residual over coverage can't be tested cleanly because the
coverage share is itself derived from the water total.

**Method note worth keeping:** this error was found by reading the raw source column instead of
reasoning from the variable's name. The same check settled the category question the same day
(water is municipal, so it is not an off-farm agricultural input). Check the source column.

## Briefing for Orhan — household vs. per-capita denomination (2026-09-18)

Orhan asked for a critical check on his own long-standing pipeline choice: every `_perHousehold`
indicator in this pipeline is `Total / Mean_Household_Count`, never `Total / Population_Total`
(per-capita). Requested as an explicit, attributed briefing, not just a passing chat answer — so
recorded here in full.

**Why household-based denomination is a reasonable, defensible choice:**
1. **Theoretical fit.** This project's own lit-review framing of food sovereignty centers
   household/family-level provisioning capacity and burden (land access, water/waste burden), as
   distinct from GFSI's more atomized per-capita "consumer" framing — household denomination
   matches FSOI's own theoretical stance better than per-capita would.
2. **Internal consistency.** Essentially every indicator in both dataframes already uses
   `Mean_Household_Count`; switching to per-capita for isolated variables would break the
   composite's internal uniformity for no clear gain.
3. **Practical/behavioral fit.** Many of the underlying burdens (a water bill, a waste bin, a
   farm plot) are organized at the household level, not the individual level, so dividing by
   household count can be more behaviorally meaningful than dividing by raw headcount.

**Where the choice carries real risk — the actual critique, not just validation:**
1. **Compositional confound risk for the DiD (the important one).** `Mean_Household_Count` is
   derived as `Population_Total / Mean_Household_Size`, and `Mean_Household_Size` is not constant
   across cities or years. If average household size changed *differently* between treated and
   control cities after 2012 (e.g. from migration or demographic shifts tied to the metro-status
   change itself), every `_perHousehold` indicator would partly reflect that compositional shift
   rather than a real change in burden/capacity — structurally the same *kind* of risk as the
   Law 6360 water-tariff-waiver flag above: plausible, not yet checked, checkable in principle
   (compare `Mean_Household_Size` trends by `Treated` group over 2008–2024). **Done 2026-09-24:**
   household size shows no differential trend (log DiD +0.029, p = 0.21; event study p > 0.15 in
   every year).
2. **Derived, not primary, denominator.** `Mean_Household_Count` is itself computed from an
   averaged, estimated figure (`Mean_Household_Size`), while `Population_Total` is a more directly
   measured administrative count (TÜİK/ADNKS). Every `_perHousehold` indicator inherits whatever
   estimation noise sits in `Mean_Household_Size`, on top of the underlying indicator's own noise
   — a per-capita denominator would avoid this extra layer. **Checked 2026-09-24:** the
   per-capita track replicates per household almost exactly.
3. ~~**Comparability to GFSI.**~~ **Withdrawn (Orhan, 2026-09-18)** — this critique point doesn't
   apply. FSOI is never numerically compared to GFSI in the first place: FSOI is city-level, GFSI is
   national-level, so the comparison is at the level of **categories and construct framing**, not
   numbers. The denominator choice therefore has no bearing on GFSI comparability. Left here rather
   than deleted so the reasoning trail stays visible.

**Bottom line:** the choice is defensible and consistent, not an error — but it's a choice, not a
neutral default, and a reviewer could reasonably ask why. Both empirical checks above have
now been run and neither changes the result.

# FSOI Working Dataframes: Variable Split

`fsoi_indicator_selection.ipynb` builds two separate city-year panels rather than one. This
note documents why, and exactly which variables live where, so the split doesn't need to be
re-derived from the notebook each time.

## Why two dataframes

TÜİK has not published municipal-level agricultural production *value* (crop/livestock/animal
products, in TL) for 2022 or 2024 yet, and municipal water/agricultural-electricity stats are
missing for 2024. Rather than carry `NaN`s for those years into the main FSOI panel, these
indicators are kept in a separate dataframe and analysed on their own — this maps onto the
Economic conditions / Ecological conditions categories from the literature review (see
`Variable_Analysis_Methods/variables_agrolife_econometrics.md`).

## Shared columns

`Year`, `Location_Name`, `Treated`, `Treated_Label` — identical values in both dataframes by
design, so either can be grouped/filtered on `Treated` without a join. No other column names
overlap.

## `Treated`

`pandas.Categorical`, ordered, four-valued:

| Value | `Treated_Label` | Meaning |
|---|---|---|
| 0 | Non-metropolitan | Non-metropolitan city |
| 1 | New-metropolitan (2012) | Became metropolitan via Law No. 6360 (2012) |
| 2 | Old-metropolitan | Already metropolitan before 2012 |
| 3 | Türkiye | The national-aggregate row, not a real city |

There are 81 real cities + 1 `Türkiye` aggregate row = 82 `Location_Name` values, matching the
panel's `82 locations × 9 years = 738 rows`.

`Treated` is kept as the numeric-coded categorical (0/1/2/3) for logic/filtering; `Treated_Label`
carries the same information as readable strings so plots (matplotlib/seaborn `hue`/legend) show
"Non-metropolitan" etc. automatically — no manual legend needed.

## New Data — Fertilizer Use (added 2026-09-12)

**Source:** `TOB_fertilizer_cities.xlsx` (Ministry of Agriculture and Forestry, TOB), sheet
`BİTKİ BESİN MADDESİ TÜKETİMİ` — total plant-nutrient/fertilizer consumption per city per year,
in tons, 2000–2025. 81 cities, zero missing values in the raw file overall — actually more
complete than several existing TÜİK-sourced indicators. Loaded and merged directly into
**`data_official_Türkiye` (main)**, not extended — this indicator has no TÜİK-style publication
gap, so the full-coverage dataframe is the right home for it, not the partial-coverage one.

**City-name matching:** the source file uses ALL-CAPS Turkish city names (`AFYONKARAHİSAR`,
`ADIYAMAN`); Python's default `.upper()`/`.lower()`/`.title()` mishandle Turkish's two distinct
"I"s (dotted İ/i vs. dotless I/ı — e.g. `"I".lower()` gives `"i"` in Python, but Turkish
requires `"ı"`), so a custom `tr_title()` function does the case-folding explicitly via
`str.maketrans({'İ': 'i', 'I': 'ı'})` before re-capitalizing. Verified against the panel's full
81-city set before merging — exact match, zero unmatched names either direction (only
`Türkiye`, the aggregate row, is absent from the fertilizer file, as expected). The merge cell
asserts both this match and the absence of duplicate Year/Location_Name rows, so a future
change to the source file that breaks either assumption fails loudly rather than silently
producing wrong values.

**Known gap:** `Hakkari` has no fertilizer records at all for 2020, 2022, or 2024 in the source
file (3 of 738 city-years, 0.4%) — confirmed as a genuine source-data gap (the other analysis
years for Hakkari are present, including legitimate zeros in 2012/2014/2016), not a
name-matching or merge bug. Small enough not to need a decision now, but don't be surprised by
those 3 `NaN`s downstream.

**New columns:** `fertilizer_use_perArea`, `fertilizer_use_perHousehold` — folded into the
**external input** category as a **cost** indicator, per Yilmaz (2025)'s Entropy-TOPSIS precedent
treating Fertilizer Intensity as a cost criterion, and per the cost/burden framing decided for
the rest of external input/water/waste (2026-09-12, see Status section above). `data_official_Türkiye`
is now `(738, 26)`.

## Composite Index Construction — Continuity Note (2026-09-11)

Written because Orhan flagged this session's context is getting large. This section is the
single place to catch up on the composite-index-methodology discussion without re-reading the
whole conversation — read this before anything else if picking this up fresh.

### Reference literature — now the working methodological anchors

- **Yilmaz (2025), "Provincial Agricultural Performance in Türkiye: An Integrated Entropy–TOPSIS
  Approach"** (*Int. J. Agric. Environ. Food Sci.* 9(4)). Entropy method for objective,
  data-driven criterion weights (more cross-provincial variability → higher weight); TOPSIS for
  ranking via distance to an ideal/negative-ideal solution. Two *different* normalizations are
  used at different steps: min-max (for the entropy weight calculation) and vector normalization
  `x/√Σx²` (for the TOPSIS distance calculation itself) — don't conflate the two if implementing
  TOPSIS. Uses **ratio/proportional criteria** (e.g. GDP/Area), explicitly rejecting raw absolute
  values as "not a direct performance criterion... misleading due to structural disparities" —
  this validates the pipeline's existing `_perArea`/`_perHousehold` design. Notably keeps two
  criteria correlated at r=0.97 on purpose, since they're theoretically distinct constructs
  (economic output vs. an environmental-pressure criterion) — correlation alone isn't automatic
  grounds for collapsing if the two things mean different things; this doesn't override the
  near-tautological pairs we're collapsing (harvested≈sowed is the same land measured twice) but
  is worth citing if a future collapse decision needs defending on theoretical grounds instead.
  Weights and rankings computed **separately per year**, with year-over-year comparison done via
  **rank change**, not raw score change — doesn't fit our DiD need (see normalization below).

- **Economist Impact (2022), "Global Food Security Index 2022"** (GFSI). 113 countries, 4
  pillars (affordability, availability, quality & safety, sustainability & adaptation), 68
  indicators, hierarchical structure: indicator → composite indicator → pillar → overall score
  (0–100) — directly analogous to our indicator → category sub-index → FSOI structure, five
  categories instead of four pillars. Two weighting options offered: **neutral (equal) weights**
  and **expert-panel-averaged weights** — validates Orhan's "equal weights for categories"
  preference as a standard, legitimate option, not a shortcut. **Normalization: min-max with
  fixed upper/lower thresholds applied identically across all years 2012–2022**, explicitly
  so "data outliers do not skew the scores" and "scores can be compared directly across years" —
  this is the precedent for the pooled-normalization approach recommended below, and it's a
  closer methodological fit to our DiD need than the Entropy-TOPSIS paper's per-year approach.
  Every one of GFSI's 68 indicators has a documented one-line "indicator rationale" — the
  convention to copy for our own indicator documentation (in-notebook comments + agent note).

- **Positioning FSOI relative to GFSI** (Orhan, 2026-09-11): **the FSOI is a critical comparative
  index to GFSI.** GFSI operationalizes food *security* — nationally aggregated, expert/
  institutionally weighted, oriented around affordability/availability/safety/adaptation as
  experienced by consumers and national systems. FSOI operationalizes food *sovereignty* — a
  city-level, producer/land-access-oriented framework grounded in the lit-review's own critique
  (`Variable_Analysis_Methods/variables_agrolife_econometrics.md`) that mainstream food-security
  indices reduce sovereignty concerns to minor consumption proxies rather than prioritizing them.
  Worth stating this explicitly and early in the thesis methodology section, not just implicitly
  through variable choice.

### Resolved — benefit/cost direction and aggregation method (2026-09-12)

Both decided by Orhan on 2026-09-12, superseding the "build both and compare" open item below
(kept for its reasoning/table, but no longer the live plan):

- **Cost/burden framing** for water, waste, external input, and land-use fallow — the primary model
  treats "lower is better" for all four. Fertilizer (new indicator, folded into external input) uses
  this same framing by construction.
- **Equal-weighted sum is the primary aggregation method**, not TOPSIS.

**Comparison scope — not 4 co-equal models.** A full 2×2 factorial (direction × aggregation)
produces 4 composite variants, but running all 4 as equally-weighted headline results would
read as indecisive in the thesis. Structure instead: **one primary specification** (equal
weight + cost framing, decided above) reported as the main FSOI result, with the other 3
cells of the 2×2 grid (TOPSIS+cost, equal-weight+benefit, TOPSIS+benefit) reported as
**appendix-level robustness/sensitivity checks** — do the rankings and the Law 6360 DiD
result hold up across all 4, or does methodology choice change the substantive conclusion?
Either answer is a reportable finding; treat it as a sensitivity analysis, not four parallel
theses.

### Cross-strand note — political category — see CLAUDE.md

The decision that FSOI adds **no seventh category** for political commitment, and that GFSI's
"political commitment to adaptation" pillar is approximated for discussion only by combining
`resmi_gazete/` and `agro_ministry_news/` (both national-level, so modelled as uniform across
cities in a year), is specified in `CLAUDE.md` → **FSOI vs. GFSI — political commitment**,
together with the caveats that must accompany it. Canonical there; not restated here.

## Coordination and scope — see CLAUDE.md

This folder's agent is `thesis_log_econometrics_agent`: full read/write in
`econometric_models_and_vars`, read-only elsewhere, never edits `CLAUDE.md`. Everything else
— the messaging protocol, relay titling, `ListAgents` staleness, the no-commits rule, and the
handover convention — is specified in `CLAUDE.md` → **Multi-Agent Coordination**, which is
canonical. Previously restated here in full; replaced with this pointer 2026-09-21, because a
restatement drifts and a pointer cannot.

---

# PART 3 — PROCESS HISTORY (moved out 2026-09-21)

The dated process record now lives in **`agent_note_econometrics_FSOI_history.md`** in this
folder. It was split out so a fresh session doesn't load it by default — it is traceability
material (how each decision was reached, which variable was dropped and why), not working
state. Read it when defending a methods choice or reconstructing why something was dropped;
otherwise Part 1 is what you need. Nothing was deleted in the split.
