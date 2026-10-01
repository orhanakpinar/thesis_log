# 5. How Food Sovereignty Is Distributed

<!--
HOLD (2026-10-01): Orhan dropped the animal-product value indicator from the index (data break;
moved to Appendix B). The full index is now 13 indicators, and EVERY full-index number in this
chapter (Tables 5.1–5.5, top/bottom provinces, group means, TOPSIS comparison, trends) must be
recomputed from the rebuilt export before this chapter is used. §5.3's decline discussion will
largely move to Appendix B. Long-panel numbers are unaffected (no market category).
-->

<!--
WORKING DRAFT v1, agent-written for Orhan to rewrite. Markers as in Chapter 4:
  [INT] interpretation · [CITE: x] citation to supply · [VERIFY] fact to check · [FIGURE] to produce
Every number is computed by writing_drafts/scripts/descriptive_tables.py from the FSOI exports
(econometric_models_and_vars/fsoi_track_{C,A}_perHousehold.csv), except the TOPSIS comparison
(notebook, "Claims-ledger checks"). Ledger rows: C1–C9, plus new rows C10–C13.
-->

This chapter describes the Food Sovereignty Index as it stands: how scores are spread across
provinces, how the three groups of provinces compare, and how scores changed over time. It is
descriptive. Differences between groups here are not estimates of the effect of Law 6360; that
question is taken up in Chapter 6 with a design built for it. Unless stated otherwise, the
chapter uses the full index (five categories, 2008–2020) with the primary specification: per
household, equal category weights, cost framing (Table 4.3).

## 5.1 The distribution across provinces

In 2020 the average province scored 0.474 on the full index. Scores ranged from 0.328
(Şanlıurfa) to 0.620 (Iğdır), with a standard deviation of 0.066. This spread was stable over
the period: the standard deviation stayed between 0.060 and 0.068 in every panel year.

![Figure 5.1](../../econometric_models_and_vars/thesis_outputs/fig_5_1_full_index_2020_map.png)

**Figure 5.1.** Full-index scores by province, 2020. New-metropolitan provinces are outlined.
*Source:* TÜİK, Ministry of Agriculture and Forestry; boundaries: HDX `cod-ab-tur` (Harita
Genel Müdürlüğü), CC BY-IGO; author's calculations.

**The top of the distribution.** All ten highest-scoring provinces in 2020 are
non-metropolitan: Iğdır, Bayburt, Burdur, Amasya, Ardahan, Kastamonu, Muş, Tokat, Çanakkale and
Gümüşhane. [INT] Most are small, predominantly rural provinces in the east, the Black Sea
region and inner Anatolia, where agriculture carries a large share of household life and
municipal service loads per household are light.

**The bottom of the distribution** is more mixed: four old-metropolitan provinces (Kocaeli,
Konya, Diyarbakır, İstanbul), three new-metropolitan provinces (Hatay, Mardin, Şanlıurfa) and
three non-metropolitan provinces (Yalova, Batman, Şırnak). The category scores show that
provinces reach the bottom by two opposite routes (Table 5.1).

**Table 5.1.** Category scores of the ten lowest-scoring provinces, full index, 2020.

| Province | Production | Land use | Market | External input | Municipal burden | FSOI |
|---|---:|---:|---:|---:|---:|---:|
| Kocaeli | 0.084 | 0.216 | 0.049 | 0.970 | 0.578 | 0.379 |
| Yalova | 0.057 | 0.237 | 0.084 | 0.963 | 0.545 | 0.377 |
| Konya | 0.451 | 0.336 | 0.484 | 0.063 | 0.547 | 0.376 |
| Diyarbakır | 0.262 | 0.317 | 0.415 | 0.405 | 0.457 | 0.371 |
| İstanbul | 0.007 | 0.201 | 0.000 | 0.994 | 0.577 | 0.356 |
| Hatay | 0.195 | 0.318 | 0.194 | 0.601 | 0.467 | 0.355 |
| Mardin | 0.296 | 0.382 | 0.368 | 0.126 | 0.570 | 0.348 |
| Batman | 0.183 | 0.285 | 0.331 | 0.655 | 0.280 | 0.347 |
| Şırnak | 0.214 | 0.272 | 0.333 | 0.687 | 0.188 | 0.339 |
| Şanlıurfa | 0.346 | 0.373 | 0.450 | 0.000 | 0.471 | 0.328 |
| *Median, all provinces* | *0.298* | *0.314* | *0.330* | *0.790* | *0.688* | *0.475* |

