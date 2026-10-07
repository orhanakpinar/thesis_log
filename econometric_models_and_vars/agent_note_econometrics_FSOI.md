> **Agent note.** Written by a Claude Code sub-agent operating on this folder
> (`econometric_models_and_vars`), documenting pipeline structure it implemented in
> `fsoi_indicator_selection.ipynb`. This is a technical record, not analysis or thesis prose —
> review before citing or incorporating into the written thesis. Human draft notes live in
> `Variable_Analysis_Methods/`.

*Rewritten 2026-10-05 as one current-state document. Every number below was checked against a
fresh end-to-end run that day (main notebook 200 cells, map notebook 15, 0 errors). The dated
trail of how each result was reached, and the previous body of this note, are in
`agent_note_econometrics_FSOI_history.md` — read it only to reconstruct or defend a step.*

---

# 1. Status

- **Analysis complete; no open analytical items.** Orhan is writing. Writing-strand requests
  arrive via `thesis_log_main_agent`; confirm each with Orhan in this chat before acting.
- **Possible later work (Orhan's call):** more maps during writing (they go in `fsoi_map.ipynb`).
- **Working habits that paid off — keep them:**
  - Compute every number in the cell that shows it; never paste a number into prose or a note
    without a cell that prints it. Make printed conclusions conditional on the computed values.
  - Verify before claiming: re-run and read the output. Several corrections in this strand came
    from re-checking earlier readings (raw vs log scale, normalised vs raw, unlike objects compared).
  - Edit notebooks through JSON scripts with anchored, assert-exactly-once replacements (the Read
    tool can't open the main notebook). Execute with `jupyter nbconvert --execute --inplace`, check
    for error outputs, then clear outputs. Re-read any shared file immediately before writing it.

# 2. Decisions in force

| Decision | Date |
|---|---|
| Two indices: **full index** (`FSOI_C`, 5 categories, 2008–2020) and **long-panel index** (`FSOI_A`, 4 categories, 2008–2024, the DiD index). Thesis uses these names; code keeps C/A. | 2026-09-21/28 |
| Headline denominator **per household**; per area is a robustness track; the two are never averaged together. | 2026-09-22 |
| Equal-weighted sum primary (categories equal, then indicators equal within category); TOPSIS, flat weighting, benefit framing are robustness checks. | 2026-09-13 |
| Cost-framed ("lower is better"): waste, water, fertiliser, agricultural electricity, land-use fallow. | 2026-09-21 |
| **Animal-product value dropped** from the full index (TÜİK provincial series breaks in 2012). Market = crop + livestock value; full index = **13 indicator pairs**. Animal products still built; annex only. | 2026-10-02 |
| **Fertiliser stays per household, zeros kept.** Hakkari's top external-input score is a real, discussable case, not a fix. | 2026-10-05 |
| **log1p kept**, described as: "log1p is applied; for indicators in small units it is close to linear, so for those the scaling is effectively min-max on winsorised raw values." | 2026-10-05 |
| Winsorising 1st/99th; floor-bunching documented, not engineered away. | 2026-09-20 |
| Wild cluster bootstrap with **999 draws**, following Cameron, Gelbach & Miller (2008), *Bootstrap-based improvements for inference with clustered errors*, Review of Economics and Statistics 90(3). No 9,999-draw run (see §3.2). Optional citation for choosing B so that α(B+1) is an integer: Davidson & MacKinnon (2000), *Bootstrap tests: how many bootstraps?*, Econometric Reviews 19(1) — not yet checked against the paper; verify before citing. | 2026-10-05 |
| The 6360 critique is attributed to **ZMO** (Ziraat Mühendisleri Odası, a TMMOB member chamber). | 2026-10-05 |

# 3. Results (verified 2026-10-05)

## 3.1 Descriptive — full index (13 pairs, per household)

- **2020 group means, equal-weighted:** non-metro 0.511, old-metro 0.446, new-metro 0.439.
- **Which group is lowest/highest depends on the view.**

  | View | Non | New | Old | Lowest |
  |---|---|---|---|---|
  | Full, 2020, equal-weighted | 0.511 | 0.439 | 0.446 | new |
  | Full, 2020, TOPSIS | 0.318 | 0.289 | 0.322 | new |
  | Full, pooled 2008–2020, equal-weighted | 0.521 | 0.466 | 0.462 | **old** |
  | Full, pooled 2008–2020, TOPSIS | 0.321 | 0.303 | 0.329 | new |
  | Long-panel, pooled 2008–2024, equal-weighted | 0.507 | 0.466 | 0.484 | new |
  | Long-panel, pooled 2008–2024, TOPSIS | 0.336 | 0.322 | 0.366 | new |

  Flat weighting, full index: 2020 non 0.467 / old 0.414 / new 0.412; pooled old 0.428 < new 0.438.
  **Wording:** "New-metro is lowest in 2020 and on the long-panel index; on the full index
  averaged over 2008–2020, old-metro is marginally lowest (by 0.004 equal-weighted, 0.010 flat).
  Which of non-metro and old-metro leads depends on the aggregation method."
- **These are group means, not treatment effects.** The group spread sits mostly in municipal
  burden (2020: non 0.744 / old 0.563 / new 0.536). Removing it, non-metro still leads every year
  but the non−new gap shrinks 42% (0.055 → 0.032).
- **Full-index change 2008→2020:** provincial mean 0.499 → 0.486 (−0.014); market contributes
  −0.018. Re-expressed relative to the national value each year (no currency or inflation):
  −0.003. **Not a food-sovereignty decline:** it is the dollar, and before the drop also the
  animal-product break.
- **No national decline on the long-panel index:** common trend +0.00195/yr (p < 0.0001) with
  municipal burden; −0.00007/yr (p = 0.844) without.
  - **Why it rises** (cell "Why does the long-panel index rise?"): the provincial mean goes
    0.493 → 0.516 (+0.023) from 2008 to 2024.
  - Contributions: municipal burden +0.0325, production +0.0072, land use −0.0046, external input
    −0.0121.
  - So the rise is municipal burden. Nationally, households grew +54.6% (household size 4.0 → 3.1)
    against waste +32.5%, so waste per household fell 14.3% and the cost-framed score rose.
  - **This is a household-size effect, not improving food sovereignty.** Excluding it, the index is
    flat.
  - **Waste is not falling** (cell "Is waste really falling?"). Türkiye 2008→2024: waste +32.5%,
    population +19.8%, households +54.6%. Waste per person **+10.6%**, per household −14.3%.
    Household growth (log 0.435) is 41% more people and 59% smaller households (size 4.0 → 3.1;
    TÜİK gives 2008 as a whole number, so that split is coarse).
  - **The trend depends on the denominator.** Long-panel index common trend: per household
    +0.00195/yr (p < 0.001); per capita **−0.00096/yr (p = 0.051)**, borderline negative, with
    municipal burden falling 0.626 → 0.568.
  - **So the honest national statement is "no robust national trend"**: slightly up per household,
    because households shrink; slightly down per capita, because waste per person rises. Never
    "food sovereignty rose". The provisional PDF's "national decline" does
  not replicate on this pipeline.
- **Rank agreement:**
  - Full vs long-panel index: Spearman mean 0.761 across 2008–2020 (0.675–0.826). Related, not
    interchangeable.
  - Category-weighted vs flat: 0.934–0.952 by year on the full index, but 0.681 on the long-panel
    index. Flag this: long-panel rankings are more weighting-sensitive.
  - With vs without animal products: 0.983–0.989. 2020 top-10 overlap 9/10, bottom-10 10/10.
- **Hakkari** (notebook cell "Hakkari in the full index"): full-index rank 6th in 2008 and 2010,
  then 9th, 16th, 13th, 21st, and 14th in 2020. Its external-input score is the highest of all
  provinces in 6 of 7 years (3rd in 2010, 11th in 2018), while production (~0.2–0.3) and land use
  (~0.3) are low. Fertiliser is zero or near-zero even in years the Ministry file reports it;
  2020–24 are absent from the file and treated as zero.

## 3.2 Causal — DiD on the long-panel index

**Design:** two-way fixed effects (province + year), `FSOI ~ Treated×Post`, Post = 2014 onward
(pre-period 2008/2010/2012), control = non-metro only (old-metro got a weaker version of the
boundary change), cluster-robust SE by province, 14 treated / 51 control.

- **Primary: −0.0373** (SE 0.0126, p = 0.0031, 95% CI [−0.062, −0.012], n = 585). Wild cluster
  bootstrap p = 0.004.
  *Approved thesis sentence (Orhan, 2026-09-29):* "Because only 14 provinces are treated,
  conventional cluster-robust standard errors may overstate significance (Bertrand, Duflo &
  Mullainathan, 2004); inference is therefore confirmed with a wild cluster bootstrap with
  restricted residuals and Rademacher weights (Cameron, Gelbach & Miller, 2008), 999
  replications, which yields p = 0.004."
- **Every specification, wild-bootstrap p (all significant):**

  | Spec | Coef | Bootstrap p |
  |---|---|---|
  | primary | −0.0373 | 0.004 |
  | size-matched control (28 clusters) | −0.0351 | 0.016 |
  | flat weighting | −0.0267 | 0.002 |
  | TOPSIS | −0.0249 | 0.005 |
  | per capita | −0.0369 | 0.007 |
  | waiver years excluded (n = 390) | −0.0342 | 0.025 |

  Monte Carlo error at 999 draws is about ±0.005 at p = 0.025, so 9,999 draws would change nothing.
  Benefit framing flips the sign (+0.031) by construction; not new evidence.
- ⭐ **ROBUST FINDING — the DiD is the same on both indices.** Long-panel −0.0373 and full index
  −0.0375, built from different category sets (four vs five, with and without market and water)
  over different years (2008–2024 vs 2008–2020). Both have clean pre-trends and are significant
  under the wild bootstrap. The effect does not depend on which index definition is used.
- **Full-index counterpart (robustness, Figure 6.1b, `table_6_1b`):** DiD −0.0375 (SE 0.0069,
  p < 0.001; wild bootstrap: none of 999 draws as extreme, so p < 0.001), n = 455.
  - Event study: 2008 −0.002 and 2010 −0.002 (pre-trends clean); 2014 −0.029, 2016 −0.039,
    2018 −0.046, 2020 −0.040.
  - Same size as the long-panel estimate.
  - Its municipal burden includes water and waste, so the same coverage mechanism applies.
- Figure y-axes read "DiD effect … (new-metro − non-metro gap, minus its 2012 value)".
- **Event study** (relative to 2012; `table_6_1`): 2008 −0.009, 2010 −0.002 (pre-trends clean on a
  two-point test); 2014 −0.041, 2016 −0.046, 2018 −0.045, 2020 −0.049, 2022 −0.038 (p = 0.015),
  2024 −0.026 (p = 0.15).
- **The effect is municipal burden.**
  - Without municipal burden the estimate is +0.0085 (p = 0.224).
  - Each category alone: municipal burden −0.175 (p < 0.0001); land use −0.023 (p = 0.003);
    external input +0.048 (p = 0.004); production −0.0002, 95% CI [−0.0225, +0.0220], a tight null.
  - **Not defensible:** "Law 6360 reduced food sovereignty."
- **Mechanism: municipal coverage expansion, one-for-one.**
  - Log DiD on raw waste collected +0.260 (~30%); on the implied coverage share +0.259
    (ratio 1.00); size-matched ratio 1.06. Same year-by-year path.
  - Household count +2% (p = 0.37), household size +3% (p = 0.21): the denominator is not the story.
  - Waste per covered resident did not change: municipalities recorded waste for ~30% more people.
  - Coverage is **derived from water** (annual water drawn ÷ (365 × water drawn per person per day
    in municipalities), as a share of provincial population). It is an indicator, not a count;
    say so wherever it is used (Figure 6.2's caption does).
- **Why the composite fades while waste does not** (exact decomposition, asserted).
  - **Window (decided by Orhan, 2026-10-07):** always 2014–18 (waiver years) vs 2020–24
    (all post-waiver years). Never drop 2020; the earlier 2022–24 comparison was ungrounded.
  - **Composite:** moves +0.0061 toward zero, a 14% fade. Municipal burden contributes +0.0140,
    more than all of it; production (−0.0041) and land use (−0.0059) drift further negative;
    external input +0.0021.
  - **Cause:** the municipal-burden score fades 27% while log waste fades only 3%. log1p is
    effectively linear at these units and treated waste per household fell, so the same percentage
    jump becomes a smaller absolute gap.
- **Land use (−0.0226), by indicator:**
  - Score scale: fallow −0.0108 (about half; more fallow in treated; the only one significant
    alone, p = 0.021), vegetables −0.0068, long-term crops −0.0039, greenhouse −0.0021, core
    cropland +0.0009.
  - Raw logs: nothing significant (fallow +26% p = 0.31, vegetables −11% p = 0.24, harvested area
    −3% p = 0.67).
  - **Reading:** no farmland loss; a weak, diffuse shift toward fallow. Too weak to carry the ZMO
    argument as a finding.
- **Water and the tariff waiver:** water-alone DiD −0.168 (p = 0.0001). In logs, water fades 23%
  after 2019 against waste's 3%. So the waiver remains possible for water only; it is not testable
  cleanly, because coverage is derived from water. 2020 is also COVID.
- **Robustness to size:** the 14 largest non-metros (Afyonkarahisar 704k … Yozgat 453k, 2012) all
  sit below the smallest treated province (Ordu 741k). The median size gap narrows from 3.02× to
  1.76×. A truly size-overlapping control group is impossible; say so.
- **Data-quality sensitivity:** dropping Kırıkkale (waste 2012 = 41 between 133 and 74), Kırşehir
  (waste 2012 = 143) and Hakkari (zero fertiliser), all controls: −0.0370 vs −0.0373.
- **Per area is not a usable DiD track once normalised.** Per-area DiD −0.0003 (p = 0.949) is
  scale compression: only 0.9% of the per-area waste score's variance is within-province (34% per
  household). Within-province SD is 10.7× smaller; the municipal-burden coefficient is 10.9× smaller.

**Limitations to state:** only three pre-treatment points; a small population-growth differential
(log population DiD +0.051; one pre-period coefficient, 2008, significant); treated and control
never overlap in size; old-metro contaminated as a control for municipal services (implied coverage
+0.089 at the reform vs +0.226 new-metro, −0.020 non-metro).

# 4. Measurement facts the methods chapter needs

**Diagnostics 1–8** (notebook section "Diagnostics"; each is printed by its own cell):
1. **Why per area correlates and per household doesn't.** Population density spans 288× across
   province-years; water per person 5.3× and waste per person 4.7×. Per area against density:
   water 0.986, waste 0.995. Water against waste: 0.977 per area but 0.210 per household. A high
   per-area correlation is therefore weak evidence of redundancy.
2. **Coverage confound.** Implied municipal population share (water total ÷ per-person rate),
   2012→2014: new-metro +0.226, old-metro +0.089, non-metro −0.020. This is the reason the
   per-person water series was dropped and old-metro is not a clean control for municipal services.
3. **Refined water is an infrastructure measure.** Provinces reporting exactly zero fell from 27
   (2008) to 9 (2022), against 0 of 648 for drawn water. Refined was dropped; drawn kept.
4. **Per household vs per capita.** Spearman between the two rankings: harvested land 0.959, crop
   production 0.965, greenhouse output 0.996, waste 0.640, water 0.752. The choice matters only for
   the municipal services; a per-capita robustness track replicates the DiD (−0.0369).
5. **Water trajectory** (descriptive only). Treated provinces' drawn water per household breaks
   upward at 2014, peaks in 2018, falls by 2022; controls stay flat. Confounded by COVID and by
   coverage.
6. **The two denominators are contaminated in opposite dimensions.** Across provinces, per area
   tracks density (0.988) and per household doesn't (0.048). Within a province over time, per area
   equals the raw total (r = 1.000, all provinces) while per household drifts (median r = 0.717).
   Hence the denominators are never averaged together.
7. **Household size vs score** (full index, 2020). Spearman with FSOI −0.267, with municipal burden
   −0.504, within non-metros only −0.053. Mostly a between-group pattern. Household size shows no
   differential trend in the DiD (log +0.029, p = 0.21).
8. **Industrialisation does not explain high water use** (cell added 2026-10-05). Non-agricultural
   electricity per household vs drawn water per household, n = 648: Pearson −0.045, Spearman
   −0.025. *An older figure, "about −0.27", sat in the notebook's markdown with no computing cell;
   it was wrong and has been replaced. The conclusion is unchanged.*


- **Per area tracks density; per household doesn't.** Drawn water, pooled province-years (n = 648,
  2008–2022), Pearson with population density: per area 0.988, per household 0.048 (waste:
  0.995 / 0.163). Within a province over time the reverse holds: per area is the raw total rescaled
  by a constant (r = 1.000), per household drifts with household size. Figure 4.3.
- **Normalisation:** log1p → winsorise 1/99 (cities only) → pooled min-max 2008–2024, Türkiye placed
  on the scale. Cost flips applied at aggregation.
  - On the 26 index columns: mean |skew| 3.07 → 1.87. log1p is near-linear (Pearson > 0.99 with
    raw) for 14 of 26: every land-use column and waste per household, because their units are tiny.
  - It does real work for production, market, agricultural electricity and water per area.
    Per-column table: `table_B3`.
- **Greenhouse floor-bunching:** share of province-years (n = 729) with normalised value < 0.05 —
  greenhouse land per household 85.3%, greenhouse output per household 79.0%, greenhouse land per
  area 85.2%, waste per area 74.6%.
- **Exchange rates:** one USD/TRY rate per year, typed into the Transformations cell (documented as
  the average of the Central Bank's first- and last-day rates). The code cannot verify the
  derivation, only its use.
- **Animal-product break (annex):**
  - Provinces sum to the national total in 2008/2010, then 0.385, 0.604, 0.436, 0.492, 0.554
    (2012–2020).
  - The provincial series is the one that breaks (national ×1.06, provincial sum ×0.41, 2010→2012).
  - Per-province break ratio: p10 0.25, median 0.45, p90 0.57. Poultry provinces are hit hardest
    (Bolu, Manisa, Sakarya). By group: old 0.36, new 0.43, non 0.46 (Kruskal–Wallis p = 0.025).
  - Candidate explanation (meat, poultry, eggs and hides excluded from 2011, per a governorate
    yearbook citing TÜİK) is **unverified at TÜİK**.
- **Noisy indicators** (one-year spikes > 2×): fallow, greenhouse and agricultural electricity are
  noisy near zero; waste has one case.

# 5. Thesis outputs (`thesis_outputs/`)

| File | Content | Made by |
|---|---|---|
| `fig_4_3_per_area_vs_per_household.png` | per area vs per household against density | main nb |
| `fig_5_1_full_index_2020_map.png` | full index 2020, new-metro outlined | `fsoi_map.ipynb` |
| `fig_5_2_group_means_over_time.png` | group means, both indices, reform shaded | main nb |
| `fig_6_1_event_study_long_panel.png` + `table_6_1_...csv` | DiD event study | main nb |
| `fig_6_1b_event_study_full_index.png` + `table_6_1b_...csv` | DiD event study, full index (robustness) | main nb |
| `fig_6_2_waste_and_coverage.png` + `table_6_2_...csv` | log waste vs log coverage | main nb |
| `table_B1_full_index_with_without_animal_products.csv` | annex comparison | main nb |
| `table_B2_animal_products_break.csv` | break characterisation | main nb |
| `table_B3_skew_by_indicator.csv` | skew per index column | main nb |
| `table_data_appendix_indicators.csv` | exact TÜİK/TOB/HGM source columns | main nb |

*(Renamed 2026-10-06 from `fsoi_track_C/A_perHousehold.csv`. The old files are left in place,
identical, until the writing strand's `descriptive_tables.py` switches to the new names; then
delete them.)*
The main notebook also exports `fsoi_full_index_perHousehold.csv` and `fsoi_long_panel_index_perHousehold.csv`,
which `fsoi_map.ipynb` reads; re-run the main notebook first whenever the index changes.

**Map data source:**
- Province boundaries: HDX "Türkiye — Subnational Administrative Boundaries" (`cod-ab-tur`,
  admin-1, OCHA). The original source is **Harita Genel Müdürlüğü**, the same agency as the area
  data. Licence CC BY-IGO.
- `fsoi_map.ipynb` downloads the boundaries once, simplifies them (0.01°), and caches them at
  `geo/tur_admin1_simplified.geojson`.
- Province names are matched on a Turkish-folded key, asserted 81/81 both ways.
- The map values come from the exported index CSVs.
- `fsoi_map.ipynb` also holds the provinces-by-group map, a province-centroid version of the 2020
  map, and a 2012→2024 raw-change map (long-panel index, descriptive only).

# 6. Pipeline reference

**Data.**
- `TÜİK_Agro_Summary.csv`: TÜİK regional statistics, read as latin-1 in the notebook; the true
  encoding is cp1254.
- `TOB_fertilizer_cities.xlsx`: fertiliser.
- `Türkiye_Municipal_Areas.xlsx`: HGM province area, constant over time.
- Analysis years are biennial, 2008–2024. 81 provinces plus a `Türkiye` aggregate row.
- `Treated`: 0 non-metro (51), 1 new-metro 2012 (14), 2 old-metro (16), 3 Türkiye.
  `Treated_Label` carries the readable text.

**Two panels.**
- `data_official_Türkiye` (main, gap-free 2008–2024): production (total crop tonnage, greenhouse
  output); land use (core = harvested + sown collapsed, r = 0.99; fallow; greenhouse land; long-term
  crops; vegetables); waste; fertiliser.
- `data_official_Türkiye_extended`: crop, livestock and animal-product value (USD, to 2020); drawn
  water and agricultural electricity (to 2022); a non-agricultural electricity covariate (not an
  indicator). Each indicator is a `_perArea` + `_perHousehold` pair; normalised columns have
  `_norm`, cost-flipped scores `_score`. A per-capita track exists for the long-panel index.

**Categories.**

| Category | Full index | Long-panel index |
|---|---|---|
| production | greenhouse output, total crop tonnage | same |
| land use | core, fallow (cost), greenhouse land, long-term crops, vegetables | same |
| municipal burden | waste + water (cost) | waste only |
| external input | fertiliser + agricultural electricity (cost) | fertiliser only |
| market | crop value + livestock value | — (no main-panel member) |

- Indicator weight = 1/(categories × members): long-panel waste and fertiliser 25% each, each
  land-use indicator 5%. The flat-weighting check equalises this.
- Water was merged with waste into one category because, as lone categories, each got up to 5× the
  per-indicator weight of a land-use indicator; in the full index this cut water's weight
  1/6 → 1/10. Water's absence from the long-panel index is a separate cause: panel coverage.
- Market and production deliberately stay separate.

**Dropped, and why — don't re-add:**
- Per-person water series: its denominator is municipal population, which Law 6360 moved.
- Refined water: records whether a treatment plant exists, not usage.
- Daily waste rate: 0.999-correlated with the annual total.
- Animal-product value: series break.

**Confounds** (canonical text in CLAUDE.md → *Law 6360 confounds*):
- (a) Coverage expansion: the main mechanism above.
- (b) The 2014–2019 tariff waiver: possible for water, not supported by waste.

**Control groups:** non-metro is the only clean control for municipal-service variables; old-metro
is usable for agricultural variables, since land use and production are collected province-wide.

**Reference literature:**
- Yilmaz (2025): Entropy–TOPSIS provincial ranking; ratio criteria; fertiliser intensity as a cost.
- Economist Impact GFSI (2022): hierarchical structure, equal-weight option, fixed min-max
  thresholds across years (the precedent for pooled normalisation).
- FSOI is positioned as a critical counterpart to GFSI, compared at the level of categories and
  construct, not numbers (CLAUDE.md → *FSOI vs. GFSI*).

**Coordination:** `thesis_log_econometrics_agent` owns this folder, is read-only elsewhere, and never
edits `CLAUDE.md`. Protocol: CLAUDE.md → *Multi-Agent Coordination*.
