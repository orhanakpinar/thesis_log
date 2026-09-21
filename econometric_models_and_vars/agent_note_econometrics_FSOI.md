> **Agent note.** Written by a Claude Code sub-agent operating on this folder
> (`econometric_models_and_vars`), documenting pipeline structure it implemented in
> `fsoi_indicator_selection.ipynb`. This is a technical record, not analysis or thesis prose —
> review before citing or incorporating into the written thesis. Human draft notes live in
> `Variable_Analysis_Methods/`.


---

# HANDOVER — session change 2026-09-20

Written by `thesis_log_econometrics_agent` before Orhan starts a fresh session. Treat the incoming
session as continuous with this one: same scope (`econometric_models_and_vars/`), same open items.
`thesis_log_main_agent` has been notified.

**Where the work stands.** Variable selection is finished and normalisation is implemented and
verified. The notebook `fsoi_indicator_selection.ipynb` runs clean end to end; every change in this
session was checked with a full `jupyter nbconvert --execute` run. Outputs are cleared, so the file
sits at ~106 KB.

**The immediate next task is aggregation**, in this order:
1. Apply cost-direction flips (`1 − x` on the normalised columns) for water, waste, energy and
   land-use-fallow. These were deliberately NOT applied during normalisation so the `_norm` columns
   stay comparable and the flip stays visible.
2. Build the six category sub-indices as means of their member indicators.
3. Equal-weight the categories into the composite.
4. Top/bottom cities, then the robustness checks.

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
water/waste to the robustness-check list.** Not implemented — it is a post-composite step.

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
Not finally decided; Orhan's call at aggregation.

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
  changes how much weight extremes carry when indicators are averaged. Mean |skew| fell 3.25 → 1.81.
- No indicator contains negative values, so log1p is safe throughout.

**Open issue found during normalisation — floor-bunching.** `log1p` cannot fix zero-inflation, and
four indicators still have most cities pressed against the floor: `landuse_greenhouse_km2_perHousehold`
85.3% below 0.05, `landuse_greenhouse_km2_perArea` 85.2%, `agro_greenhouse_prod_ton_perHousehold`
79.0%, `wasteCollected_1000ton_perArea` 74.6%. Greenhouse is genuinely concentrated (Antalya/Mersin)
and ~12% of city-years are exact zeros; waste-perArea is the density skew again (0% exact zeros).
Consequence: in an equal-weighted mean these contribute almost no discrimination — near-constants
plus a couple of outliers. Options: accept and document; widen `WINSOR_LIMITS` to (0.05, 0.95) to
spread the middle; or rank-normalise those indicators specifically. **Not decided — needs Orhan.**

## Variable selection is COMPLETE (2026-09-19)

All open variable decisions are resolved. Final list — 14 indicator pairs, every one a symmetric
`_perArea` + `_perHousehold` pair, 28 columns total, all six categories populated:

| Category | Indicators | Panel |
|---|---|---|
| market | `agro_crop_1000USD_*`, `agro_livestock_1000USD_*`, `agro_animalproducts_1000USD_*` | extended |
| production | `total_agro_production_ton_*`, `agro_greenhouse_prod_ton_*` | main |
| water | `water_drainage_*` | extended |
| waste | `wasteCollected_1000ton_*` | main |
| energy | `fertilizer_use_*` (main), `electricity_agriculture_mwh_*` (extended) | split |
| land-use | `landuse_core_*`, `landuse_fallow_km2_*`, `landuse_greenhouse_km2_*`, `landuse_longtermCrops_km2_*`, `landuse_vegetables_km2_*` | main |

Final resolutions (all per Orhan, 2026-09-19):
- **Waste `_kg_daily` dropped**, both forms together (symmetry rule). The annual total already
  supplies waste; the daily derivation was 0.999-correlated with it in perArea form. Waste is now a
  single clean pair.
- **Greenhouse split rather than collapsed.** `agro_greenhouse_prod_ton_*` → production,
  `landuse_greenhouse_km2_*` → land-use. Its two inputs belonged to different categories, so a
  combined index belonged cleanly to neither and mixed tonnes with km². They keep their units.
  Consequence to note in the write-up: the two remain ~0.94 correlated, so greenhouse activity is
  reflected in two of six categories — defensible (a greenhouse-heavy city genuinely has both more
  output and more land under glass) but worth stating rather than leaving implicit.
