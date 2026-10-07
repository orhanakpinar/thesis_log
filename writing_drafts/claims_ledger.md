# Claims ledger

Every claim the thesis will make: the number behind it, where that number is computed, and the
limit that must travel with it. Chapters are written from this file, not from memory or notes.

**How to use it**
- **Status:** `settled` = decided and computed · `open` = needs work or a decision · `Orhan` =
  your call or your writing · `verify` = check against a primary source before citing.
- **✓ column:** tick it only when you can explain the claim out loud without notes. The empty
  ticks are your defense prep list.
- **`[INT]`** marks an interpretation, not a computed fact. These are where your voice goes.
- Chapter codes: Intro · Lit · Law6360 · Measure · Descr · Causal · Discourse · Discussion.

**Sources (abbreviations)**
- **NB**: `econometric_models_and_vars/fsoi_indicator_selection.ipynb` (section names given)
- **MAP**: `econometric_models_and_vars/fsoi_map.ipynb`
- **ATT**: `writing_drafts/scripts/attrition_table.py` (reads `FSOI_Variables_List/*.xlsx`)
- **DT**: `writing_drafts/scripts/descriptive_tables.py` (reads the FSOI exports `fsoi_full_index_perHousehold.csv` and `fsoi_long_panel_index_perHousehold.csv`)
- **RGD**: `resmi_gazete/resmigazete_annotation_diagnostics.py`
- **RGN / AMN / ECN**: agent notes for Gazette / ministry news / econometrics (a pointer to
  where a figure is documented; the figure itself must come from code)
- **PDF**: the 2025 preliminary PDF (superseded results; historical record only)

Numbers were transcribed from the notes and CLAUDE.md on 2026-09-26, and checked against the
econometrics note's "Writing-ready summary" (full notebook re-run 2026-09-28, 168 cells, 0 errors):
consistent, no changes needed. Before a number goes into a chapter, re-read it from its computing
cell.

---

## Specification map

Three independent choices. The thesis reports one primary combination; every alternative is a
row in a single robustness table.

| Choice | Options | Primary |
|---|---|---|
| Which index | full index (5 categories, 2008–2020) / long-panel index (4 categories, 2008–2024) | full for description, long-panel for the DiD |
| Denominator | per household / per area / per capita | per household |
| Aggregation | equal category weights / equal indicator weights (flat) / TOPSIS | equal category weights |
| Direction | cost framing / benefit framing | cost framing |

---

## A. Research design and framing

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| A1 | The thesis asks (1) whether food sovereignty can be measured from official statistics, and how much of it; (2) whether Law 6360 left a measurable trace. | two-layer framing | n/a | | Intro | Orhan (drafting) | ☐ |
| A2 | Tested hypothesis: Law 6360 reduced food sovereignty in new-metropolitan provinces. | original design | n/a | Verdict must separate composite vs. components (see D21) | Intro, Causal | settled | ☐ |
| A3 | Law 6360 was enacted in 2012 and took effect with the March 2014 local elections. | legal record | primary source | | Law6360 | verify | ☐ |
| A4 | 14 provinces became metropolitan: 13 under Law 6360, plus Ordu under Law 6447 (2013). The PDF says "fourteen by 6360". | legal record | primary source | Ordu's route differs; say so once | Law6360 | verify | ☐ |
| A5 | After the reform: 30 metropolitan provinces (16 old + 14 new), 51 non-metropolitan. | group coding | NB, `Treated` categorical | | Law6360, Measure | settled | ☐ |
| A6 | Unit of analysis: province-year, biennial 2008–2024 (9 time points). | panel design | NB | Biennial: post-period starts 2014 | Measure | settled | ☐ |

