> **Agent note.** Written by a Claude Code sub-agent operating on this folder
> (`econometric_models_and_vars`), documenting pipeline structure it implemented in
> `fsoi_indicator_selection.ipynb`. This is a technical record, not analysis or thesis prose —
> review before citing or incorporating into the written thesis. Human draft notes live in
> `Variable_Analysis_Methods/`.


---

# Where to start (see "Aggregation, DiD, and robustness — current state" in Part 1)

The 2026-09-20 handover that used to sit here is fully superseded — aggregation, both
tracks, the DiD, and every robustness check are built and executed clean. Its content moved
to history 2026-09-24; the two facts from it still worth keeping without re-deriving:

- **`perArea` is ~99% population density across cities but is the clean track within a city
  over time; `perHousehold` is the reverse.** Contaminated in opposite dimensions
  (Diagnostic 6). Build the index from `perHousehold` only; `perArea` is a separate
  robustness track, never mixed into the same aggregation.
- **Every analytical claim goes in the notebook as a cell that computes its numbers** — never
  paste a result found elsewhere as a hardcoded literal. Caught once already (2026-09), a
  repo-wide Working Convention in `CLAUDE.md` since.


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
  grows; per-head rates fall as lower-usage rural population is absorbed). Plausible, not proven —
  a real treatment effect could produce part of the same pattern. Affects water, waste and possibly
  external input, i.e. three of the six categories. **A ratio of two municipal statistics is immune to
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
Categories present here: production, land-use, waste, external input (fertiliser only).

**`data_official_Türkiye_extended`** — 5 indicator pairs: `agro_crop_1000USD_*`,
`agro_livestock_1000USD_*`, `agro_animalproducts_1000USD_*`, `water_drainage_*`,
`electricity_agriculture_mwh_*` — plus raw source columns and denominators (`Area_km2`,
`Mean_Household_Count`, `Water_Drainage_1000m3PerYear`, `Water_Refined_1000m3PerYear`,
`Electric_Energy_Use_*`) and the `nonagri_electricity_mwh_perHousehold` covariate, which is a
control, **not** an FSOI indicator (it is excluded via `EXTENDED_EXCLUDE`).
Categories present here: market, water, external input (agricultural electricity).

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
   **Not yet built:** the DiD regression itself, and the item-5 robustness checks below.

## Aggregation, DiD, and robustness — current state (as of 2026-09-24)

*The full blow-by-blow (every intermediate specification, every corrected conclusion, in the
order it happened) moved to `agent_note_econometrics_FSOI_history.md` on 2026-09-24 — read
there only to reconstruct how a number was found or to defend the process. What follows is
the current, settled picture, corrections already folded in rather than narrated.*

**Track A's DiD-ready structure is built and stress-tested more than any other part of this
pipeline:** flips, `CATEGORY_MAP_C`/`CATEGORY_MAP_A`, `build_fsoi()`, both tracks, top/bottom
cities, and a full DiD section, all executed clean in `fsoi_indicator_selection.ipynb`
(144 cells as of 2026-09-24, zero errors, outputs cleared).

**Descriptive result.** Under the primary aggregation (equal-weighted sum), non-metropolitan
cities score highest (Track C 2020: non-metro 0.500, old-metro 0.433, new-metro 0.424).
**This is robust to removing any single category** (municipal_burden, production, land_use,
external_input, or market — all five tested) **but not to changing the aggregation method**:
under TOPSIS, old-metropolitan leads instead (0.366 vs. 0.336 vs. 0.322). The one thing
robust across every specification tried, aggregation method included, is that
**new-metropolitan cities score lowest.** Do not report "non-metro scores highest" as
settled; report "new-metro scores lowest" instead.

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

**The original pre-rebuild "national decline, independent of Law 6360" finding does not
replicate.** Checked directly (pooled linear trend, city FE, all three real groups, plus the
`Türkiye` aggregate row on its own): with municipal_burden, the trend is **positive and
significant** (+0.00195/year, p < 0.0001) — an increase, not a decline. Without it: flat,
not significant. This is a fact about the rebuilt index, not a verdict on the old one — the
two use different, non-comparable variable sets and constructions, and this check can't say
why they disagree. Orhan confirmed 2026-09-24 the old index mixed perHousehold/per-capita
with weak weighting; the current perHousehold-headline, equal-weighted-primary track is the
chosen path and doesn't need reconciling with it further.

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


8. ~~Report the composite to `thesis_log_main_agent`~~ — done, 2026-09-22 (composite) and
   ongoing (DiD result, same day) — see the cross-session messages logged around this note's
   last updates.

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
observations (2020, 2022); only market caps the six-category index at 2020. Don't let the
composite's year limit truncate the waiver analysis.

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