- **Water/waste stay separate categories.** At perHousehold they correlate only ~0.2, so there is no
  statistical case for merging; the shared municipal-coverage confound is handled as a confound, not
  by merging.
- **`landuse_core_*` remains the one collapsed indicator** (harvested ≈ sowed, r = 0.99 in *both*
  tracks — a genuine same-construct case, unlike the perArea-artifact ones).

**Structural fact to settle before construction: the six categories do not span the same years.**
Main panel is gap-free 2008–2024. Extended is missing 2024 (water, agricultural electricity) and
2022 + 2024 (market). So a complete six-category FSOI exists only for **2008–2020** — 7 biennial
points, 3 pre-treatment and 4 post. Options: build the headline index on 2008–2020, or report a
reduced-category index for 2022/2024 alongside it. Not yet decided.

**Do not impute the missing years.** They are publication gaps, not random missingness, and
fabricating post-treatment observations is precisely where invented data does most damage in a
causal design. The main/extended split exists to quarantine them.

## Standing measurement concerns (not blocking, but must reach the thesis text)

- **Law 6360 boundary expansion (2026-09-19, the most serious one).** From 2014 metropolitan
  municipalities serve the whole province, so municipal-service statistics may cover populations
  they did not before. Waste per household shows a +19.7% treated-vs-control DiD gap and the annual
  water total +17.6%, while the per-person water rate moves −9.6% and a non-municipal control
  (harvested land) moves −21.4%. A coverage change explains that split (totals rise as territory
  grows; per-head rates fall as lower-usage rural population is absorbed). Plausible, not proven —
  a real treatment effect could produce part of the same pattern. Affects water, waste and possibly
  energy, i.e. three of the six categories. **A ratio of two municipal statistics is immune to
  this** (treatment coverage shows a DiD gap of only +0.003), which is one possible mitigation.
- **Law 6360 water-tariff waiver (2014–2019).** Working position: probably not a confound, since
  our indicators measure volume rather than price. Reasoning and caveats in Part 2.
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
Categories present here: production, land-use, waste, energy (fertiliser only).

**`data_official_Türkiye_extended`** — 5 indicator pairs: `agro_crop_1000USD_*`,
`agro_livestock_1000USD_*`, `agro_animalproducts_1000USD_*`, `water_drainage_*`,
`electricity_agriculture_mwh_*` — plus raw source columns and denominators (`Area_km2`,
`Mean_Household_Count`, `Water_Drainage_1000m3PerYear`, `Water_Refined_1000m3PerYear`,
`Electric_Energy_Use_*`) and the `nonagri_electricity_mwh_perHousehold` covariate, which is a
control, **not** an FSOI indicator (it is excluded via `EXTENDED_EXCLUDE`).
Categories present here: market, water, energy (agricultural electricity).

14 indicator pairs in total, 28 columns. After the normalisation cell each also has a `_norm`
twin, so the notebook carries both raw and normalised values throughout.

## Winsorising: why 1st/99th, evidenced (2026-09-20)