## B. Measurement: from theory to 14 indicators

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| B0 | Municipal burden stays inside the index; Chapter 6 leads with the category decomposition. | Orhan's decision 2026-10-01 (first draft) | n/a | Can be revisited with Ali Hoca | Measure, Causal | settled (first draft) | ☐ |
| B00 | **Animal-product value dropped from the index (Orhan, 2026-10-01); moved to Appendix B.** Reason is data quality, not results: provincial series sums to only 38–60% of the national total from 2012, unevenly across provinces and groups (C15). Full index becomes 13 indicators (26 columns); market = crop value + live animal value. Long-panel index unchanged. | decision | rebuild pending in NB | **All full-index numbers (B20 rows, C1–C14, Ch. 5) must be recomputed** | Measure, Descr, Appendix | settled; rebuild pending | ☐ |
| B1 | Candidate indicators were extracted by grounded-theory reading of 32 Türkiye-focused papers (Dergipark: *tarımsal*, *kırsal*; plus one agroecology and one welfare paper). | 32 papers (49 read, 32 used) | `literature_research/` (locate the paper list) | | Measure | verify list exists | ☐ |
| B2 | Reading produced 184 candidate indicators in 27 categories. | 184 / 27 (+1 "Extras" row) | ATT | An earlier report said 251 raw → 183 merged; use 184 (the file) and say the 251 was before merging | Measure | settled | ☐ |
| B3 | 88 of 184 candidates could be matched to a data source file; 24 survived filtering. | 184 → 88 → 24 | ATT | "Matched to a source" ≠ available at province-year for all years | Measure | settled | ☐ |
| B4 | The relational categories went to zero: Land Security (6), Autonomy (5), Seed Sovereignty (3), Cooperative (6), Food Sovereignty (4), Scale (4), Farmer Dynamics (3), Gender (1), Ethnicity (2), Income (1). | per-category counts | ATT | Reason is availability (Orhan). Several had a matched source but were dropped at the data check (Land Security 5/6, Cooperative 5/6, Food Sovereignty 4/4), so say "not available as a province-level series for the panel years", not "the state doesn't publish them at all". | Measure | settled (wording per B5 table) | ☐ |
| B5 | Full 184-row table with a "why eliminated" column goes in the appendix. Draft reasons: 24 kept; 101 source found but dropped at the data check (years/coverage); 34 no official source; 21 need survey data; 5 only at NUTS1/NUTS2. | draft table | ATT → `tables/indicator_attrition_draft.xlsx` | Draft reasons are rule-based from the Source/Level columns; Orhan corrects the `reason_orhan` column where needed | Appendix | open: Orhan's pass | ☐ |
| B4a | The core of sovereignty has the highest source-match rate (27/37, 73%) vs production and land (24/72, 33%) and social and governance (37/75, 49%), yet 1 kept. Sources exist, but not as province-year series. | bloc counts | `scripts/fig_4_1_attrition.py` (Figure 4.1) | | Measure | settled | ☐ |
| B5a | The panel starts in 2008 because several indicators aren't available earlier. | availability | TÜİK series coverage | A choice made for completeness; state it | Measure | settled | ☐ |
| B6 | 24 filtered indicators became 14 indicator pairs: refined water dropped, per-person water dropped, waste daily series dropped, harvested ≈ sowed collapsed into core land use, greenhouse split between production and land use, fertilizer added from the Ministry of Agriculture and Forestry. | step list | NB + ECN "Variable selection is COMPLETE" | Fertilizer comes from the ministry, not TÜİK | Measure | settled; trace each step | ☐ |
| B7 | Refined water was dropped because it records whether a treatment plant exists (27/81 provinces exactly zero in 2008). | 27/81 zeros | NB (water diagnostics) | | Measure | settled | ☐ |
| B8 | Per-person water was dropped because TÜİK divides by municipal population, which Law 6360 itself expanded. | coverage jump, see E1 | NB diagnostics | Must not be re-added | Measure | settled | ☐ |
| B9 | Five categories: production, municipal burden (water + waste), external input (fertilizer + agricultural electricity), market, land use. | category map | NB `CATEGORY_MAP_C` | | Measure | settled | ☐ |
| B10 | Water and waste were grouped because equal category weighting gave each lone-indicator category up to 5× the per-indicator weight of land use. They are also the only two non-agricultural, municipal household services. | weight = 1/(N×k) | NB | Grouping, not merging: both indicators stay separate | Measure | settled | ☐ |
| B11 | "External input", not "energy": fertilizer and agricultural electricity are both purchased off-farm inputs; input autonomy is constitutive of food sovereignty. | construct argument | n/a | [INT] | Measure | settled | ☐ |
| B12 | Cost-framed (lower = better): water, waste, fertilizer, agricultural electricity, fallow land. | flip list | NB `COST_INDICATORS` (asserted) | Direction is a theoretical choice; benefit framing reported as robustness (D10) | Measure | settled | ☐ |
| B13 | Normalization: log1p → winsorize at 1st/99th percentiles → pooled min-max. Thresholds from provinces only (Türkiye row placed on the scale), pooled over 2008–2024 so a change means the province changed. | recipe | NB "Normalisation" + "Choosing the winsorising bounds" | | Measure | settled | ☐ |
| B14 | Why 1/99: 5/95 collapses Antalya, Mersin, Adana, Muğla to exactly 1.000 in greenhouse; rank normalization discards magnitude. | scheme comparison table | NB "Choosing the winsorising bounds" | | Measure | settled | ☐ |
| B15 | Floor-bunching (share of province-years, n = 729, with normalized value < 0.05): greenhouse land per household 85.3%, greenhouse output per household 79.0%, greenhouse land per area 85.2%, waste per area 74.6%, greenhouse output per area 49.4% (an old note wrongly gave 74.6% for greenhouse output per area). Documented, not engineered away. | shares | NB normalization checks | Their practical weight is below nominal | Measure | settled | ☐ |
| B16 | Aggregation: category sub-index = mean of its indicators; FSOI = mean of categories (equal weights). TOPSIS and flat per-indicator weighting are robustness checks. | `build_fsoi()` | NB | Precedent: GFSI's neutral weights | Measure | settled | ☐ |
| B17 | Per household is the headline denominator; per area is a robustness track; the two are never combined. | design | NB | | Measure | settled | ☐ |
| B18 | The two denominators fail in opposite dimensions: across provinces per area ≈ population density (r = 0.988); within a province over time per household drifts (r = 0.72 with the raw total). | r values | NB Diagnostic 6 | | Measure | settled | ☐ |
| B18a | Industrialization does not explain high water use per household: non-agricultural electricity per household and water per household are essentially uncorrelated (Pearson −0.045, Spearman −0.025, n = 648). An older note's "about −0.27" was never computed; do not use it. | correlation | NB Diagnostic 8 | | Measure | settled | ☐ |
| B19 | Per household vs. per capita: rankings nearly identical for land and production (ρ 0.96–1.00) but not for waste (0.640) or water (0.752). | Spearman ρ | NB | Why a per-capita check was run (D12) | Measure | settled | ☐ |
| B20 | Full index: 5 categories, 14 pairs, 2008–2020, 574 rows (82 locations × 7 years incl. the Türkiye row). Long-panel index: 4 categories, 9 pairs, 2008–2024, 738 rows. | row counts | NB `build_fsoi()` asserts | 82 = 81 provinces + Türkiye aggregate | Measure | settled | ☐ |
| B21 | Two indices because TÜİK has not published market value (2022, 2024) or water / agricultural electricity (2024). Missing years are publication gaps; nothing is imputed. | coverage table | NB (rows per year per category) | | Measure | settled | ☐ |
| B22 | Categories differ between the indices: in the long-panel index, external input = fertilizer only and municipal burden = waste only. | category maps | NB `CATEGORY_MAP_A` | State it; don't smooth it over | Measure | settled | ☐ |
| B23 | FSOI measures the *material base* of food sovereignty (productive capacity, input dependence, land use), not its *relational core* (ownership, autonomy, voice). | follows from B4 | n/a | [INT]; depends on B4 reasons | Measure, Discussion | Orhan | ☐ |
| B24 | Whether municipal burden stays inside the index or is reported separately as "what the reform changed". | | | Methodology change; take to Ali Hoca | Measure | **open: Orhan + advisor** | ☐ |