*Note.* Higher scores mean more food sovereignty in every column; cost indicators are already
reversed. *Source:* computed from the full-index export.

The first route is urbanization. İstanbul, Kocaeli and Yalova produce very little per household
and realize little market value, but they also use few purchased agricultural inputs, so they
score near the top on external input. The second route is intensive agriculture. Konya,
Şanlıurfa and Mardin produce and earn above the national median, yet score near zero on
external input: their agriculture depends heavily on fertilizer and on electricity, much of it
for irrigation [VERIFY: irrigation as the main driver of agricultural electricity in Şanlıurfa
and Konya]. A third, smaller pattern appears in Şırnak and Batman, where low production is
combined with a low municipal burden score.

[INT] These opposite routes illustrate the averaging limitation discussed in Section 4.2.4: the
same low score can hide very different profiles, which is why category scores are reported
alongside the composite. They also show the index working as its framing intends. Two of
Türkiye's most productive agricultural provinces, Konya and Şanlıurfa, score low not because
they produce little, but because their production depends on purchased inputs. A food security
index would rank them high. The FSOI ranks them low because dependence counts against
sovereignty. Whether that is the right judgment is a question about the concept, and the thesis
returns to it in Chapter 8.

## 5.2 The three groups of provinces

Table 5.2 shows the average full-index score of each group of provinces over time, with the
national aggregate for reference.

**Table 5.2.** Mean full-index score by group of provinces, 2008–2020.

| Year | Non-metropolitan (51) | Old-metropolitan (16) | New-metropolitan (14) | Türkiye (aggregate) |
|---|---:|---:|---:|---:|
| 2008 | 0.511 | 0.458 | 0.474 | 0.479 |
| 2010 | 0.533 | 0.475 | 0.496 | 0.496 |
| 2012 | 0.515 | 0.465 | 0.478 | 0.497 |
| 2014 | 0.515 | 0.459 | 0.452 | 0.482 |
| 2016 | 0.497 | 0.430 | 0.424 | 0.459 |
| 2018 | 0.505 | 0.437 | 0.425 | 0.462 |
| 2020 | 0.500 | 0.433 | 0.424 | 0.454 |

*Note.* Unweighted means across provinces in each group. The national aggregate is Türkiye's
own score on the same scale, not the mean of the provinces. *Source:* computed from the
full-index export.

![Figure 5.2](../../econometric_models_and_vars/thesis_outputs/fig_5_2_group_means_over_time.png)

**Figure 5.2.** Mean index score by group of provinces over time, full index (2008–2020) and
long-panel index (2008–2024). The shaded band marks Law 6360, passed in 2012 and in force from
2014. *Source:* author's calculations.

**Which result is robust.** Under the primary specification, non-metropolitan provinces score
highest in every year. But this ordering depends on how the index is aggregated. Under TOPSIS,
old-metropolitan provinces lead in 2020, although only narrowly (0.313 against 0.306 for
non-metropolitan provinces). The ordering of these two groups is therefore not a finding about
the provinces. It is also sensitive to the data: the break in the animal-product value series
(Section 5.3) lowers old-metropolitan provinces' market scores more than those of the other
groups, which works against old-metropolitan provinces in exactly this comparison. What does
hold across every view tried is that new-metropolitan provinces are
the lowest group or tied for lowest. The only tie occurs when all years from 2008 to 2020 are
pooled: new-metropolitan provinces then average 0.453 and old-metropolitan provinces 0.451.

