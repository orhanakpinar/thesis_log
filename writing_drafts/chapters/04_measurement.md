# 4. Measuring Food Sovereignty with Official Statistics

<!--
WORKING DRAFT, agent-written for Orhan to rewrite. Markers:
  [INT]     an interpretation: accept, rewrite or reject
  [CITE: x] a citation you supply from your own reading; never cite unverified
  [VERIFY]  a fact to confirm against its source before keeping
Ledger rows used: B1, B2 (see claims_ledger.md). Search details: literature_research/ReadMe.md.
-->

This chapter describes how I turned food sovereignty, a concept about control, into a
measurable index built from official Turkish statistics. It has three parts. Section 4.1
follows the indicators from theory to data: what the concept asks for, what Turkish research
treats as relevant, and what official statistics can actually provide. Section 4.2 explains how
the remaining indicators are combined into a single index. Section 4.3 sets out what the
resulting index can and cannot claim to measure.

## 4.1 Indicator Selection

### 4.1.1 What the concept asks for

Food security and food sovereignty ask different questions about the same food system. Food
security asks whether people have reliable access to sufficient, safe and nutritious food. The
Food and Agriculture Organization's 1996 definition, and the four pillars of availability,
access, utilization and stability added in 2009, frame the problem in terms of supply and
consumption [CITE: FAO 1996; FAO 2009]. Food sovereignty, which La Via Campesina brought to the
same 1996 World Food Summit, asks who controls that system: who holds the land, who keeps and
exchanges seeds, who depends on purchased inputs, who reaches markets on their own terms, and
who decides agricultural policy [CITE: La Via Campesina 1996; Nyéléni 2007; Patel 2009]. A
country can in principle reach food security through imports and global markets. It cannot
reach food sovereignty that way, because sovereignty concerns control over production itself.

This difference matters for measurement. The most widely used composite indices measure food
security. The Global Food Security Index, for example, scores countries on affordability,
availability, quality and safety, and sustainability and adaptation, using national-level
indicators [CITE: Economist Impact 2022]. Attempts to measure food sovereignty are fewer and
more recent, and they work mostly at the national level [CITE: Ruiz-Almeida & Rivera-Ferre
2019; Mansouri 2023]. [INT] I am not aware of an established index that measures food
sovereignty below the national level, where differences in land, production and rural
livelihoods actually play out.

Turning a contested concept into numbers involves a chain of decisions: from the broad
background concept, to a specific systematized definition, to indicators that can be observed,
to the scores those indicators produce [CITE: Adcock & Collier 2001]. Each step can lose part of
the concept. The rest of this section traces that chain for the Food Sovereignty Index (FSOI)
and records what is lost at each step. [INT] I treat that loss not only as a limitation but as
a finding about what official statistics make visible.

### 4.1.2 Grounded extraction from Turkish studies

Rather than adopting indicators from global indices, whose content is shaped by what
international databases collect, I built the candidate list from research on Türkiye. The aim
was to cast a broad net for agricultural and rural indicators that Turkish researchers consider
relevant, and then to narrow that list toward food sovereignty. [INT] Starting from local
studies grounds the index in the conditions of Turkish agriculture rather than in the
availability of global data.

The themes of the international debate, reviewed in Chapter 2, guided what to look for. The
indicators themselves came from Türkiye-focused research. I searched Dergipark, Türkiye's
national academic journal platform, for articles whose abstracts contain both *tarımsal*
(agricultural) and *kırsal* (rural). The search returned 481 records (27 June 2024), some of
them empty rows in the export. After screening for relevance, I read 49 studies in full and
used 32 of them as sources of indicators. I added two further studies, one on agroecology and
one on social welfare policy.

From these 34 studies I recorded every variable the authors used, measured or argued to
matter for agricultural production and rural life. The approach follows the logic of grounded
theory: categories emerge from the material rather than being fixed in advance
[CITE: Glaser & Strauss 1967]. After merging duplicates and near-synonyms, the list held 184
candidate indicators in 27 categories. The categories range from those close to production
(land use, crop type, market, costs, water) to those at the core of sovereignty (land security,
autonomy, seed sovereignty, cooperatives), together with social categories such as household
structure, demography, gender and ethnicity. The full list is in Appendix A.

This list is the index's point of departure: what Turkish research suggests food sovereignty
depends on. The next section asks how much of it official statistics can show.

### 4.1.3 What official statistics can see