## C. Descriptive results

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| C1 | **Wording (rebuilt index, 2026-10-02):** "New-metropolitan provinces are lowest in every 2020 and long-panel view; in the full index averaged over 2008–2020, old-metropolitan provinces are marginally lowest (by 0.004 equal-weighted, 0.010 flat)." Rebuilt values: 2020 EW non 0.511 / old 0.446 / new 0.439; flat 0.467 / 0.414 / 0.412; TOPSIS old 0.322 / non 0.318 / new 0.289; pooled EW non 0.521 / new 0.466 / old 0.462. Flat vs category-weighted ranks ρ 0.934–0.952 (full index). OLD wording below is superseded: New-metropolitan provinces are lowest or tied-lowest in every view tried. | Six views; the exception is full index pooled 2008–2020, equal-weighted: non 0.511, new 0.453, old 0.451 (old lowest by 0.002) | NB "Claims-ledger checks" | Descriptive, not causal. Don't say "lowest in every specification" | Descr | settled | ☐ |
| C2 | Which of non-metro and old-metro leads depends on the method. Full index 2020 (rebuilt, 13 indicators): equal-weighted non-metro leads; TOPSIS old-metro leads, but only by 0.004 (old 0.322, non 0.318, new 0.289). Pre-rebuild values (0.313 / 0.306 / 0.276) are superseded. | like-for-like comparison | NB "Claims-ledger checks" (rebuilt) | Never report "non-metro highest" as a finding; the TOPSIS lead is marginal too | Descr | settled | ☐ |
| C3 | Full index (rebuilt), 2020, equal-weighted: non-metro 0.511, old-metro 0.446, new-metro 0.439 (pre-rebuild 0.500 / 0.433 / 0.424, superseded). Long-panel index pooled 2008–2024 equal-weighted: 0.507 / 0.484 / 0.466 (unaffected). | group means | NB "Claims-ledger checks" | Always name which index, year and method a group mean refers to | Descr | settled | ☐ |
| C4 | The equal-weighted ordering is robust to dropping any single one of the five categories. | category-drop runs | NB | Robust to category removal, not to method change | Descr | settled | ☐ |
| C5 | Full (rebuilt) vs. long-panel province rankings agree at Spearman ρ 0.675–0.826 (mean 0.761) across seven shared years (pre-rebuild 0.72–0.83, mean 0.778, superseded). Rebuilt 2020: Siirt 21st (full) vs 58th (long-panel); 8 provinces differ by more than 25 places. | ρ by year; rank shifts | NB rank-convergence cell; DT (rank shifts) | Not interchangeable; report both | Descr | settled | ☐ |
| C6 | Rankings are moderately sensitive to weighting: category-weighted vs. flat per-indicator ρ = 0.681 (long-panel, pooled); TOPSIS vs. primary ρ = 0.917. | ρ | NB robustness | Group direction stable, individual ranks less so | Descr | settled | ☐ |
| C7 | **Long-panel index:** no national decline. Pooled trend +0.00195/year (p < 0.0001) with municipal burden, per household; flat without it (−0.00007/year, p = 0.844). | trend regression | NB | The upward drift is a household-size effect and reverses per capita (C7b): report as "no robust trend", never as a rise. Full index: see C10 | Descr | settled | ☐ |
| C10 | **Full index:** mean falls 0.494 → 0.474 (2008–2020); 68% of provinces end lower. The decline is driven by market (0.466 → 0.342, contribution −0.025 of −0.021); the other four categories roughly cancel out (net +0.004). Production in tons rises; the municipal burden score rises (measured burden per household fell). | category decomposition | DT (`scripts/descriptive_tables.py`); four-version check in NB "Update 2026-10-01" | **Not a food-sovereignty decline.** Comes from the USD conversion plus a break in TÜİK's animal-product value series (provinces sum to the national total in 2008/2010, only 38–60% from 2012). Change 2008–2020: USD as built −0.021; without animal products −0.014; relative to national −0.003; relative without animal products +0.004. New-metro lowest in 2020 under all four. | Descr | settled: Orhan reviewed; keep animal products in the index, report the break as a limitation | ☐ |
| C15 | Data-quality limitation of the market category: animal-product value series coverage break from 2012 (see C10); also causes market's 2010 peak. The provincial series is under-counted (national row fine) and **not uniform**: provincial/national ratio p10 0.25, median 0.45, p90 0.57 (Bolu 0.05, Manisa 0.10, poultry provinces worst); by group old-metro 0.36, new-metro 0.43, non-metro 0.46 (Kruskal–Wallis p = 0.025). Penalises old-metro most, which bears on the non- vs old-metro ordering. | coverage check | NB "Chapter 6 outputs and the animal-product break" | Candidate explanation (meat, poultry, eggs, hides excluded from 2011) is from a governorate yearbook, **not verified at TÜİK: don't cite** | Measure, Descr | settled | ☐ |
| C11 | New-metro scored above old-metro in every pre-reform year (rebuilt: 2012 0.497 vs 0.481) and below from 2014 (2014 0.464 vs 0.472; 2020 0.439 vs 0.446). | group means by year | DT | Descriptive; old-metro also partly treated; Chapter 6 tests it | Descr | settled | ☐ |
| C12 | **Rebuilt index:** nine of the ten highest-scoring provinces in 2020 are non-metropolitan; the tenth is Antalya (old-metro). Iğdır highest (0.628), Şırnak lowest (0.351). Hakkari 14th, via the top external-input score (near-zero fertilizer reported in every year it reports); full-index rank 2008→2020: 6, 6, 9, 16, 13, 21, 14; highest external-input score in 6 of 7 years (NB cell "Hakkari in the full index"). | ranking | DT | Hakkari: low input use ≠ sovereignty where there is little agriculture (Orhan, 2026-10-05: keep zeros, discuss as a case) | Descr | settled | ☐ |
| C7b | **CORRECTED 2026-10-07: the long-panel index has no robust national trend.** Per household +0.00195/yr (p < 0.001; mean 0.493 → 0.516); per capita −0.00096/yr (p = 0.051; full per-capita long-panel composite, all four categories rebuilt per capita, harvested land per capita substituting for the core-cropland index; same spec: FSOI ~ Year + province FE, 81 provinces, clustered SE). Municipal-burden means 0.626 → 0.568 are context only, not the trend. Türkiye 2008→2024: waste +32.5% (waste is NOT falling), population +19.8%, households +54.6% (size 4.0 → 3.1); waste per person +10.6%, per household −14.3%. Wording: "no robust national trend in the long-panel index: slightly up per household because households shrink, slightly down per capita because waste per person rises." **Never write that food sovereignty or the index rose nationally.** "Neither index shows a real national food-sovereignty trend" holds. | decomposition | NB (econometrics, 2026-10-07) | | Descr, Discussion | settled | ☐ |
| D2b | DiD on the **full index** (robustness): −0.0375 (SE 0.0069, p < 0.001; bootstrap p < 0.001), n = 455; event study 2008 −0.002, 2010 −0.002, 2014 −0.029, 2016 −0.039, 2018 −0.046, 2020 −0.040. Long-panel stays primary. | | NB; `thesis_outputs/fig_6_1b…`, `table_6_1b…` (thesis Figure 6.3) | Municipal burden = water + waste here; same coverage reading | Causal | settled | ☐ |
| C10b | **Rebuilt index:** mean falls 0.499 → 0.486 (2008–2020), 65% of provinces lower; market contributes −0.018 of −0.014; relative-to-national version +0.004. | DT; Appendix B | | "a fall in the dollar value of output, not a decline in food sovereignty" | Descr | settled | ☐ |
| C13 | Low scores come by two opposite routes: urban-industrial (İstanbul, Kocaeli, Yalova: low production, high external-input score) and intensive agricultural (Konya, Şanlıurfa, Mardin: above-median production, near-zero external-input score). | category profiles | DT | Illustrates compensability (B16) | Descr | settled | ☐ |
| C14 | Province ranks are stable: Spearman 0.79 between 2008 and 2020 (full index). Spread stable (SD 0.060–0.068). | | DT | | Descr | settled | ☐ |
| C8 | The municipal burden category carries most of the descriptive group gap (group means 0.744 / 0.563 / 0.536). | category means | NB "Claims-ledger checks" | Full index, 2020 | Descr | settled | ☐ |
| C9 | Maps: group membership, 2020 full-index choropleth, 2012 → 2024 change (descriptive only). | four maps | MAP | Boundaries: HDX `cod-ab-tur`, source HGM, CC BY-IGO; cite | Descr | settled | ☐ |