**A change in position around the reform.** Before Law 6360, new-metropolitan provinces scored
above old-metropolitan provinces in every panel year (for example 0.478 against 0.465 in 2012).
From 2014 onward they scored below them (0.452 against 0.459 in 2014, 0.424 against 0.433 in
2020). [INT] The timing coincides with the reform, but a descriptive comparison cannot say
whether the reform caused it. The old-metropolitan provinces were themselves affected by the
same law, which extended metropolitan boundaries in their provinces as well, and the groups
differ in many ways besides their status. Chapter 6 tests the question with a
difference-in-differences design against non-metropolitan provinces.

**Where the group differences come from.** Table 5.3 breaks the 2020 group means into their
categories.

**Table 5.3.** Mean category scores by group, full index, 2020.

| Group | Production | Land use | Market | External input | Municipal burden | FSOI |
|---|---:|---:|---:|---:|---:|---:|
| Non-metropolitan | 0.303 | 0.318 | 0.382 | 0.751 | 0.744 | 0.500 |
| Old-metropolitan | 0.290 | 0.310 | 0.248 | 0.755 | 0.563 | 0.433 |
| New-metropolitan | 0.266 | 0.323 | 0.301 | 0.694 | 0.536 | 0.424 |

*Source:* computed from the full-index export.

Production and land use differ little between the groups; the largest gap in either is 0.037.
The groups separate mainly on two categories. On municipal burden, non-metropolitan provinces
score about 0.2 higher than both metropolitan groups, meaning lighter measured municipal
service loads per household. On market, non-metropolitan provinces score highest and
old-metropolitan provinces lowest. [INT] The municipal burden gap is the one to watch: the
metropolitan groups are exactly the provinces whose municipal boundaries Law 6360 redrew, and
Chapter 6 shows that this category carries the reform's measurable effect.

## 5.3 Change over time

**The full index declines, and the decline is in dollar value.** Across all provinces, the mean
full-index score fell from 0.494 in 2008 to 0.474 in 2020, and 68% of provinces ended the
period lower than they started. Table 5.4 shows where the decline comes from.

**Table 5.4.** Mean category scores across provinces, full index, 2008–2020.

| Year | Production | Land use | Market | External input | Municipal burden | FSOI |
|---|---:|---:|---:|---:|---:|---:|
| 2008 | 0.266 | 0.337 | 0.466 | 0.790 | 0.612 | 0.494 |
| 2012 | 0.280 | 0.327 | 0.458 | 0.774 | 0.656 | 0.499 |
| 2016 | 0.282 | 0.318 | 0.365 | 0.742 | 0.648 | 0.471 |
| 2020 | 0.294 | 0.317 | 0.342 | 0.742 | 0.672 | 0.474 |
| Contribution to the 2008–2020 change | +0.006 | −0.004 | −0.025 | −0.010 | +0.012 | −0.021 |

*Note.* The contribution of a category is its change divided by five, since each category is
one-fifth of the index; contributions sum to the change in the FSOI. Intermediate years are in
the script output. *Source:* computed from the full-index export.

The decline is driven by the market category, which fell from 0.466 to 0.342 and on its own
lowered the index by 0.025. The other four categories roughly cancel out (together +0.004):
external input and land use fell slightly, while production rose, and the municipal burden
score rose, meaning that measured municipal service load per household fell. Production
measured in tons therefore grew while the measured value of production fell.

Two features of the market data, rather than a change in the provinces, explain the market
decline. The first is a break in the source series. TÜİK's provincial values for animal
products add up to the national total in 2008 and 2010, but to only 38–60% of it from 2012 on
(Section 4.2.1). This break is also what produces the market peak in 2010 in Table 5.4. The
under-count is not uniform across provinces. The ratio of provincial to national value after
2012 ranges from about 0.25 (10th percentile) to 0.57 (90th percentile), with poultry-producing
provinces hit hardest (Bolu 0.05, Manisa 0.10). It also differs by group: 0.36 for
old-metropolitan, 0.43 for new-metropolitan and 0.46 for non-metropolitan provinces (a
Kruskal–Wallis test rejects equal distributions, p = 0.025). The
second is the currency. Market values are converted to US dollars, and the lira depreciated
steeply against the dollar over these years [CITE: Central Bank exchange-rate series]. Table
5.5 shows the 2008–2020 change in the mean full-index score under four versions of the market
category.