For a candidate indicator to enter the index, it had to meet three conditions. It had to come
from an open, official source, in line with the open-data principle of this study. It had to be
published at the province level (*il*, NUTS-3), since the province is the unit of analysis. And
it had to be available for every panel year from 2008 onward. The Turkish Statistical
Institute (TÜİK) is the main source. I used a ministry source only where TÜİK has no
equivalent, as for fertilizer use (Section 4.1.4). International datasets such as NASA
remote-sensing products and FAO's AQUASTAT were set aside because their coverage of Turkish
provinces is irregular, and region-level (NUTS-2) series were set aside because they cannot
separate provinces within a region. [VERIFY: NASA and AQUASTAT as the named examples, from the
preliminary report] The panel starts in 2008 because several indicators are not published for
earlier years.

Of the 184 candidates, 88 could be matched to a potential data source, and 24 met all three
conditions. Table 4.1 shows why the rest were eliminated, grouped into three blocs of
categories: production and land, the core of sovereignty, and social and governance
categories.

**Table 4.1.** Candidate indicators by category bloc and reason for elimination.

| Bloc | Candidates | Kept | Needs survey data | No official source | Only at region level | Source found, incomplete years or coverage |
|---|---:|---:|---:|---:|---:|---:|
| Production and land | 72 | 17 | 6 | 18 | 2 | 29 |
| Core of sovereignty | 37 | 1 | 9 | 5 | 0 | 22 |
| Social and governance | 75 | 6 | 6 | 11 | 3 | 49 |
| **Total** | **184** | **24** | **21** | **34** | **5** | **100** |

*Note.* Production and land: land use, crop type, market, costs, water, ecology, spatial,
husbandry. Core of sovereignty: land security, autonomy, seed sovereignty, cooperatives, food
sovereignty, scale, farmer dynamics, agroecology. Social and governance: household,
demography, rural development, technical capital, governance, finance, regional, network,
income, ethnicity, gender, other. Reasons are coded from the source and level recorded for
each candidate during the data search; the full list is in Appendix A.
*Source:* computed by `writing_drafts/scripts/attrition_table.py`.