## D. Causal results

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| D1 | Design: two-way fixed effects (province + year), SE clustered by province; long-panel index; control = non-metro only; Post = 2014 onward; 14 treated, 65 clusters, n = 585. | spec | NB DiD section | Old-metro excluded (see E2) | Causal | settled | ☐ |
| D2 | Primary estimate −0.037 (SE 0.013; 95% CI −0.062 to −0.012; p = 0.003). | coefficient | NB DiD | | Causal | settled | ☐ |
| D3 | Wild cluster bootstrap (Rademacher, 999 draws, restricted residuals): p = 0.004. | p | NB | Corrects for few treated clusters | Causal | settled | ☐ |
| D4 | Pre-treatment check: 2008 and 2010 vs. 2012, neither significant. | event study | NB | Two points: a weak test; say so | Causal | settled | ☐ |
| D5 | Event study (long-panel FSOI, 2012 = ref): 2008 −0.009, 2010 −0.002; 2014 −0.041, 2016 −0.046, 2018 −0.045, 2020 −0.049, 2022 −0.038 (p 0.015), 2024 −0.026 (p 0.15). The fade is mechanical: log1p is effectively linear for waste per household, so a stable % gap becomes a shrinking score gap as waste per household declines. **Fixed window (Orhan, 2026-10-07): always 2014–18 (waiver years) vs 2020–24 (all post-waiver years); never drop 2020; the 2022–24 window is retired.** Log waste fades 3% (0.257 → 0.249); municipal-burden score effect fades 27%; long-panel composite fades 14% (+0.0061 toward zero; contributions municipal burden +0.0140, production −0.0041, land use −0.0059, external input +0.0021). Note: "27%" is the municipal-burden fade, not the composite's. | coefficients; exact decomposition | NB "Chapter 6 outputs…"; `thesis_outputs/table_6_1…csv`, Figure 6.1 | Use only the fixed window 2014–18 vs 2020–24 | Causal | settled | ☐ |
| B13a | log1p is effectively linear (r > 0.99 with raw) for 14 of 28 normalized columns; their skew is unchanged. Don't say the log step reduces skew across the board. | | NB | | Measure | settled | ☐ |
| D6 | Without municipal burden the estimate is +0.009 (p = 0.224). | leave-one-category-out | NB | | Causal | settled | ☐ |
| D7 | Category by category: municipal burden −0.175 (p < 0.0001); land use −0.023 (p = 0.003); external input +0.048 (p = 0.004); production −0.0002 (SE 0.011; 95% CI −0.022 to +0.022). | isolation runs | NB; production CI in "Claims-ledger checks" | Production is a **tight** null: it rules out effects larger than ±0.022 (0.18 SD of the production score, ~8× smaller than municipal burden's effect) | Causal | settled | ☐ |
| D8 | Flat weighting: −0.027 (p = 0.0007); without municipal burden −0.008 (p = 0.174). | | NB | | Causal | settled | ☐ |
| D9 | TOPSIS: −0.025 (p = 0.002); without municipal burden −0.0003 (p = 0.968). | | NB | | Causal | settled | ☐ |
| D10 | Benefit framing flips the sign (+0.031, p = 0.008), mechanically. | | NB | Not new evidence | Causal (appendix) | settled | ☐ |
| D11 | Excluding tariff-waiver years (2014, 2016, 2018): −0.034 (p = 0.042); without municipal burden +0.003 (p = 0.746). | | NB | Smaller n | Causal | settled | ☐ |
| D12 | Per-capita denominator: −0.0369 vs. −0.0373. | | NB | | Causal | settled | ☐ |
| D13 | The normalized per-area null (−0.0003, p = 0.949) is scale compression: only 0.9% of the per-area waste score's variance is within-province (34% per household). | variance share; 10.7× vs 10.9× | NB "Denominator decomposition" | Normalized per area is not usable for DiD; raw per area is | Causal | settled | ☐ |
| D14 | In logs of raw quantities: waste collected +0.260 (~30%, p < 0.0001); per household +27%; per capita +23%; household count +2% (p = 0.37); household size +3% (p = 0.21). | log DiD | NB "Denominator decomposition" | The effect is in the numerator | Causal | settled | ☐ |
| D15 | Implied municipal coverage share rises +0.259 in logs, matching waste (+0.260), ratio 1.00, same yearly path. Waste per covered resident did not change. | log DiD | NB | Coverage is derived from TÜİK water figures, waste is independent | Causal | settled | ☐ |
| D16 | Law 6360's clearest statistical footprint is the extension of municipal service coverage (administrative reach), not household burden or agricultural outcomes. | D13–D15 | n/a | [INT] | Causal, Discussion | Orhan | ☐ |
| D17 | Size-matched controls (14 largest non-metros): no size overlap (largest control Afyonkarahisar 704k < smallest treated Ordu 741k); estimate −0.035 (p = 0.013, bootstrap p = 0.016); coverage ratio 1.06. | 28 clusters | NB size-matched section | "Size alone doesn't produce the result, with the nearest available controls"; an overlapping control group can't be built | Causal | settled | ☐ |
| D18 | Population differential about 5% (+0.051 log); 2008 pre-coefficient −0.027 (p = 0.004). Size-matched: +0.071; −0.029 (p = 0.060). | | NB | Small vs. the ~30% coverage jump; stated limitation | Causal | settled | ☐ |
| D19 | Water: DiD −0.168 (p = 0.0001, normalized). In logs, waste fades 3% (2014–18 vs 2020–24: 0.257 → 0.249; a permanent shift) and water fades 23% (2014–18 vs **2020–22**, water's last published year; confirmed by econometrics 2026-10-07). Never say "over the same windows". Waiver is possible for water, not supported by waste. | | NB water section | Water vs. coverage not cleanly testable; COVID overlaps 2020 | Causal | settled | ☐ |
| D20 | Wild cluster bootstrap for all six specifications, all significant: primary p = 0.004, size-matched 0.016, flat 0.002, TOPSIS 0.005, per capita 0.007, waiver-excluded 0.025. Dropping data-quality outlier provinces: −0.0370 vs −0.0373. | bootstrap p | NB "Update 2026-10-01" | | Causal | settled | ☐ |
| D21 | Verdict on the hypothesis: the composite falls, but the fall is municipal coverage; measured agricultural components show no consistent reduction. | D2, D6, D7, D15 | n/a | [INT]. Not "no effect", not "6360 did not reduce food sovereignty" | Causal, Discussion | Orhan writes | ☐ |

## E. Confounds and limitations

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| E1 | Implied municipal coverage 2012 → 2014: non-metro −0.020, new-metro +0.226 (about 73% → 96%), old-metro +0.089 (90% → 99%). | coverage shares | NB diagnostics | | Measure, Causal | settled | ☐ |
| E2 | Old-metro provinces are a contaminated control for municipal variables (they got a weaker version of the same boundary change) but usable for agricultural ones. | E1 | NB | | Causal | settled | ☐ |
| E3 | Tariff waiver 2014–2019: converted villages paid no taxes/fees; drinking water capped at 25% of the lowest municipal tariff (Çelikyay, 2014, SETA Analiz 101). | legal / secondary | n/a | The water variable is household network supply, so the waiver is a real open confound for water | Law6360, Causal | verify source | ☐ |
| E4 | Only three pre-treatment points (2008, 2010, 2012). | panel | n/a | Parallel trends can't be confirmed strongly | Causal | settled | ☐ |
| E5 | Treatment was assigned by a population threshold, so no size-overlapping control exists. | D17 | NB | | Causal | settled | ☐ |
| E6 | Province is coarser than the reform's mechanism (abolishing village legal personality acts at village/district level). | design | n/a | Limitation paragraph, not a task | Causal, Discussion | settled | ☐ |
| E7 | 2020 is a COVID year. | | n/a | Overlaps the waiver's end | Causal | settled | ☐ |
| E8 | Smallholder effects may be masked by province aggregates. | | n/a | Parked by decision; limitation only | Discussion | settled | ☐ |
| E9 | The water variable is "İçme ve kullanma suyu şebekesi ... Toplam çekilen su miktarı": municipal household supply, no irrigation. | TÜİK source column | NB raw column | | Measure | settled | ☐ |
| E10 | Per household drifts about 6% against old-metro (safe against non-metro: −0.045 on ~3.2). | | NB | | Measure | settled | ☐ |
| E11 | Fertilizer: Hakkari missing 2020/2022/2024 (3 of 738 province-years). | | NB merge cell | | Measure | settled | ☐ |

## F. Official Gazette

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| F1 | All Gazette titles 2000–2024 were scraped and validated against the earlier outputs at 94.2–99.8% text match per year; one silently dropped day (2020-08-27) was found and recovered. | per-year diff | `resmigazete_module.py`; numbers in RGN Part 2 | Baseline files deleted; validation can't be re-run | Discourse (methods) | settled | ☐ |
| F2 | Of 112,157 titles (2000–2024), 195 mention *büyükşehir* or 6360, 2,416 mention *tarım*, 0 mention both. | counts | RGD | **Titles only**: can't show the domains are disjoint in the body text | Discourse | settled | ☐ |
| F3 | The PDF reported 2,398 *tarım* entries (27 June 2000 – 7 June 2024) vs. 2,416 in F2. | | PDF p.12 vs RGD | Different window/run; say which is used | Discourse | open: reconcile | ☐ |
| F4 | Relevance classification: two hand-annotated batches (479, 384), accuracy 95.62% / 96.61%; the remaining 1,241 predicted; 546 relevant: 266 international, 280 domestic. | | older pipeline (PDF p.13) | Locate the code/files that reproduce this | Discourse | **verify reproducible** | ☐ |
| F5 | International items: 161 tariff quotas, 80 collaborations, 9 concessions, 1 partnership, 7 IPARD/IFAD, 3 chemical fertilizer, 4 import rules. | | annotation files | | Discourse | settled | ☐ |
| F6 | Clustering: TF-IDF silhouette max 0.30 (180 clusters), 0.20 at 50; BERTopic 22 topics, silhouette 0.17. Rewrite as "clustering showed X, so annotation + classification" (Ali Hoca comment 5). | | old notebooks | Locate reproducing code | Discourse (methods) | verify | ☐ |
| F7 | Category counts are exact (full population) but sparse: Supports median 11/year, Agreements 8/year; 42 of 125 year × group cells empty. | | RGD | Exact as description, weak as inference | Discourse | settled | ☐ |
| F8 | Composition before vs. after 2012 (98 vs. 175 items): resource control falls 9.6% → 5.7%, market integration rises 33.7% → 44.6%. | | RGN | **Do not cite yet**: rests on an AI-proposed grouping you haven't adopted; resource control n = 20 | Discourse | Orhan (adopt grouping or not) | ☐ |
| F9 | Body text is collectable (post-2005 `.htm`); 116 metropolitan and 3,121 agricultural items could be fetched in under an hour. | probe | RGN | Optional: only if the discourse chapter needs a full-text test | Discourse | Orhan (optional) | ☐ |
| F10 | The recall of the *tarım* keyword filter. | | `resmigazete_keyword_recall.py` | Check whether it was measured | Discourse | verify | ☐ |

## G. Ministry news

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| G1 | 7,107 pages scraped; 6,492 usable articles (559 dead URLs, 56 extraction misses). | counts | `agroforestministry_news.csv`; AMN | Quote 6,492 as corpus size | Discourse | settled | ☐ |
| G2 | The archive starts in 2013, so this source has no pre-law baseline. | | AMN | | Discourse | settled | ☐ |
| G3 | Publication volume is very uneven: 1,043 articles in 2017 vs. 103 in 2014. | per-year counts | AMN (locate the script) | Counts partly measure publishing behavior | Discourse | verify script in repo | ☐ |
| G4 | A 500-article stratified sample was classified by an LLM against a category codebook. | | `..._CLAUDE_LABELS.csv` | No human ground truth yet | Discourse | settled | ☐ |
| G5 | Human validation: 150–200 stratified rows, Cohen's kappa against the LLM labels. | | `annotate_tool.py` | **Required** before any ministry-news number is reported | Discourse | **open: Orhan annotates** | ☐ |
| G6 | 4 of 500 articles connect Law 6360 to agriculture (Metropolitan_Law category), measured on full text; one is a buried quote in an agricultural fair article. | | CLAUDE_LABELS | Conditional on G5 | Discourse | open (after G5) | ☐ |
| G7 | Per-year category rates are not supportable (95% CI ±10 to ±19 points; ~293 articles/year needed; four years don't contain that many). | Wilson CIs | AMN | Use raw counts per year only | Discourse (methods) | settled | ☐ |
| G8 | Category name: `Metropolitan_Law` here, `Buyuksehir_Law` in the literature codebook. | | | Use one name in the thesis | Discourse | settled | ☐ |

## H. Discourse and theory

| ID | Claim | Evidence | Computed in | Scope limit | Ch | Status | ✓ |
|---|---|---|---|---|---|---|---|
| H1 | The state frames Law 6360 as administrative/municipal reform (efficiency, service scale). | the law's *genel gerekçe* (preamble) | primary source | Quote it | Law6360, Discourse | **open: find and quote** | ☐ |
| H2 | ZMO (*Ziraat Mühendisleri Odası*, Chamber of Agricultural Engineers, a member chamber of TMMOB), 48th General Assembly declaration, explicitly links 6360 to agriculture: village assets transferred to municipalities, aging villages, call for review. | zmo.org.tr declaration | primary source | Verify date and wording. **Cite as ZMO everywhere** (Orhan, 2026-10-05) | Discourse | verify | ☐ |
| H3 | Official silence vs. professional-body critique: the agricultural reading of 6360 comes from outside the state. | F2, G6, H2 | n/a | [INT] | Discourse, Discussion | Orhan | ☐ |
| H4 | Discursive absence is not causal absence: whether 6360 affected agriculture is a question for the panel, not the texts. | | n/a | Must accompany H3 every time | Discourse | settled | ☐ |
| H5 | The two text measurements are not equal evidence: ministry news is full text (stronger); Gazette is title-only. | | n/a | Never present them as converging peers | Discourse | settled | ☐ |
| H6 | Legibility: the state counts output, not control (B4), and doesn't discuss 6360 as agricultural policy (H3). One argument about what the state makes visible. | B4, H3 | n/a | [INT]; Scott to be read before citing | Discussion | Orhan writes | ☐ |
| H7 | Windows: 2000–2012 Gazette only; 2013–2024 both sources; 2025–2026 news only; 2026 partial. | | n/a | State the supported window on any combined chart | Discourse | settled | ☐ |
| H8 | Gazette and news data are national-yearly, collinear with year fixed effects, so they can't enter the DiD. Their role is interpretive. | | n/a | | Discourse | settled | ☐ |
| H9 | Both sources measure policy activity, not attitudinal commitment, and both are state self-reporting. | | n/a | Required caveat for any GFSI "political commitment" comparison | Discourse | settled | ☐ |

## I. Superseded claims: must not reappear

| ID | Old claim (where) | Replaced by |
|---|---|---|
| I1 | Old-metro > new-metro > non-metro (PDF Fig. 1, p.17–18) | C1, C2 |
| I2 | "The greatness of a city correlates with domestic food production" (PDF p.18) | drop |
| I3 | National loss of food sovereignty after 6360 (PDF abstract, p.18, p.20, p.21) | C7 |
| I4 | "Law 6360 has no direct effect" from ANOVA p = 0.43, t-test p = 0.35 (PDF p.18) | D2, D6, D7, D21 |
| I5 | Six categories incl. "Energy"; plain min-max; 2008–2018 (PDF p.16–17) | B9–B16, B20 |
| I6 | Water and waste carry low weight (PDF Fig. 2, p.19) | D6, D7 |
| I7 | Gazette text out of scope because PDFs need OCR (PDF p.12, p.21) | F9 |
| I8 | "p should be lower than 0.05, therefore no effect" (PDF p.18) | style guide rule |
| I9 | "First of its kind" with one citation (PDF p.20) | support with a literature search or drop |
| I10 | "kredi faiz indirimi" = "tax rate reductions" (PDF p.14) | "credit interest rate reductions" |
| I11 | "Idib." (p.8), "undermined" for "undertaken" (p.1) | typos |
| I12 | Law 6360 as "a control variable" (`thesis_draft.md` line 1) | the treatment (A2) |
| I13 | "Fourteen cities" by Law 6360 (PDF p.2, p.20) | A4 |

Note: the PDF's 2013 cutoff and the current "Post = 2014 onward" are the same split for biennial
data (2012 is pre, 2014 is post), so that one is not a conflict.

---

## Open items, collected

**Your decisions**
- B24: municipal burden inside the index or reported separately (take to Ali Hoca).
- F8: adopt the Gazette five-group scheme or not.
- F9: optional Gazette body-text collection.
- A1, B23, D16, D21, H3, H6: interpretations you write.

**Your work**
- G5: human validation of 150–200 ministry-news rows.
- B5: correct the draft elimination reasons in `tables/indicator_attrition_draft.xlsx`.

**To verify or reconcile (I can do most of these)**
- A3, A4, E3, H1, H2: primary legal/secondary sources.
- D5: re-read from the notebook.
- F3, F4, F6, F10, G3: locate the code that reproduces the number.
- B1: the list of 32 papers.

**For other agents (via the main agent)**
- none open.