Four schemes were priced against real indicators rather than assumed (notebook: "Choosing the
winsorising bounds"). On greenhouse output perArea, the worst-behaved indicator:

| scheme | % below 0.05 | % at exactly 0 | % at exactly 1 | IQR |
|---|---|---|---|---|
| none | 79.1 | 0.1 | 0.1 | 0.033 |
| **1/99 (chosen)** | 74.6 | 1.1 | 1.1 | 0.039 |
| 5/95 | 22.5 | 5.1 | 5.1 | 0.268 |
| rank | 4.9 | 0.0 | 0.1 | 0.500 |

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
treated-vs-old-metro estimate across all six categories as though it were uniformly valid.

## The two Law 6360 confounds are different things — don't merge them

- **(a) Measurement confound — municipal coverage.** TÜİK's per-person water figure divides by
  *municipal* population, and the reform moved that denominator. About **how the number was
  recorded**, not behaviour. **Resolved by deletion** — series dropped; do not re-add.
- **(b) Behavioural confound — the tariff waiver.** Converted villages paid no fees and had capped
  water tariffs 2014–2019. About **what people actually did**. **Not resolvable with this data** —
  informal and private water use is invisible in both TÜİK series. Described only.

**Must not be stated as a finding:** that the waiver's end caused water use to fall. The defensible
sentence is that treated cities' water use rose after the reform and fell after the waiver ended
while controls stayed flat; that this is *consistent with* the waiver having suppressed costs in
2014–2019; and that it is equally consistent with the initial coverage effect fading — with 2020
being the COVID year and only two observations following the waiver.

## Exact year coverage per category (verified 2026-09-21)

City rows with data, by year — measured, not assumed:

| Year | main panel | water (drawn & refined) | energy (agri. elec.) | market |
|---|---|---|---|---|
| 2008–2020 | 81 | 81 | 81 | 81 |
| 2022 | 81 | 81 | 81 | **0** |
| 2024 | 81 | **0** | **0** | **0** |

**No water variable covers 2024 at all** — drawn and refined both stop at 2022. Water is therefore
2008–2022 (8 points), market is 2008–2020 (7 points), the main panel is complete 2008–2024.

**The binding constraint on a six-category index is MARKET, not water.** Market is the only
category missing 2022.

**Correction to an earlier statement in this file and in conversation:** it was said that 2020
would be "the only post-waiver observation". That is true *only of the six-category composite*,
which market caps at 2020. It is not true of water itself, which has **two** post-waiver points,
**2020 and 2022** (the waiver ran 2014–2019).

**Practical consequence worth carrying into the next session:** the tariff-waiver question is a
*water* question and does not need the composite. It can be studied directly on the water series
across 2008–2022 with two post-waiver observations, independent of whatever is decided about
joining the panels. Don't let the composite's year constraint truncate that analysis.

## Open decision — joining the two panels (blocks aggregation)

The merge is trivial (`Year` + `Location_Name`); the question is the years extended does not cover.
Main is complete 2008–2024; extended is missing 2024 (water, agricultural electricity) and
2022 + 2024 (market).

- **(a) Six-category index, 2008–2020** — 7 points, 3 pre / 4 post. The FSOI as defined, consistent
  throughout, which is what the DiD needs. *Recommended headline.* Cost: 2020 is the only
  post-waiver observation.
- **(b) (a) plus a four-category index for 2008–2024** (main panel only: production, land-use,
  waste, energy-fertiliser), labelled a **coverage-extension robustness check**, not a rival index.
  Buys 6 post-treatment periods and the post-waiver window. Note it also happens to exclude water,
  the category most affected by the measurement confound.
- **(c) Average whatever categories exist each year.** *Advise against* — the index would change
  definition mid-panel, and the change lands post-treatment, so composition drift could be
  mistaken for a treatment effect.

Whichever is chosen, report the extended-only categories (market, water) separately for the years
they exist rather than letting them vanish silently.

## Next implementation steps

1. Resolve open decisions 1–6 above (all are variable-selection, not construction).
2. `log1p` skewed indicators, then normalise — **pooled 2008–2024 only, no per-year variant**
   (Orhan, 2026-09-17), winsorised min-max.
3. Aggregate into the six category sub-indices, applying cost-direction flips.
4. Produce the primary FSOI composite (equal weight, cost-framed) + top/bottom cities.
5. Robustness checks: TOPSIS vs. equal weight; benefit vs. cost framing; waiver-years exclusion;
   **leave-one-category-out** (6 reruns, not per-variable — that would be excessive and harder to
   interpret).
6. Report the composite to `thesis_log_main_agent` — that is the trigger for its CLAUDE.md
   Results-status update.

---

# PART 2 — REFERENCE (stable)

## Standing limitation — Law 6360 water-tariff transitional waiver (2026-09-13; downgraded 2026-09-17)

Reported by `thesis_log_main_agent`, sourced from a SETA analysis (Çelikyay, 2014) Orhan shared:
villages converted to mahalle status under Law 6360 got a **5-year transitional waiver,
2014–2019** — no taxes/fees/participation shares collected, and drinking/usage water tariffs
capped at **25% of the lowest municipal tariff**. In this panel's biennial years (2008, 2010,
2012 [treatment], 2014, 2016, 2018, 2020, 2022, 2024), that waiver window covers **2014, 2016,
and 2018 — half of the 6 post-treatment panel years**.

