# The difference-in-differences, in plain words

A study aid for Orhan before Chapter 6. Not thesis text. Numbers from `claims_ledger.md`
(section D); illustrative numbers are marked as such.

## 1. The question

Did Law 6360 change the FSOI of the 14 new-metropolitan provinces?

To answer, we would need to know what their FSOI **would have been without the law**. That world
doesn't exist, so we can't see it. Every causal method is a way of estimating that missing world.

## 2. Two simple answers, and why each fails

- **Before vs. after, new-metro only.** Compare new-metro provinces in 2012 with 2020. Problem:
  many things changed between 2012 and 2020 for *every* province: the lira, the weather, COVID,
  national farm policy. A before–after difference mixes the law with all of that.
- **New-metro vs. others, after only.** Compare new-metro with non-metro provinces in 2020.
  Problem: these groups were different long before the law. New-metro provinces are bigger and
  more urban. A gap in 2020 could have existed in 2008 too.

## 3. The idea: difference in differences

Use the **change** in non-metro provinces as the stand-in for what would have happened to
new-metro provinces without the law.

| (illustrative numbers) | Before (2008–2012) | After (2014–2024) | Change |
|---|---:|---:|---:|
| New-metro | 0.48 | 0.46 | −0.02 |
| Non-metro | 0.50 | 0.52 | +0.02 |
| **Difference in the changes** | | | **−0.04** |

Both groups were hit by the lira, COVID and national policy. Subtracting the non-metro change
removes what they share. What's left is the part of the new-metro change that non-metro
provinces *didn't* experience, which is our estimate of the law's effect.

## 4. The one assumption everything rests on

**Parallel trends:** without the law, new-metro and non-metro provinces would have moved in
parallel. They can differ in *level* (one higher than the other); what matters is that they'd
have changed at the same *pace*.

It can't be proven, because it's about the world we can't see. It can be checked partly: if the
two groups moved in parallel *before* the law (2008 → 2010 → 2012), that's reassuring. Our check:
the pre-law differences in 2008 and 2010 are not significant. **But three time points is a weak
test.** Say this plainly; don't oversell it.

## 5. The pieces of the model, in words

- **Province fixed effects** absorb everything permanent about a province: Konya is always
  large, Iğdır always small. The model only looks at how each province changes relative to
  itself.
- **Year fixed effects** absorb everything that hit all provinces in the same year: the lira in
  2018, COVID in 2020.
- **The effect** is the extra change in new-metro provinces from 2014 onward, beyond both.
- **Why non-metro provinces as the comparison, not old-metro?** Law 6360 also redrew municipal
  boundaries in old-metro provinces, more weakly. They were partly "treated" too, so they can't
  show the world without the law.
- **Clustered standard errors:** a province's years are not independent observations (Konya in
  2016 resembles Konya in 2018), so uncertainty is computed per province, not per data point.
- **Wild cluster bootstrap:** with only 14 treated provinces, ordinary p-values can look better
  than they are. The bootstrap is a check designed to catch exactly that. It didn't: p = 0.004,
  the same as the ordinary p = 0.003.

## 6. What we found

**Step 1, the headline:** the long-panel index fell by **0.037** more in new-metro than in
non-metro provinces after 2014 (95% CI −0.062 to −0.012). Taken at face value: the law lowered
food sovereignty.

**Step 2, but where?** Run the same model on each category alone:

| Category | Effect | Reading |
|---|---:|---|
| Municipal burden (waste) | −0.175 | large, clear |
| Land use | −0.023 | small, real, worse for new-metro |
| External input (fertilizer) | +0.048 | small, real, *better* for new-metro |
| Production | −0.0002 (CI −0.022 to +0.022) | nothing, and a tight nothing |

Remove municipal burden and the composite effect disappears (+0.009, not significant). **The
whole headline is municipal burden.**

**Step 3, what is municipal burden actually showing?** In the long-panel index it's waste
collected per household. Look at the raw numbers in logs:
- waste collected rose about **30%** more in new-metro provinces;
- the number of households barely moved (+2%, not significant);
- the **share of the population covered by municipal services** rose by almost exactly the same
  amount as waste (log +0.259 vs +0.260).

So municipalities weren't collecting more waste per person. They were collecting waste from
**more people**: villages that had just become neighborhoods of metropolitan municipalities.
**Waste per covered resident did not change.**

**The honest headline:** Law 6360's clearest footprint in these statistics is the **extension of
municipal service coverage**, not a change in food sovereignty. Agricultural production shows no
detectable change, and the small land-use and input effects point in opposite directions.

## 7. Each check answers one objection

| Objection a jury could raise | Check | Result |
|---|---|---|
| "Only 14 treated provinces; your p-value is too optimistic." | wild cluster bootstrap, all six specifications | holds in every one (p from 0.002 to 0.025) |
| "A few provinces have bad data." | drop the data-quality outliers | unchanged (−0.0370 vs −0.0373) |
| "Your weighting makes waste too important." | equal indicator weights; TOPSIS | smaller, still there; always municipal burden |
| "It's the tariff waiver years (2014–2019)." | drop 2014, 2016, 2018 | similar (−0.034) |
| "It's the household denominator, not the numerator." | per-capita version; log decomposition | same (−0.037); the change is in waste itself |
| "Why does per area show nothing?" | variance check | min-max scaling squeezed per-area differences within provinces to almost nothing (0.9% of variance); not a real null |
| "New-metros are just bigger provinces growing differently." | controls = 14 largest non-metros | similar (−0.035); but no true size overlap exists, since the law used a population threshold |
| "Cost framing decides the sign." | benefit framing | the sign flips, as it must; it's a convention, not evidence |

## 8. What remains uncertain, stated plainly

- Three pre-reform time points: parallel trends is only weakly tested.
- Population grew about 5% faster in new-metro provinces, with one significant pre-reform
  difference (2008). Small next to the 30% coverage jump, but real.
- Province is coarser than the reform, which acted on villages.
- 2020 is a COVID year.
- For water (full index only), the tariff waiver remains a possible explanation; for waste it
  isn't.

## 9. Three sentences to be able to say without notes

1. "I compare how new-metropolitan provinces changed after 2014 with how non-metropolitan
   provinces changed over the same years; the difference is the estimated effect."
2. "The composite falls, but the whole effect is waste collection, and waste rose exactly as much
   as municipal coverage did: the reform counted more people, it didn't change what they
   produce."
3. "Agricultural production shows no detectable change, with an interval tight enough to rule
   out effects larger than about 0.02."
