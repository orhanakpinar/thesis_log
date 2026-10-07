# Appendix B. The Animal-Product Value Series

<!--
WORKING DRAFT, agent-written for Orhan to rewrite. Holds the material removed from Chapters 4
and 5 when animal-product value was dropped from the index (Orhan, 2026-10-01). Numbers from the
econometrics notebook, sections "Update 2026-10-01" and "Chapter 6 outputs and the
animal-product break"; the with/without table is still to be delivered.
-->

The value of animal products (TÜİK, *Hayvansal ürünler değeri*) met every selection condition in
Section 4.1.3 and was part of the market category in an earlier version of the index. It was
excluded because its provincial series does not match the national series. This appendix
documents the problem and shows how the main results change with the indicator included.

## B.1 The break

Provincial values of animal products add up to the national total in 2008 and 2010. From 2012
onward they add up to only 38–60% of it (Table B.2).

**Table B.2.** Sum of provincial animal-product values as a share of the national value.

| 2008 | 2010 | 2012 | 2014 | 2016 | 2018 | 2020 |
|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 1.000 | 0.385 | 0.604 | 0.436 | 0.492 | 0.554 |

*Source:* TÜİK; `econometric_models_and_vars/thesis_outputs/table_B2_animal_products_break.csv`.

The share also moves from year to year after the break, so the undercount is not even a stable
proportion over time. The national figure itself continues without a break,
growing by a factor of about 1.06 between 2010 and 2012, while the sum of provincial values falls
to about 0.41 of its earlier level. The provincial series, not the national one, is undercounted.
The crop and live-animal value series show no such break: their provincial values add up to the
national total in every year.

The undercount is not uniform across provinces. After 2012, the ratio of a province's value to
what it would be at full coverage ranges from about 0.25 (10th percentile) through 0.45 (median)
to 0.57 (90th percentile). Poultry-producing provinces are hit hardest, for example Bolu (0.05),
Manisa (0.10) and Sakarya (0.13). The ratio also differs by group: 0.36 for old-metropolitan,
0.43 for new-metropolitan and 0.46 for non-metropolitan provinces (Kruskal–Wallis test,
p = 0.025).

[VERIFY: the exact definition of the per-province ratio, so this paragraph describes it
correctly]

[CITE: TÜİK metadata, if the cause can be confirmed. A governorate yearbook footnote suggests
that meat, poultry, eggs and hides were excluded from the provincial series from 2011; this is
not verified at TÜİK and must not be cited until it is.]

## B.2 Why the series was excluded

A series that undercounts provinces by different amounts would distort two things the FSOI is
used for. Over time, it produces a drop in market scores from 2012 that reflects the series, not
the provinces; it is also what produced a market peak in 2010 in the earlier version. Between
groups, it lowers old-metropolitan provinces more than the others, which affects exactly the
comparison between non-metropolitan and old-metropolitan provinces that Chapter 5 already finds
sensitive to method.

## B.3 Results with and without the series

Province rankings on the full index with and without animal products agree closely: the rank
correlation is between 0.983 and 0.989 in every year.

**Table B.1.** Main full-index results with and without animal-product value.

| Result | With animal products | Without (used in the thesis) |
|---|---|---|
| 2020 group means (non / old / new) | 0.500 / 0.433 / 0.424 | 0.511 / 0.446 / 0.439 |
| Change in mean FSOI, 2008–2020 | −0.021 | −0.014 |
| New-metropolitan lowest group, 2020 | yes | yes |
| Rank correlation between the two versions | 0.983–0.989 across years (0.989 in 2020) | |
| Top-10 provinces, 2020 | 9 of 10 shared (Gümüşhane in this version only) | 9 of 10 shared (Antalya in this version only) |
| Bottom-10 provinces, 2020 | 10 of 10 shared | 10 of 10 shared |

*Source:* `econometric_models_and_vars/thesis_outputs/table_B1_full_index_with_without_animal_products.csv`.

The exclusion changes the levels slightly but none of the conclusions of Chapter 5. The
long-panel index used for the causal analysis in Chapter 6 has no market category and is not
affected.

## B.4 The earlier decline result

With animal products included, the mean full-index score fell by 0.021 between 2008 and 2020.
Four versions of the market category showed where that decline came from:

| Market category measured as | Change in FSOI, 2008–2020 |
|---|---:|
| US dollars, as built | −0.021 |
| US dollars, without animal products | −0.014 |
| Relative to the national value in each year | −0.003 |
| Relative to the national value, without animal products | +0.004 |

Once market values are expressed relative to the national total each year, which removes both
the currency conversion and the series break, the decline almost disappears. The decline was
therefore not a decline in food sovereignty. [INT — this may stay in Chapter 5 in a short form;
decide when Chapter 5 is rewritten]