**Table 5.5.** Change in mean full-index score, 2008–2020, under four versions of the market
category.

| Market category measured as | Change in FSOI, 2008–2020 |
|---|---:|
| US dollars, as built | −0.021 |
| US dollars, without animal products | −0.014 |
| Relative to the national value in each year | −0.003 |
| Relative to the national value, without animal products | +0.004 |

*Source:* econometrics notebook, "Update 2026-10-01" checks.

Once market values are expressed relative to the national total each year, which removes both
the currency and the national level of the series, the decline almost disappears, and without
animal products it turns slightly positive. [INT] The full-index decline is therefore not a
decline in food sovereignty, nor a sign that provinces drifted apart. It comes from the dollar
and from a break in one source series. New-metropolitan provinces remain the lowest group in
2020 under all four versions. The animal-product series stays in the index as published, with
this limitation stated; the causal analysis in Chapter 6 uses the long-panel index, which has
no market category and is therefore unaffected by the break. [INT] A weaker lira may well affect
food sovereignty at the national level, for example by raising the cost of imported inputs, but
the FSOI cannot measure that: the conversion applies one rate to every province, so it carries
no information about differences between them.

**The long-panel index shows no decline.** The long-panel index, which has no market category,
rises slightly between 2008 and 2024 in all three groups: by 0.030 in non-metropolitan, 0.013 in
new-metropolitan and 0.010 in old-metropolitan provinces. A trend regression on this index finds
a small, statistically significant increase when municipal burden is included and no trend
without it (Chapter 6 reports the estimates).

[INT] The two indices therefore agree once the market category is set aside: measured in
physical terms, Turkish provinces show no general decline in the material base of food
sovereignty over this period. An earlier, preliminary version of this study reported a
national loss of food sovereignty after 2012. That index was built differently and cannot be
reproduced from the current pipeline, so the two results cannot be compared directly. The
checks above suggest why the earlier result may have appeared: an index that includes output
valued in dollars, from a series with a coverage break, will register both as a decline.
[INT — you decide whether to mention the preliminary study at all; the jury may know it]

**Provinces keep their relative positions.** The rank order of provinces in 2020 is close to
that of 2008 (rank correlation 0.79). Movements in the index are mostly shared across provinces
rather than reshuffling them.

## 5.4 Summary

Food sovereignty, as the FSOI measures it, is highest in small, rural non-metropolitan
provinces and lowest in two very different kinds of province: urban-industrial provinces that
produce little, and intensive agricultural provinces whose production depends on purchased
inputs. New-metropolitan provinces are the lowest or tied-lowest group in every specification
tried, and they moved from above to below old-metropolitan provinces at the time of Law 6360,
while which of the other two groups ranks highest depends on the aggregation method. The main
differences between groups lie in municipal burden and market value, not in production or land
use. Over time, the full index declines, but the decline comes from the market category's
currency conversion and a break in one source series; measured relative to national values,
and in the long-panel index, there is no general decline. These are descriptive patterns. Chapter 6 asks which of them, if any, can be attributed
to Law 6360.

---

## Suggested citations for Chapter 5

- Central Bank of the Republic of Türkiye (TCMB), exchange rate series (EVDS), for the lira's
  depreciation against the dollar. Data source, not literature.
- No new literature is needed; Chapter 5 cites Chapter 4 for methods.

## Figures

Both figures are produced by the econometrics notebooks at 300 dpi in
`econometric_models_and_vars/thesis_outputs/` and linked above.