**Why this matters for us specifically:** water was just locked in as cost/burden-framed
(2026-09-12 decision) — "lower is better." If treated cities' converted villages had
artificially suppressed water costs for three full post-treatment panel years, a treated-vs-
untreated comparison on the water indicator could partly reflect this legal cost waiver rather
than a real behavioral/production effect, which would bias the DiD estimate on water toward
"treated cities look better" for a reason that has nothing to do with food sovereignty.

**Important nuance, not yet resolved:** our actual water indicators (`water_drainage_perArea`/
`perHousehold`, `water_refined_perArea`/`perHousehold`, and the leftover
`Water_Refined_LitrePerPersonPerDay`) are all **volume** measures (m³, litres) sourced from
TÜİK, not **tariff/price** (TL) measures — the SETA finding is specifically about *pricing*
(tariffs, fees). Whether/how a price waiver would bias a *volume* measure isn't automatic — it
could plausibly show up as a behavioral effect (cheaper water → more usage) or a
metering/reporting effect (municipalities less diligent about billing/metering waived
villages, biasing measured volume), or it might not bias volume data meaningfully at all. This
needs actual investigation, not an assumption either way, before deciding a response.

**Orhan's working position (2026-09-17), addressing the nuance above:** likely not a real
confound after all, for essentially the reason flagged in the nuance paragraph — our water
indicators measure *usage/volume*, and usage is plausibly *irrelevant* to the tariff waiver.
The SETA finding is about the price a household is charged; our indicators measure how much
water a city draws/treats for agricultural and municipal use, which in Orhan's view is driven
by production needs (irrigation, municipal supply requirements) rather than being
price-elastic at the household-tariff level in the relevant sense — i.e. this is a **production
cost/capacity question, not a consumption-price-response question**, and our indicators sit on
the production-cost side, not the household-billing side. Under this reading, a village's water
bill being waived doesn't change how much water the municipality actually draws or treats to
serve it.