The losses are not spread evenly. Nearly a quarter of the production and land indicators
survive (17 of 72). From the core of sovereignty, one survives (1 of 37), and it is an
agroecology indicator about the effect of agricultural waste, not a measure of control.
[VERIFY: that the one surviving core indicator is "Waste production affects of agricultural
lands/products"] Land security, autonomy, seed sovereignty and cooperatives all go to zero.

The reasons differ, too. Many core indicators fail because they would need survey data:
information about who owns land, who decides what to plant, or who belongs to a cooperative is
collected, if at all, through household or farm surveys, not published as a yearly province
series. Nine of the 37 core candidates fall into this group, including five of the six land
security indicators and four of the five autonomy indicators. Governance shows a different
pattern: 13 of its 21 candidates could be matched to a source, often a legal text or a
ministry program, but only one exists as a yearly province-level series. Governance appears in
the state's record as law, not as statistics. [INT] This is one reason the thesis examines the
Official Gazette separately (Chapter 7).

[INT] The pattern is systematic rather than accidental. Official statistics count what is
produced, where it is grown and what goes into it. They do not count who controls it. An index
built from these statistics can therefore measure the material base of food sovereignty,
meaning productive capacity, land use and dependence on purchased inputs, but not its
relational core of ownership, autonomy and voice. Section 4.3.2 returns to what this means for
interpreting the FSOI.

Two cautions apply to Table 4.1. First, the largest group, 100 indicators where a source was
found but coverage was incomplete, is a broad category. It covers missing years, missing
provinces and series that changed definition over time, and I did not record the exact reason
for every indicator. Second, "no official source" means that I did not find one during the data
search, not that none exists anywhere. Both cautions point to the same conclusion: the table
shows what a researcher can build from open official statistics, which is the question this
chapter asks.

### 4.1.4 From 24 indicators to 14

The 24 surviving candidates are concepts, not yet data. Turning each into a series meant choosing
the published table that measures it, and at this step the list changed shape in three ways:
some candidates were set aside, some were merged, and some were split or replaced by a better
measure.

**Set aside.** Three spatial candidates (village elevation, slope and satellite-based land
recognition) were left out of scope because processing satellite imagery for 81 provinces over
nine panel years was beyond the computational resources of this study. Two household candidates,
purchasing power and agricultural employment, exist only at the regional (NUTS-2) level. Detailed
crop-type series were summed into total crop production, so that provinces with very different
crop mixes remain comparable. Health personnel, farm machinery and net migration were on the
working list of TÜİK series but were set aside to keep the index focused on agricultural
production and its direct inputs: each measures a broader side of rural life whose link to
food sovereignty would need an argument of its own. Organic production was set aside because
too many years were missing.

**Merged.** Harvested area and sown area are almost the same measurement (r = 0.99 in both
denominators), so they form a single core land-use indicator.

**Split or replaced.** Greenhouse activity is split between two categories: greenhouse output
(tons) belongs to production, and greenhouse area (km²) to land use. The two are strongly
correlated (about 0.94), so greenhouse activity is reflected in two categories. I state this
rather than leave it implicit. Municipal water enters as the annual volume drawn into the
drinking and utility network. The volume of refined water was dropped because it records
whether a treatment plant exists rather than how much water is used: 27 of 81 provinces
reported exactly zero in 2008. TÜİK's per-person daily water series was also dropped, for a
reason that matters for the whole design: it is computed per person living in municipalities,
and Law 6360 itself enlarged that population (Section 6.x). A daily per-person waste series
duplicated the annual total (r = 0.999) and was dropped as well. Finally, fertilizer use, which TÜİK does not publish by province, was added from the Ministry
of Agriculture and Forestry's provincial plant-nutrient consumption records. These cover every
province without gaps from 2000 onward, apart from Hakkari in 2020–2024.

The result is 14 indicators (Table 4.2). Each is computed in two forms, per household and per
area, which gives 28 columns; Section 4.2.2 explains why the two forms are never mixed.

**Table 4.2.** The 14 FSOI indicators.

| Category | Indicator | Source | Unit (before denominator) | Direction | Years |
|---|---|---|---|---|---|
| Production | Total crop production | TÜİK | tons | benefit | 2008–2024 |
| Production | Greenhouse production | TÜİK | tons | benefit | 2008–2024 |
| Land use | Core cultivated land (harvested ≈ sown) | TÜİK | km² | benefit | 2008–2024 |
| Land use | Fallow land | TÜİK | km² | cost | 2008–2024 |
| Land use | Vegetable land | TÜİK | km² | benefit | 2008–2024 |
| Land use | Long-term crop land | TÜİK | km² | benefit | 2008–2024 |
| Land use | Greenhouse land | TÜİK | km² | benefit | 2008–2024 |
| Market | Crop production value | TÜİK | 1,000 USD | benefit | 2008–2020 |
| Market | Live animal value | TÜİK | 1,000 USD | benefit | 2008–2020 |
| Market | Animal product value | TÜİK | 1,000 USD | benefit | 2008–2020 |
| Municipal burden | Water drawn into the municipal network | TÜİK | 1,000 m³ | cost | 2008–2022 |
| Municipal burden | Waste collected | TÜİK | 1,000 tons | cost | 2008–2024 |
| External input | Fertilizer use (plant nutrients) | Ministry of Agriculture and Forestry | tons | cost | 2008–2024 |
| External input | Agricultural electricity use | TÜİK | MWh | cost | 2008–2022 |

*Note.* Market values are converted from Turkish lira to US dollars at the end-of-year exchange
rate of the Central Bank of the Republic of Türkiye. Years are biennial (2008, 2010, …). The
direction column is explained in Section 4.2.1. [VERIFY: TÜİK table names for each row go in the
data appendix; the electricity table name and the USD conversion method should be checked
against the notebook]

## 4.2 Combining Indicators

### 4.2.1 Five categories and what they measure

The 14 indicators are grouped into five categories. Each category answers one question about a
province's food sovereignty, and each indicator has a direction. For **benefit** indicators a
higher value means more sovereignty; for **cost** indicators a higher value means less, so their
scores are reversed before aggregation (Section 4.2.4).

**Production** asks how much a province produces. It combines total crop production and
greenhouse production, both in tons, and both are benefit indicators. [INT] Productive capacity
is the most basic material condition of sovereignty: a province that produces little depends on
food from elsewhere, however secure its supply may be.

**Land use** asks how much land is kept in agricultural use, and in what form. It combines core
cultivated land, vegetable land, long-term crop land (orchards and similar perennial crops) and
greenhouse land as benefit indicators, and fallow land as a cost indicator. [INT] Fallow is
treated as land withdrawn from production. [INT — likely jury question: in dryland Central
Anatolia, fallow (*nadas*) is a traditional practice that conserves soil moisture, so fallow
land is not simply lost land. This needs a sentence of defense, or a note that the benefit
framing is reported as a robustness check (Section 4.2.4).]

**Market** asks what value producers realize from what they produce. It combines the value of
crop production, live animals and animal products, converted to US dollars so that lira
inflation does not appear as growth. All three are benefit indicators. Market measures value,
production measures volume. The two are kept apart because they capture different things, and
because market data end in 2020 while production data run to 2024 (Section 4.3.1).

**External input** asks how far agriculture depends on inputs bought from outside the farm. It
combines fertilizer use and agricultural electricity use, both cost indicators. [INT] Input
autonomy, meaning the ability to farm without depending on purchased inputs, is central to food
sovereignty and to the agroecological literature it draws on [CITE: agroecology and input
autonomy, e.g. from your Chapter 2 sources]. An earlier version of the index called this
category "energy". The new name reflects what the two indicators share: fertilizer contains no
energy unit, but both are purchased off-farm inputs.

**Municipal burden** asks how much municipal service load falls on a household. It combines
water drawn into the municipal drinking and utility network and waste collected, both cost
indicators. Unlike the other four categories, this one is not agricultural. It enters the index
as the cost side of rural life [INT], and its two indicators are grouped for three reasons: both
are municipal household services, both are cost indicators, and both are affected by the same
change in municipal boundaries under Law 6360. [INT — open decision for you and your advisor:
keep this category inside the index, or report it separately (ledger B24). The causal results
make this choice consequential, so it should be settled before Chapter 6 is written.]

**How the indicators relate.** Grouping follows content, but correlations were checked so that
no category double-counts the same signal. Harvested and sown area were merged because they are
nearly identical (r = 0.99). Greenhouse output and greenhouse area remain in separate categories
although they correlate at about 0.94, which gives greenhouse-intensive provinces such as
Antalya and Mersin some weight in both production and land use. Water and waste, by contrast,
correlate only weakly once expressed per household (r ≈ 0.21), so they are two separate
indicators that share one category rather than a single merged measure. [VERIFY: r ≈ 0.21 from
the notebook's current correlation table]

---

## Suggested citations for §4.1.1–4.1.3

§4.1.3 needs no new literature. Cite the data sources: TÜİK's data portal (and the specific
tables, listed in the data appendix), and the ministry source for fertilizer. James C. Scott's
*Seeing Like a State* (1998) fits the "what the state counts" argument, but save it for the
Discussion, where you develop legibility after reading it.

Status: **in PDF** = already in your preliminary PDF's bibliography, so you have it.
**new** = not yet in your bibliography; find and read it before citing. I am fairly confident
each "new" reference below exists as written, but check volume, pages and year against the
real source.

| Cited as | Reference (APA 7) | Status | Used for |
|---|---|---|---|
| FAO 1996 | FAO. (1996). *Rome Declaration on World Food Security and World Food Summit Plan of Action*. https://www.fao.org/4/w3613e/w3613e00.htm | in PDF | security definition |
| FAO 2009 | FAO. (2009). *Draft declaration of the World Summit on Food Security* (WSFS 2009/2). | in PDF | four pillars |
| La Via Campesina 1996 | La Via Campesina. (1996). *The right to produce and access to land. Food sovereignty: A future without hunger*. | in PDF | sovereignty origin |
| Nyéléni 2007 | Nyéléni. (2007). *Declaration of Nyéléni*. Forum for Food Sovereignty, Sélingué, Mali, 27 February 2007. | new | the standard definition of sovereignty |
| Patel 2009 | Patel, R. (2009). Food sovereignty. *The Journal of Peasant Studies, 36*(3), 663–706. | new, verify title and pages | what sovereignty asks for; the definitional problem |
| Economist Impact 2022 | Economist Impact. (2022). *Global Food Security Index 2022*. | in PDF | GFSI pillars |
| Ruiz-Almeida & Rivera-Ferre 2019 | Ruiz-Almeida, A., & Rivera-Ferre, M. G. (2019). Internationally-based indicators to measure agri-food systems sustainability using food sovereignty as a conceptual framework. *Food Security, 11*(6), 1321–1337. | in PDF | prior measurement attempt |
| Mansouri 2023 | Mansouri, A. (2023, July). *Designing indicators for monitoring the food sovereignty*. 64th ISI World Statistics Congress, Ottawa. | in PDF | prior measurement attempt |
| Adcock & Collier 2001 | Adcock, R., & Collier, D. (2001). Measurement validity: A shared standard for qualitative and quantitative research. *American Political Science Review, 95*(3), 529–546. | new | concept → indicators chain |
| Glaser & Strauss 1967 | Glaser, B. G., & Strauss, A. L. (1967). *The discovery of grounded theory*. Aldine. | in PDF | grounded extraction |

**Worth reading for this section, optional to cite:** Edelman, M., et al. (2014), the
introduction to *The Journal of Peasant Studies* 41(6) special issue on critical perspectives on
food sovereignty. It shows the concept is contested, which supports the "contested concept"
framing in §4.1.1.

**Your reading decides one `[INT]`:** "I am not aware of an established index below the national
level." After reading Mansouri and Ruiz-Almeida & Rivera-Ferre, keep it, soften it, or drop it.
