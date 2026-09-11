> **Agent note.** Written by a Claude Code sub-agent operating on this folder
> (`econometric_models_and_vars`), documenting pipeline structure it implemented in
> `fsoi_indicator_selection.ipynb`. This is a technical record, not analysis or thesis prose —
> review before citing or incorporating into the written thesis. Human draft notes live in
> `Variable_Analysis_Methods/`.

## Status & Forward Steps (2026-09-11) — read this first

**Done:** main/extended dataframe split; `Treated` 4-category categorical + labels; correlation/
redundancy groundwork on both dataframes (one near-duplicate pair resolved and dropped);
methodology grounded in Yilmaz (2025, Entropy-TOPSIS) and GFSI (2022) — decided simple-mean
sub-indices over PCA, pooled+per-year winsorized min-max over z-score; FSOI positioned as a
critical comparative index to GFSI; cross-strand categorical question resolved — **FSOI stays
at 6 categories** (market, production, water, waste, energy, land-use), no political category.

**Blocking everything below:** benefit/cost direction for water, waste, energy, and land-use
fallow — see "Open item" further down for the per-category table and recommendation. Waiting
on Orhan; not yet decided as of 2026-09-11.

**Forward plan once unblocked** (full detail in "Synthesized pipeline plan" below):
1. Normalize the 4 leftover columns in main (plan agreed, not yet coded).
2. Build simple-mean sub-indices for the remaining collapse candidates.
3. `log1p` skewed indicators, then normalize (pooled + per-year, winsorized min-max).
4. Aggregate into the 6 category sub-indices, documented inline.
5. Compare equal-weighted sum vs. TOPSIS, and benefit/cost sensitivity, at category level.
6. Produce the FSOI composite + top/bottom example cities — the "durable result" that triggers
   reporting back to `thesis_log_main_agent` for its CLAUDE.md Results-status update.

Not this session's work: Gazette/Ministry-news become a national-level companion analysis, not
a composite input (see "Cross-strand note" below).

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

## `data_official_Türkiye` (main panel — full 2008–2024 coverage)

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
  checked here at all.

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
   money/volume indicators, before any normalization.
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

### Open item — benefit/cost direction per category (blocks steps 2 and 5 above)

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
question aside — **confirmed for agroministrynews_agent (Orhan declined NER city-tagging), but
still pending for officialgazette_agent** (main agent asked directly, hadn't heard back as of
2026-09-11 — this was an inference from the old thesis PDF description, not yet verified). Even
if Gazette data turns out to be city-level after all, reason (1) alone is enough to keep it out
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