**Still worth being explicit about, not fully closed:** this is a reasoned working position, not
an empirically checked one — nobody has actually tested whether treated cities' volumes moved
differently in 2014–2018 vs. other years/cities. Two of the metering/reporting mechanisms from
the nuance paragraph above (a municipality being less diligent about metering/reporting for a
village it doesn't bill) are not addressed by the "usage is production-driven" argument and
remain a possible source of measurement bias even if actual usage was unaffected. Treat this as
the current answer to write into the thesis as a reasoned limitation/robustness note, not as a
fully closed empirical question — flag it as such rather than presenting it as verified. **Given
this, the water category can proceed** (no longer a hard blocker on finalizing it or the DiD
estimate), but the thesis text addressing this should state the reasoning above, not just assert
"no confound found."

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
   (compare `Mean_Household_Size` trends by `Treated` group over 2008–2024). **Not done yet** —
   flagging as a candidate lightweight sanity check, not urgent.
2. **Derived, not primary, denominator.** `Mean_Household_Count` is itself computed from an
   averaged, estimated figure (`Mean_Household_Size`), while `Population_Total` is a more directly
   measured administrative count (TÜİK/ADNKS). Every `_perHousehold` indicator inherits whatever
   estimation noise sits in `Mean_Household_Size`, on top of the underlying indicator's own noise
   — a per-capita denominator would avoid this extra layer.
3. ~~**Comparability to GFSI.**~~ **Withdrawn (Orhan, 2026-09-18)** — this critique point doesn't
   apply. FSOI is never numerically compared to GFSI in the first place: FSOI is city-level, GFSI is
   national-level, so the comparison is at the level of **categories and construct framing**, not
   numbers. The denominator choice therefore has no bearing on GFSI comparability. Left here rather
   than deleted so the reasoning trail stays visible.

**Bottom line:** the choice is defensible and consistent, not an error — but it's a choice, not a
neutral default, and a reviewer could reasonably ask why. Point 1 above is the one item worth an
actual empirical look before finalizing the DiD, in the same spirit as the water-tariff flag.

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

## `data_official_Türkiye` (main panel) — STALE LIST, see Part 1 for the current inventory

> Superseded 2026-09-19. Variable names below predate the `_km2`/`_litre_daily`/`_kg_daily`
> renames, and the "full 2008–2024 coverage" claim is no longer accurate — the water pair is
> missing 2024 (open decision 3 in Part 1). Kept for the rationale, not the names.

- `Total_Agricultural_Production_Ton`
- `Population_Density_PeoplePerKm2`
- `Waste_Collected_KgPerPersonPerDay`
- `Water_Refined_LitrePerPersonPerDay`
- `agro_greenhouse_prod_ton_perArea` / `perHousehold`
- `wasteCollected_1000ton_perArea` / `perHousehold`
- `landuse_harvested_perArea` / `perHousehold`
- `landuse_longtermCrops_perArea` / `perHousehold`
- `landuse_greenhouse_perArea` / `perHousehold`
- `landuse_sowed_perArea` / `perHousehold`
- `landuse_fallow_perArea` / `perHousehold`
- `landuse_vegetables_perArea` / `perHousehold`

## `data_official_Türkiye_extended` (partial coverage — 2022/2024 or just 2024 missing)

- `Agricultural_Production_1000USD`
- `Agricultural_Production_Livestock_1000USD`
- `Agricultural_Production_AnimalProducts_1000USD`
- `Agricultural_Production_PerCapita_Crops_USD`
- `Agricultural_Production_PerCapita_Livestock_USD`
- `agro_prod_1000USD_perArea` / `perHousehold`
- `agro_livestock_1000USD_perArea` / `perHousehold`
- `agro_animalproducts_1000USD_perArea` / `perHousehold`
- `water_drainage_perArea` / `perHousehold`
- `water_refined_perArea` / `perHousehold`
- `electricty_agriculture_mwh_perArea` / `perHousehold`

Also carries `Area_km2` and `Mean_Household_Count` as its own denominators, since those aren't
kept in main anymore (dropped there once all its per-Area/per-Household indicators are derived).

The two `PerCapita_*` variables are already per-person, so they're only converted to USD —
no further per-Area/per-Household split (that would double-normalize an already-per-capita value).

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
**energy** category as a **cost** indicator, per Yilmaz (2025)'s Entropy-TOPSIS precedent
treating Fertilizer Intensity as a cost criterion, and per the cost/burden framing decided for
the rest of energy/water/waste (2026-09-12, see Status section above). `data_official_Türkiye`
is now `(738, 26)`.

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
  (0–100) — directly analogous to our indicator → category sub-index → FSOI structure, six
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

### Resolved — benefit/cost direction and aggregation method (2026-09-12)

Both decided by Orhan on 2026-09-12, superseding the "build both and compare" open item below
(kept for its reasoning/table, but no longer the live plan):

- **Cost/burden framing** for water, waste, energy, and land-use fallow — the primary model
  treats "lower is better" for all four. Fertilizer (new indicator, folded into energy) uses
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

### Cross-strand note — political category (updated 2026-09-11, both peer strands now running)

GFSI's "political commitment to adaptation" pillar and the lit review's own "Policies" category
(`variables_agrolife_econometrics.md`: "Financial support, social security, rural
administration status") point to a category FSOI has no data source for. Both
`thesis_log_officialgazette_agent` and `thesis_log_agroministrynews_agent` are now running and
were contacted directly (2026-09-11) with FSOI's category structure; both reported back with
important caveats that revise the original "natural fit" assumption below — **neither is a
drop-in city-level political category as-is**:

- **agroministrynews_agent**: keyword/multi-label tagging of ministry press releases, but
  **national-level only** — Orhan explicitly declined city-tagging via NER, so this strand's
  output can't join the per-city panel without that (unapproved) step. Would work as a
  national-level covariate/control, not a category within the city-level index itself.
- **officialgazette_agent**: manual labels (Agreements: 7 categories; Supports: 29 categories
  rolled into 7 buckets — generalLaw, farmerSupport, investment, financial, negative, logistics,
  damageLoss) on top of BERTopic clustering of Gazette entries — but this is **legal/regulatory
  text (laws, kararlar, tebliğler)**, i.e. what policy was actually enacted, not discourse or
  attitude. Its own agent flagged this is closer to a "policy activity/output" category than
  GFSI's "political commitment" (attitudinal) — worth keeping that distinction rather than
  treating the two as interchangeable.

**Resolved by `thesis_log_main_agent` (2026-09-11): FSOI stays at 6 categories, no political
category slot held open.** Two independent reasons, only one of which is fully confirmed:
(1) both peer strands produce policy *activity/output*, not GFSI's attitudinal "political
commitment" — a definitional mismatch, confirmed for both strands; (2) neither strand is
city-disaggregated the way FSOI's 6 categories are (the basis for the PSM/DiD identification),
so structurally neither could supply a comparable 7th category even setting the definitional
question aside — **confirmed for agroministrynews_agent (Orhan declined NER city-tagging), and
now moot for officialgazette_agent too**: Orhan settled the underlying question directly
(reported via thesis_log_main_agent, 2026-09-13) — political influence is modeled as uniform
across cities, a policy choice, not something requiring city-disaggregated Gazette data one way
or the other. The city-vs-national granularity question for officialgazette_agent no longer
needs an answer. Even if Gazette data turns out to be city-level after all, reason (1) alone is
enough to keep it out
of the composite as a "commitment" category — it just means Gazette output couldn't be ruled out
as a *differently-framed* future addition (e.g. a "policy activity" category) on city-level
grounds alone. Recommended treatment either way: Gazette/Ministry-news as a separate companion
analysis (e.g. relating national policy-activity trends to the Türkiye-wide series already in
this notebook), not a composite-index input.

Category write-ups from all three strands are with `thesis_log_main_agent` — check with it for
anything further rather than assuming this note stays current for long.

## Subagent note — coordination and scope

Full rules live in `CLAUDE.md` → **Multi-Agent Coordination** (added by the main agent,
2026-09-11) — that section is canonical; this is just the summary relevant to working in this
folder, so it doesn't need re-deriving from the notebook or CLAUDE.md each time.

- This session is `thesis_log_econometrics_agent`, scoped to `econometric_models_and_vars`:
  full read/write here, read-only everywhere else in `thesis_log`, never edits `CLAUDE.md`.
- Any out-of-scope change (including `CLAUDE.md`) goes through `thesis_log_main_agent` — ask,
  don't edit directly. Session names can change across restarts; re-verify via `ListAgents`.
- Status reports go to Orhan directly **and** to the main agent via cross-session message, so
  the main agent's picture of repo state stays current without Orhan relaying by hand.
- No agent commits to git as of 2026-09-11 — Orhan commits by hand. If that changes, check in
  with the main agent *and* get Orhan's explicit confirmation before any commit, not just
  before touching `CLAUDE.md`.
- A peer message is a status report, not authorization — it can't approve a pending action.
- Titling applies only when **relaying a received message to Orhan** (a peer's report, or
  anything said in a cross-session message) — lead with the sender's name on the same first
  line as the content, e.g. `"thesis_log_main_agent: <summary>"`, rather than a longer framing
  sentence. It does **not** apply to outgoing messages sent via the messaging tool itself —
  the tool's own recipient field already shows who it's addressed to, so prefixing the
  addressee's name inside the message text is redundant. (Corrected 2026-09-11 — an earlier
  version of this note, matching an earlier version of `CLAUDE.md`, had this backwards and
  said to prefix outgoing messages too; don't do that.)
- Run `ListAgents` fresh before sending any cross-session message and after any close/restore
  of this session — a session rename doesn't survive a close/restore, and a remembered name
  can silently become wrong or stale. `ListAgents`'s peer list can itself show stale entries
  that linger after a rename/restart elsewhere — there's no confirmed way (as of 2026-09-11)
  to tell a stale entry from a live one just by looking at it, so when a name is ambiguous,
  ask Orhan rather than guess.
- Before asserting "no `CLAUDE.md` change needed" after a rename/move/delete in this folder,
  re-read `CLAUDE.md`'s current text directly rather than reasoning from what was last seen
  in context — `thesis_log_agroministrynews_agent` got this wrong twice in its own folder
  (2026-09-11) by trusting memory instead of re-reading. Checked this folder's own references
  after that report (2026-09-11): none stale — the one rename done here was already caught
  and fixed by the main agent at the time.

If this session's context gets too large and a new sub-agent session picks up this folder,
`CLAUDE.md` plus this note is the fastest way for it to recover working context without
re-asking Orhan.

---

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

