# Agent note: agro_ministry_news scope and pipeline (AI-authored working note)

This file is AI-authored pipeline documentation for future sessions working on this strand.
Anything about result validity should live in the root `CLAUDE.md`, not here.

## New workflow, 2026-09-13ish: AI-first-pass + Orhan's top-of-head categories

Orhan proposed a new collaborative annotation model, replacing the pure "Claude classifies,
Orhan reviews" pattern from batches 1-2:

1. Claude (via subagent) classifies a batch: `Categories` (from the fixed 44-list, as
   before) + `Ceremonial_Political` + a single merged `Comment` field (replaces the old
   two-field `TopicGloss`/`Notes` split — simpler schema, same content). The existing 170
   rows were migrated to this schema (`Comment` = old `TopicGloss` + " | Notes: " + old
   `Notes` where present).
2. An empty `Orhan_Category` column is added for Orhan to fill in his own "top of head"
   category per row after reading Claude's `Categories`+`Comment` — this is deliberately
   NOT constrained to the 44-list; it's how new categories (he named `Water`, `Forestry`,
   `Collaboration` as likely candidates) are meant to emerge, grounded in concrete rows
   rather than invented abstractly.
3. Claude then reviews what Orhan added ("check the last version") and the category scheme
   evolves from there — annotating more richly / more consistently once real candidate
   categories exist. Orhan explicitly framed this as also being how a future session learns
   *how he thinks* about the literature_research categories, not just what the categories are.
4. **Scale plan, step by step, not all at once:** 170 (done) → +130 = 300 (batch 3, in
   progress) → +100 = 400 (batch 4) → +100 = 500 (batch 5). Each step should let Orhan review
   before the next batch runs, per his "step by step" framing — don't auto-chain all the way
   to 500 without checking in.
5. The classification subagent for batch 3 was explicitly told to call out candidate new
   category types (Water/Forestry/Collaboration-style content that doesn't fit the 44-list)
   directly in `Comment`, to give Orhan concrete rows to react to rather than a blank slate.

**Open interpretation note — resolved, 2026-09-13ish:** Orhan's exact phrase was "make a
Category and Comment as same." Checked with him directly: he actually meant to keep
`Categories` + two separate free-text fields (`TopicGloss`/`Notes`, i.e. the original
structure) — not merge them into one `Comment` column the way this session read it. **He
decided to keep the merged single `Comment` field anyway, no revert needed** — he finds it
readable as-is and prefers not to spend the effort reverting. So the schema
(`Categories, Ceremonial_Political, Comment, Orhan_Category`) is confirmed as the actual
going-forward schema, by explicit choice, not by defaulting to a misreading. Don't revert
this without Orhan asking.

**Known content-consistency caveat, accepted as-is:** the 170 rows migrated from batches 1-2
have `Comment` mechanically built as `TopicGloss + " | Notes: " + Notes` (a concatenation),
while batch 3's `Comment` field is genuinely free-flowing prose written directly by the
subagent (topic + ambiguity + candidate-category flags together) — richer and more useful,
per Orhan ("That comment section is better than Glossary I think"). **Orhan is considering
re-running batches 1-2 to regenerate their `Comment` field in batch 3's richer free-flowing
style, for consistency** — but explicitly said not to do this now ("let's stay same no need
to do it now"). Treat this as a real, live backlog item to revisit if he raises it again, not
something to do preemptively.

### Batch 3 results, 2026-09-13ish (130 new rows, cumulative now 300)

Output appended to `agroforestministry_news_validation_cumulative_CLAUDE_LABELS.csv`
(now 300 rows total, `Orhan_Category` still empty pending his review).

- **Category tally (batch 3 only):** `Agro_policy` 38, `TR_ruralGov` 38, `TR_agroGov` 33,
  `Agro_econ` 28, `TR_agroEcon` 20, `Rural_Livelihood` 20, `Risks_Global` 16,
  `Food_Security` 15, `Agro_international` 14, `Rural_Development` 13, `Health` 9, `Seed` 8,
  `Gender` 6, `Land_Policy` 6, `History` 6, `Cooperatives` 5, `Land_Consolidation` 4,
  `Small_holder` 4, `Shortfood` 4, `Education` 3, `Agroecology` 3, `Agro_tech` 3,
  `Buyuksehir_Law` 3, `Policy_Access` 3, `Rural_Family` 3, `Deruralization` 2, `Migration` 2,
  `Rural_Policy` 1, `Urbanization` 1, `Debt` 1. `Ceremonial_Political = yes`: 27/130.
  11 rows got zero categories (condolence/ceremonial content, or animal-welfare/nature-
  tourism topics genuinely outside the 44-list's scope — consistent with prior batches).
- **`Buyuksehir_Law`: 3 hits this batch — a meaningful recovery after the prior 170-row run
  scored 0.** Worth Orhan reading directly, ranked by strength:
  1. **Haber/4207 — the strongest hit found so far in this whole pilot.** The 3rd Agriculture
     and Forestry Council's final declaration, item 17, explicitly calls for büyükşehir
     belediyeleri to restructure neighborhoods into rural/urban categories while preserving
     village legal-entity (`köy tüzel kişiliği`) status, with the Ministry coordinating rural
     life — this is a direct, explicit description of Law 6360's rural-administration
     mechanics, not a buried incidental mention like Haber/392 was.
  2. Haber/3757 — tanzim satış (price-controlled produce sales) explicitly run by büyükşehir
     belediyeleri across several named cities.
  3. Haber/3666 (English) — Minister Pakdemirli credits metropolitan municipalities,
     "especially Ankara and Istanbul," with organizing produce delivery to consumers.
  - Two near-misses were flagged in Comments but deliberately NOT tagged: Haber/4160
    (a forest lease to İBB since 2012 — coincidental timing with the law, not an actual Law
    6360 rural-responsibility transfer) and Haber/3284 (Ankara büyükşehir belediyesi doing
    landscaping near a dam — unrelated). Worth Orhan spot-checking these two specifically to
    confirm the "not tagged" call was right, given how easy this category is to miss/misjudge
    (see the Haber/392 saga above).
- **Water/Forestry/Collaboration candidate flags — concrete rows for Orhan's top-of-head
  review, exactly what this workflow needs:**
  - Water-security-flavored content with no clean home in the 44-list: Haber/6706, 5623,
    6774, 6370, 5542, 5617, 5183, 1981, 5215, 1941, 3477, 3879, 3130, 2447, 1769 (15 rows).
  - Forestry/wildfire-disaster content: Haber/4788, 5967, 6499, 3477, 1668, 3146 (6 rows).
  - Explicit cross-institution/inter-ministry collaboration content: Haber/6774, 6392.
  - One additional candidate not previously discussed: a food-waste/zero-waste
    sustainability angle at Haber/7015, doesn't map cleanly onto anything existing either —
    worth Orhan considering alongside Water/Forestry/Collaboration when he does his pass.
- **Data-quality note, not a category issue:** two near-duplicate article pairs found in this
  batch — Haber/5455 & 5456 (same Indonesia G20 trip, covered twice) and Haber/3346 & 3325
  (near-identical province investment-recap templates for Kilis and Trabzon). Both pairs were
  classified independently per instructions rather than merged/deduped. Worth knowing this
  kind of near-duplicate exists in the corpus generally (ministry site sometimes publishes
  template-recap articles per province) if duplicate-content ever becomes a concern for
  full-corpus counts later.

**Status:** holding at 300 per Orhan's "step by step" plan — waiting for his review /
`Orhan_Category` additions before batch 4 (+100 → 400).

**File status note:** Orhan deleted `agroforestministry_news_seed.csv` (the 807-row "tohum"
keyword subset) and `agroforestministry_news_seed_lemmatized.csv` (its `zeyrek`-lemmatized
version) — confirmed gone. Both belonged to the lemmatization/TF-IDF branch that was
superseded by the LLM classification pivot (see "Turning point" section below); nothing in
the current pipeline (the cumulative sample + LLM classification work) reads either file.
Don't go looking for them or treat their absence as something broken. If the "tohum" subset
is ever needed again, it's one line to regenerate: filter `agroforestministry_news.csv` for
"tohum" in `Title` or `Paragraphs`.

## Forward-steps roadmap (keep updated — last updated 2026-09-12)

Read this first for current status at a glance; sections below have the full reasoning
behind each row.

| # | Step | Status |
|---|---|---|
| 1 | Full-text scrape (7,107 articles, Number 153-7260) | Done |
| 2 | "Tohum" seed subset regenerated (807 rows, title-or-body match) | Done |
| 3 | Keyword-bag frequency diagnostic (raw word counts, no weighting) | Done |
| 4 | Pick lemmatizer | Done — `zeyrek` confirmed by Orhan, added to `requirements.txt` by main agent |
| 5 | Investigate 615 rows with empty `Paragraphs` | Not started |
| 6 | Pick which literature categories to target (subset of the ~44, multi-label) | Orhan's call, not decided |
| 7 | Apply lemmatization to seed subset, re-run keyword-bag to confirm cleanup | Done, 2026-09-12 — see lemmatization section below for validated results and known residual errors |
| 8 | Build TF-IDF on the lemmatized seed subset, inspect top-weighted words | **Superseded, 2026-09-12** — see "Turning point" section below. Not deleted from the roadmap because the reasoning for trying it first is still valid context, just outgrown |
| 9 | Try YAKE/RAKE on the same subset, compare against TF-IDF | **Superseded, 2026-09-12** — same as #8 |
| 10 | Decide whether/how to extend to full corpus and tie results to chosen categories | Still open, now via the LLM path instead of #8/#9 |
| 11 | Pick LLM(s) | **Confirmed, 2026-09-12** — three-way comparison: Claude Haiku 4.5 (pilot/production candidate, Sonnet 5 fallback) + a local open-source model (`Qwen2.5-3B-Instruct` candidate, GTX 1660 Ti 6GB) + Orhan's own hand labels. See "Decisions confirmed" subsection |
| 12 | Design validation protocol | **Confirmed, 2026-09-12** — stratified whole-corpus sample, hand-labeled by Orhan, percent agreement + Cohen's kappa against each model, fixed model/prompt/settings (temp 0), qualitative spot-check of disagreements |
| 13 | Small classification demo (6 random articles, done inline by Claude, 2026-09-12) | Done — see "Turning point" section for the actual results; already surfaced a real category gap (#2820, resolved → `Agroecology`) and motivated adding a ceremonial/political-visibility category |
| 14 | Set up local model (`Qwen2.5-3B-Instruct` or similar, 4-bit) on Orhan's GPU | Not started |
| 15 | Draw + hand-label the stratified validation sample | Not started |
| 16 | Run Claude Haiku 4.5 + local model on the validation sample, compute agreement/kappa vs. Orhan's labels | Not started, blocked on #14/#15 |
| 17 | Decide final category schema (literature-codebook subset + the new ceremonial/political-visibility tag) based on what the pilot actually surfaces | Not started, blocked on #16 |
| 18 | Run the chosen classifier at full-corpus scale | Not started, blocked on #17 |
| — | Sentence embeddings / zero-shot transformer classification | Superseded by the LLM pivot below rather than "paused" — an LLM-based approach subsumes what this would have offered |
| — | TF-IDF / YAKE / RAKE as the *main* classification method | Superseded, 2026-09-12 (see "Turning point") — may still resurface later as a cheap *supplementary* signal (e.g. literal keyword counts alongside LLM categories), not ruled out for that narrower use |
| — | LDA, BERT-based topic modeling, NER | Still ruled out / discarded, don't re-propose without Orhan raising it again — note this is a **different** decision from the LLM classification pivot, don't conflate them |
| — | Downstream framing: this strand's output is a national-level "policy activity/attention" signal, not a 7th FSOI category and not GFSI's "political commitment" framing | Decided, 2026-09-12 (see cross-strand coordination section below) |

Immediate unblockers are #11 (which LLM) and #12 (validation protocol) — both need Orhan's
decision, not something to guess at.

## Turning point, 2026-09-12: pivot from rule-based statistics to LLM-assisted classification

**What changed and why.** Steps 1-7 (scrape, subset, keyword-bag, `zeyrek` lemmatization)
were built on the premise that transparent, rule-based/statistical methods (no LDA, no BERT)
were the right fit for defensibility. That premise held up fine for the narrow goal of
"count words accurately," but broke down against the actual goal Orhan needed: understanding
what an article is *about*, not just which literal words it contains. Concrete evidence that
drove the pivot, all found via direct empirical checking (not assumption) over this session:
- `zeyrek` mis-lemmatized `tarım` (agriculture) → `tar`, and `bin` (thousand) → `binmek` (to
  ride), both silently, because it doesn't rank candidate analyses by likelihood. Fixed with
  an exact-surface-match heuristic (see lemmatization section above) — but then a **further**
  check (Orhan asking specifically about "bakan") found the fix is incomplete: bare "bakan"
  (minister) lemmatizes correctly, but the inflected form "Bakanlığı" (the ministry) still
  falls through to the wrong candidate, `bakmak` (to look). Each fix uncovered a new instance
  of the same underlying problem: a morphology-only tool cannot resolve ambiguity that
  requires *context*, and every fix found so far still needed a human (Orhan) to notice
  something looked wrong and ask about it directly.
- Even with lemmatization "working," none of steps 1-9 would have told us **what an article
  is about** — only literal word frequency/importance. Orhan's actual stated goal
  ("understand the text and quantify content," "spot key findings in broad categories") was
  never something TF-IDF/YAKE could deliver; they were always going to plateau at
  keyword-level signal, not topic-level understanding.
- A 6-article demo (done inline by Claude during this conversation, sampled from across the
  *whole* corpus, not just the tohum subset) showed an LLM-based read can do in one pass what
  the rule-based pipeline structurally cannot: correctly separate real policy content from
  pure ceremony/photo-ops (e.g. a minister's courtesy visit with no policy content vs. an
  actual regulation-planning meeting), and surface a genuine category gap — a Forestry
  Directorate wild-orchid seedling propagation program that is seed-*adjacent* but wouldn't
  match the "tohum" keyword filter and doesn't cleanly fit any of the 44 literature
  categories. See chat log 2026-09-12 for the full 6-row table if needed.

**Reframed defensibility argument.** The earlier "no BERT/LLM for now" stance was reasonable
given the information available at the time, but the operating assumption — "rule-based =
defensible, model-based = not" — doesn't hold up against what was actually found: the
rule-based path still needed the same kind of manual spot-checking to catch errors (three
separate bugs found and fixed/partially-fixed this way), so it wasn't actually saving
validation effort, just hiding where the errors occurred. The real lesson from
`resmi_gazete/`'s own precedent (cited repeatedly earlier in this file) is that **validation
against a human-checked sample is what makes a method defensible, not the method's internal
simplicity.** An LLM-assisted classification, paired with a documented validation protocol
(gold-standard hand-labeled sample, agreement metric — see roadmap #12), can satisfy the same
defensibility bar an LDA/BERTopic pipeline would have needed anyway, while actually
addressing the real goal (content understanding) instead of a proxy for it (word frequency).

**What this does NOT change:** NER and LDA/BERTopic-style unsupervised topic discovery are
still separately discarded/ruled out (different decisions, don't conflate). Lemmatization
and keyword-bag counting aren't thrown away either — they may still be useful as a cheap
supplementary signal alongside LLM-assigned categories (e.g. reporting literal keyword
frequency as a sanity check on LLM output), just not as the primary classification method.

**Next decisions needed from Orhan (not to be guessed at):** which LLM to prototype/use
(Claude now for prototyping vs. an open-source model for the final reproducible pipeline —
options and tradeoffs discussed in chat 2026-09-12, not duplicated here to avoid this note
going stale as models change) and the validation protocol design (roadmap #12).

**For later thesis documentation (Orhan, 2026-09-12):** record explicitly that a rule-based/
statistical NLP approach (lemmatization via `zeyrek`, planned TF-IDF/YAKE) was tried first
and did not reach a conclusive, adopted result — the pivot to LLM-assisted classification
came *after* that attempt, not instead of ever trying it. This is a methodology-narrative
point for the thesis write-up, not just a pipeline log entry — don't let it get lost.

### Decisions confirmed, 2026-09-12

- **Validation protocol — SUPERSEDED, 2026-09-12, same day it was confirmed.** Originally:
  draw a stratified sample, Orhan hand-labels it blind, compare against model output via
  percent agreement + Cohen's kappa. Two things changed this same day, both from Orhan
  directly:
  1. **Orhan will not hand-label.** His words: "I will not touch on annotation. I may only
     review validation... Later I will closely analyze the topics and their text
     counterpart." So there is no independent human gold-standard label set, and no
     agreement/kappa statistic is being computed against one. Don't plan around kappa unless
     Orhan explicitly asks for it again.
  2. **The blind-labeling design was compromised in practice anyway.** Batch 1's subagent
     summary (category tally + gap findings) came back as a tool result inside the same
     interactive session Orhan was watching, and he confirmed he saw it ("I saw the output
     here. Category tally is not bad... it's very quirky that we found so many ceremonial").
     So even if hand-labeling had gone ahead, it would not have been blind for batch 1.
  **What the validation protocol actually is now:** Orhan reviews the LLM's category
  assignments and flags (`Ceremonial_Political`, `TopicGloss`, `Notes`) *together with* the
  source article text, looking for errors, quirks, and interesting patterns — an expert
  qualitative audit/spot-check, not blind independent double-coding with an inter-rater
  reliability statistic. **This is a real methodological difference, not just a shortcut** —
  if this shows up in the thesis methodology section, it should be described accurately as
  expert review of LLM output, not as an inter-annotator agreement study. Don't retroactively
  describe it as the original design.
- **Model comparison is now explicitly three-way, not just "pick one LLM":** human
  hand-labels vs. Claude vs. a local open-source model, run on the *same* validation sample.
  Orhan wants the local model included specifically as a computational-social-science-style
  comparison point across model scale/type, not because it's expected to outperform Claude.
  (Note: Claude's exact parameter count isn't publicly disclosed by Anthropic — don't state a
  specific figure as fact in the thesis; "much larger than a locally-hosted open model" is the
  fair, verifiable framing.)
  - **Correction, 2026-09-12: no separate Anthropic API access.** Orhan only has Claude Code
    (Pro subscription, via the VS Code extension) — not a separate Anthropic API key/billing
    account. This changes the mechanism entirely: there is no standalone Python script calling
    the `anthropic` SDK per-article. Instead, classification work runs *inside Claude Code
    sessions*, via the `Agent` tool spawning subagents (with `model: "sonnet"` per Orhan's
    preference — he wants **Sonnet**, not Haiku, since he isn't paying per-token and quality
    matters more than marginal cost here). The earlier per-token dollar-cost estimate ($10-15
    for the full corpus) doesn't apply to how this is actually being run — what matters
    instead is **Claude Code Pro's rolling 5-hour usage-window limits**. A handful of
    subagent calls for a ~70-article pilot is trivial; classifying the full ~7,100-article
    corpus this way would need many subagent calls spread across multiple session windows —
    a real time/quota commitment to plan for later (roadmap #18), not a small pilot-scale
    task. Don't assume the earlier per-token cost math still applies anywhere in this note.
  - **Local model: reconsidered, now optional/deprioritized, 2026-09-12.** Orhan questioned
    the value given the scale gap (a 3B local model vs. Claude) — reasonable pushback. My
    honest assessment, given to him directly: modest value as a documented "how much does
    model scale matter for this specific task" comparison point (a fine footnote for a
    computational social science thesis), but **not decision-critical** — Claude will likely
    be the production classifier regardless of the local model's performance, and setting up
    local quantized inference (GTX 1660 Ti, 6GB, Turing architecture — a 3B-class model like
    `Qwen2.5-3B-Instruct` at 4-bit would be the realistic fit; 7B is tight; no flash-attention
    speedup on this GPU generation) costs real setup time for a comparison that doesn't change
    any pipeline decision either way. Status: **not started, and not currently planned unless
    Orhan decides the comparison is worth the time** — don't treat this as a committed
    roadmap item the way it was recorded earlier in this same session.
- **Category schema additions confirmed:**
  - Article #2820 (wild salep-orchid seedling propagation, flagged as a category gap in the
    6-article demo) → **`Agroecology`** is a good fit, per Orhan. Resolves that specific gap;
    doesn't mean every biodiversity/conservation article automatically maps there without
    checking.
  - Orhan wants an explicit **ceremonial/political-visibility/marketing category** (his
    framing: "we should rule out full marketing or political cases... expected in Türkiye's
    website as political conjuncture"). This should be a first-class tag in the schema — used
    to *identify and exclude* content like a minister's courtesy visit or a building-opening
    ceremony from the "policy activity" signal, not just noted as noise after the fact. Not
    yet named/specced as a formal category — needs a decision on exact label and whether it's
    single-label-exclusive (an article is *either* this *or* a substantive category) or can
    co-occur with a real policy tag (a real policy announcement can still be delivered with
    heavy political framing).

### Standardized subagent classification prompt (Orhan asked, 2026-09-12, to record this so
the process is reproducible rather than reinvented each session)

Launch via the `Agent` tool, `subagent_type: "general-purpose"`, `model: "sonnet"` (Orhan's
explicit preference — see "Correction: no separate Anthropic API access" above for why this
is a subagent, not a raw API call). Prompt template, fill in the bracketed parts:

> You are helping with an MA thesis on Turkey's Food Sovereignty Index. Part of the project
> scrapes press releases from the Turkish Ministry of Agriculture and Forestry
> (tarimorman.gov.tr) and wants to classify what each article is actually about.
>
> Read this CSV file in full (it's long, will need multiple Read calls with offset/limit —
> read every row, don't stop partway): `[input CSV path]`
>
> Columns: Batch, Number, URL, Title, Date, Paragraphs. There are `[N]` rows, mostly Turkish,
> a few English.
>
> For EACH row, read Title and Paragraphs and produce:
> 1. `Categories`: zero or more labels, semicolon-separated, chosen ONLY from the fixed
>    44-category literature codebook (see below) — do not invent new category names, multi-
>    label is normal (2-3 tags per article is typical usage elsewhere in the thesis).
> 2. `Ceremonial_Political`: "yes"/"no" — primarily ceremonial/photo-op/personal messaging
>    with little substantive policy content? Can co-occur with a real category.
> 3. `TopicGloss`: one plain-English sentence on what the article is actually about,
>    independent of the category list — keep flagging things that don't fit well, even though
>    the category list itself is now fixed (this is still useful exploratory information, see
>    "Category scheme correction" below for why).
> 4. `Notes`: anything ambiguous, low-confidence, or where a category had to be stretched to
>    fit — be honest about stretches rather than hiding them.
>
> Write output as a NEW CSV (don't modify the input) to: `[output CSV path]`
> Columns: Batch, Number, Categories, Ceremonial_Political, TopicGloss, Notes
>
> Be deliberate and consistent. Process all rows, no sampling/skipping. When done, report:
> rows processed, category tally, count of Ceremonial_Political=yes, how many rows got zero
> categories, and any content types that still don't fit well even after trying to map them
> onto the fixed list.

### Category scheme correction, 2026-09-12: literature codebook only, no invented categories

Orhan corrected the direction taken after batch 1/2: **"Keep categories as defined in
literature_research notebook."** The `Water_Infrastructure`, `Forestry_Disaster`, and
`Animal_Welfare` categories added after batch 1 are **dropped** — they were invented for this
news corpus specifically, not part of the literature review's actual codebook, and Orhan
wants this strand's categories to stay tied to that existing, theoretically-grounded list
rather than drift into a second, disconnected taxonomy (the exact concern raised the first
time the 44-category codebook was discussed, revisited here after briefly drifting from it).

Orhan also specifically asked about a "Husbandry" or "Livestock" category (for
sheep/meat/animal-husbandry content) — **checked directly in
`literature_research/literature_annotation.ipynb`, and no such category exists.** Livestock/
"hayvancılık" content in that notebook's actual annotated examples gets **multi-tagged across
general-purpose categories** depending on angle — e.g. `TR_agroGov`/`TR_ruralGov` (livestock
registration systems, ministry livestock programs), `Agro_econ` (livestock economics/prices),
`Agroecology` (livestock-environment interaction), `Variable` (livestock headcount statistics
used as a quantitative indicator) — not a single dedicated "livestock" bucket. **Apply the
same practice going forward for any recurring content type that doesn't have an obvious
single-category home** (irrigation/dams, forestry/wildfire, livestock, etc.): multi-tag onto
the closest existing general categories the way the literature review itself does, rather
than proposing a new category name. This is a real constraint, not just a style
preference — expect the "no category fits well" rate to go up compared to batch 1/2's looser
scheme, and that's an accepted tradeoff, not a labeling failure to fix.

**The full 44-category codebook** (from `literature_research/literature_annotation.ipynb`
cell 1 — re-verify against that notebook if this list is ever suspected stale, don't trust
this copy blindly forever): `Agro_econ`, `Agro_international`, `Agro_policy`, `Agro_tech`,
`Agroecology`, `Autonomy`, `Big_agro`, `Buyuksehir_Law`, `Collectives`, `Cooperatives`,
`Debt`, `Deruralization`, `Education`, `Food_Network`, `Food_Security`, `Food_Sovereignty`,
`Gender`, `Health`, `History`, `Interdisciplinary`, `Land_Consolidation`, `Land_Policy`,
`Land_Use`, `Migration`, `Monoculture`, `Monoculture_Poli`, `Policy_Access`, `Risks_Global`,
`Rural_Development`, `Rural_Family`, `Rural_Livelihood`, `Rural_Policy`, `Rurban`, `Seed`,
`Shortfood`, `Small_holder`, `Survivorship_bias`, `TR_agroEcon`, `TR_agroGov`, `TR_landUse`,
`TR_ruralGov`, `TR_Peasant`, `Urbanization`, `Variable`. Most of these are literature-review
meta-categories (`Gender`, `Health`, `Migration`, `History`, `Interdisciplinary`,
`Survivorship_bias`, etc.) that may rarely or never apply to ministry press releases — that's
expected, don't force usage just to spread across the list. `Food_Sovereignty` specifically:
batch 1/2 found it applies almost never to this corpus (0/70, then 0/100) — apply strictly,
don't stretch it, and treat continued near-zero usage as a finding about the data source, not
a sign the classifier is missing things (see batch results below).

### Cumulative sample file architecture (Orhan, 2026-09-12: "place annotated batches in same
file on top of each other... use it later for cumulative graphs")

Switched from per-batch files (overwritten each round) to **one growing cumulative file**
with a `Batch` column, so nothing gets lost and later analysis (e.g. cumulative counts/graphs
over time) has everything in one place:
- `agro_ministry_news/agroforestministry_news_validation_cumulative.csv` — source articles,
  columns `Batch, Number, URL, Title, Date, Paragraphs`.
- `agro_ministry_news/agroforestministry_news_validation_cumulative_CLAUDE_LABELS.csv` —
  Claude's classification, columns `Batch, Number, Categories, Ceremonial_Political,
  TopicGloss, Notes`.

The old per-batch files (`agroforestministry_news_validation_sample_BLANK.csv` and
`..._CLAUDE_LABELS.csv`) were **deleted 2026-09-12** once their content was merged in — don't
go looking for them, they're gone on purpose, not lost by accident.

**Known duplicate:** batches 1 and 2 were drawn independently (different seeds) and happened
to overlap on 2 article Numbers by chance. Both copies were kept in the cumulative file
(one row per batch draw) rather than deduped, since each batch's classification run is
independent — if this matters for a cumulative count/graph later, filter on `Number` first,
don't assume 170 rows means 170 distinct articles.

**Future batches — sampling method simplified per Orhan ("I don't know how you batch it.
Just randomly select"):** drop the year-stratification logic from batches 1-2, just draw a
plain random sample from articles with non-empty `Paragraphs` that **aren't already in the
cumulative file** (check existing `Number`s in `agroforestministry_news_validation_cumulative.csv`
first, exclude them, then random-sample from the remainder — keeps growing the cumulative set
without re-drawing the same articles). Append (don't overwrite) both the source-article rows
and, after running the classification subagent again, the labels rows, incrementing the
`Batch` number each time.

### Sample batch log

| Batch | N | Sampling | Seed | Category scheme used | Status |
|---|---|---|---|---|---|
| 1 | 70 | 5/year × 14 years (2013-2026) | 7 | Old exploratory scheme (literature subset + `Water_Infrastructure` flagged, no `Forestry_Disaster`/`Animal_Welfare` yet) | **Superseded** — merged into the cumulative file 2026-09-12 and re-classified under the corrected literature-only scheme (see below) |
| 2 | 100 | 7/year × 12 years + 8/year × 2 largest years (2017, 2018) | 11 | Old exploratory scheme (literature subset + `Water_Infrastructure`/`Forestry_Disaster`/`Animal_Welfare` all invented, non-literature categories) | **Superseded** — same merge/re-classification as batch 1. Results from this scheme are kept below as a historical record of what the invented categories found, since that's genuinely useful information even though the categories themselves were dropped |
| 1+2 combined | 170 (168 distinct, 2 overlap) | n/a (merge of the above) | n/a | **Corrected: full 44-category literature codebook only** (see "Category scheme correction" above) | **Completed 2026-09-12.** Results below |

**Historical record: what batch 1/2's now-abandoned invented categories found (kept for
reference, not the current scheme):** `Water_Infrastructure` (irrigation/dam/flood-control)
was extremely common — 14/70 in batch 1, 28/100 in batch 2, making it arguably the single
most frequent story type in this whole corpus; `Forestry_Disaster` (wildfire response)
appeared in 6/100 in batch 2; `Animal_Welfare` (stray/street animals) never got a genuine hit
in either batch (0/70, 0/100) — Orhan's read on this ("Animal_Welfare is not very much")
matches what the data actually showed, and is part of why it was dropped rather than kept as
a rarely-used category. `Food_Sovereignty` was 0/70 then 0/100 under both schemes — this
finding carries over regardless of which category scheme is used, and is worth treating as a
substantive finding about the data source (see "Category scheme correction" above), not an
artifact of the abandoned categories.

**Other findings from batch 1/2 worth carrying forward regardless of category scheme:**
- **Data-quality issue:** Haber/276 is a leftover "deneme" (test) placeholder entry with no
  real content, sitting live in the scraped corpus. Filter entries like this out before any
  full-corpus run — there may be more, not checked yet.
- ~34% and ~29% of batch 1/2 respectively were flagged `Ceremonial_Political = yes` —
  consistent enough across two independent samples to trust as a real base rate for this
  corpus, not sampling noise.

### Corrected classification results, 2026-09-12 (170 rows, full 44-category codebook)

Output: `agroforestministry_news_validation_cumulative_CLAUDE_LABELS.csv`. All 170 rows
processed, verified against the source file's Batch+Number keys (no rows lost/duplicated).

**Category tally** (times used across 170 rows; most articles carry 2-4 tags): `Agro_econ`
75, `TR_agroGov` 50, `Agro_policy` 49, `Rural_Development` 46, `TR_ruralGov` 45,
`TR_agroEcon` 36, `Risks_Global` 34, `Land_Policy` 33, `Agro_international` 29,
`Agroecology` 14, `Land_Use` 14, `Food_Security` 14, `Agro_tech` 13, `Rural_Livelihood` 13,
`Seed` 11, `Health` 7, `Education` 6, `Land_Consolidation` 6, `Gender` 6, `Migration` 3,
`Rurban` 2, `Small_holder` 2, `Urbanization` 1, `Debt` 1, `Deruralization` 1,
`Cooperatives` 1, `TR_landUse` 1. **Never used:** `Autonomy`, `Big_agro`, `Buyuksehir_Law`,
`Collectives`, `Food_Network`, `Food_Sovereignty`, `History`, `Interdisciplinary`,
`Monoculture`, `Monoculture_Poli`, `Policy_Access`, `Rural_Family`, `Rural_Policy`,
`Shortfood`, `Survivorship_bias`, `TR_Peasant`, `Variable` — mostly literature-review
meta-categories, expected per the guidance given to the subagent, **except**:

**`Buyuksehir_Law` = 0 this run is a real miss, confirmed by checking source text directly —
not just an acceptable "meta-category, expected to be rare" case.** Batch 2's earlier
(now-superseded) pass had flagged Haber/392 as a genuine `Buyuksehir_Law` hit. I checked the
raw article text directly to see which run was right: Haber/392 (a 2014 agricultural fair
opening in Diyarbakır) contains, buried in a quote from the Diyarbakır Metropolitan
Municipality's co-mayor near the end of the article: *"Bugüne kadar büyükşehir
belediyelerinin tarım ve hayvancılık faaliyetlerine dolaylı katıldığını ancak son
düzenlemeyle 30 büyükşehir belediyesinin artık bu konuda sorumluluk ve görev alacağını"*
("until now metropolitan municipalities participated only indirectly in agricultural/
livestock activities, but under the recent regulation 30 metropolitan municipalities will now
take on responsibility in this area") — **this is genuinely, explicitly about Law 6360's
effect on metropolitan municipalities' agricultural role, the exact thing this whole thesis
is about.** The corrected run's `TopicGloss` for this row only describes the fair/export/dam
angle and misses this entirely; the category tag list for the row doesn't include
`Buyuksehir_Law`. **So the earlier run was right and the newer, more careful-seeming run
missed it** — the opposite of what I expected when I went to check.
- **Why this matters beyond one row:** this is now a concrete, verified example of the exact
  failure mode Orhan asked about (rerun and compare to catch mismatches) actually catching a
  real miss — not a hypothetical. It also suggests a specific risk pattern: `Buyuksehir_Law`
  content in this corpus may often be a buried secondary detail (a quote from a local
  official, not the article's main subject) rather than the headline topic, which makes it
  easy for a single classification pass to miss even when reading the full text. Given this
  category is the one most directly tied to the thesis's core research question, **it
  deserves a dedicated, careful re-check across the full sample (and eventually the full
  corpus) rather than trusting either run's count as-is** — don't report either 0 or 1 as the
  real answer for this category without that recheck.
- **Action for next session/turn:** run the Categories-vs-TopicGloss consistency check
  (section below) with specific attention to `Buyuksehir_Law` false negatives, and/or a
  targeted second pass asking specifically "does this article mention the Metropolitan Law,
  Law 6360, or metropolitan municipalities taking on new agricultural/rural responsibilities,
  even briefly or in a quote" rather than relying on general classification alone.

**`Ceremonial_Political = "yes"`:** 38/170 (~22%) — consistent with the ~34%/~29% seen in
batches 1/2 separately (different exact rate expected given different scheme/sample
composition, but same general "a substantial minority of ministry press output is
ceremonial/political framing" finding, now confirmed a third time).

**Zero-category rows:** 13/170 — mostly pure ceremonial visits or content with no
agricultural substance, plus the Haber/276 "deneme" placeholder.

**Content types still not mapping cleanly onto the 44-category list** (per the "multi-tag
onto closest existing category, don't invent" instruction — these got stretched tags rather
than new categories, noted honestly in each row's `Notes`): pure wildlife/nature human-
interest stories (stretched into `Agroecology`), hydroelectric energy-output stories where
the dam is nominally under the Ministry via DSİ but the content is really about electricity
not agriculture (stretched into `TR_ruralGov`/`Rural_Development`), urban drinking-water/
desalination infrastructure for city populations rather than farmland irrigation (same
stretch), and a handful of one-paragraph blurbs too thin to classify with real confidence.
This is the expected tradeoff Orhan accepted when the category scheme was corrected — record
it, don't try to silently fix it by reintroducing dropped categories.

### Orhan's feedback on the corrected results, 2026-09-12 — inputs for the next iteration, not yet applied

None of the below has been implemented yet — recorded so it isn't lost, to fold into the
"topic glossary" work Orhan mentioned wanting to do next, and/or the next classification pass.

- **`Buyuksehir_Law` → rename to `Metropolitan_Law` going forward in this strand.** Orhan's
  explicit request, on top of confirming the miss above was a real problem ("that's a bit
  sad... there is a sad miss"). **Caveat: `literature_research/literature_annotation.ipynb`
  still uses `Buyuksehir_Law` as the category name** — that notebook is outside this strand's
  write scope (read-only reference) and has no dedicated strand agent yet per root
  `CLAUDE.md`. Don't silently let the two strands' naming diverge without Orhan noticing —
  flag to him (or to `thesis_log_main_agent`) whether the literature notebook's category name
  should be updated too for consistency, rather than just renaming it here in isolation.
- **Water content:** Orhan agrees `Agroecology` is an acceptable stretch-fit for now, but
  floated a possible new **`Water_Security`** category ("maybe we need water_security
  somewhere") — framed as tentative, not a firm decision. Note this is a different framing
  than the earlier dropped `Water_Infrastructure` (that was construction/infrastructure-
  focused; "water security" is a different, arguably more literature-legitimate frame, closer
  to the `Food_Security`-style categories already in the codebook) — worth discussing as a
  possible genuine codebook *addition* (with Orhan's sign-off, and ideally reflected back to
  the literature strand too) rather than a repeat of the invented-category problem, if he
  decides to go ahead with it.
- **Ceremonial content shouldn't always end up uncategorized:** "Sometimes ceremonials are
  just Rural_Livelihood" — e.g. a ceremonial village visit can still genuinely touch rural
  livelihood themes and deserves that tag even if `Ceremonial_Political = yes`. Don't treat
  "ceremonial" and "categorizable" as mutually exclusive when reviewing/re-running
  classification — this was technically already allowed by the "can co-occur" instruction
  given to the subagent, but Orhan's comment suggests the actual outputs may have been too
  quick to leave ceremonial rows at zero categories. Worth checking specifically in the
  consistency pass.
- **Possible new catch-all: "Magazine_events"** for human-interest/soft-news content that
  doesn't map to a real policy category (photo contests, TV interviews, fair-visit color
  pieces) — Orhan's suggestion, tentative ("maybe"), floated as an alternative to leaving
  these at zero categories or stretching them into `Agroecology`/etc. Not decided.
- **Gender confirmed:** "If there are Woman news, it is related to Gender" — this is already
  correct in the current schema/instructions (`Gender` got 6 hits in the corrected run), no
  change needed, just a confirmation to keep applying it that way.
- **Known scope gap, acknowledged not fixed: ethnicity/traditional-community content.**
  Orhan's own words: "I left Ethnicity out of the research so maybe we lose some traditional
  events there?" There is no ethnicity-related category anywhere in the 44-category codebook.
  This means articles about ethnic/traditional community events (which do appear in this
  corpus — e.g. Kurdish-region cultural content came up in earlier spot-checks) have no home
  and will likely fall to zero categories or get stretched elsewhere. This is a known,
  acknowledged limitation of the literature review's scope, not a bug in this strand's
  classification — don't try to invent an Ethnicity category to "fix" it without Orhan
  raising that directly, since he's the one who deliberately scoped it out of the lit review.
- **"We will work on topic glossary perhaps."** Orhan wants to build out something like a
  proper glossary mapping recurring topic types (the ones found via `TopicGloss` across
  batches) to categories/decisions, presumably to stabilize a lot of the ad hoc judgment
  calls above into a documented reference. Not started, no format decided — flag this as a
  live open task next time it comes up rather than assuming it dropped.

### Consistency-check pass: Categories vs. TopicGloss (Orhan's idea, 2026-09-12)

Orhan asked whether we can rerun a check comparing the `Categories` column against the
`TopicGloss`/`Notes` columns to catch mismatches (e.g. gloss describes wildfire response but
no matching category got tagged, or vice versa) — yes, and it's cheap to (re)run any time:
it's a second pass over the *already-produced* `..._CLAUDE_LABELS.csv` file, not a new read of
the source articles, so it doesn't need the corpus or even much time. Mechanism: launch
another subagent (or reuse this same session), give it the labels CSV, and ask it to flag
rows where `Categories` and `TopicGloss` seem to describe different things — a
self-consistency audit rather than a check against ground truth. Useful both as a QA step
right after a classification run, and as a way to dig deeper into specific rows Orhan wants
to scrutinize later. Not run yet as of this note revision — do this once the current
cumulative re-classification (170 rows) finishes, or any time after on any labels file.

**Results, run 2026-09-12.** Output:
`agroforestministry_news_validation_cumulative_CONSISTENCY_CHECK.csv`. 8 rows flagged out of
170 (Categories_vs_Gloss_mismatch: 6, Metropolitan_Law_miss: 1, Ceremonial_undercategorized: 1).

- **Haber/392's Metropolitan Law miss: confirmed caught, and confirmed to be the *only* one
  in this 170-row sample** — the targeted full-text re-read (Check 2) checked every other
  "büyükşehir" occurrence in the corpus (animal-shelter funding, water-council membership,
  water-infrastructure partnerships, a mayor listed as an event attendee) and none of them
  involved a new/expanded agricultural mandate the way Haber/392's buried quote did. Useful
  bound on the problem: within this sample it's a single, specific miss, not a systemic
  failure across many rows — but see the honesty note below on *how* it was caught before
  assuming a future pass would catch the next one automatically.
- **Important methodological honesty, worth remembering before trusting future passes:** the
  subagent reported this only surfaced because it read every article's full text end-to-end
  hunting specifically for büyükşehir/6360 language — nothing in the headline, title, or the
  existing Categories/TopicGloss/Notes metadata would have flagged Haber/392 for review.
  **A plain Categories-vs-TopicGloss consistency check (the original, cheaper idea) would
  NOT have caught this miss** — it required the more expensive targeted full-text re-read
  (Check 2). This matters for cost/effort planning at full-corpus scale: catching every
  buried `Metropolitan_Law`/`Buyuksehir_Law` mention likely requires a dedicated full-text
  pass specifically hunting for that content, not just a cheaper post-hoc consistency check
  on already-generated labels.
- **Ceremonial_undercategorized: 1 hit** (Batch 1, Number 165) — a livestock-facility site
  visit left at zero categories despite similar thin ceremonial content elsewhere in the
  corpus getting a stretch tag. Confirms Orhan's "sometimes ceremonials are just
  Rural_Livelihood" concern was pointing at a real inconsistency, not a non-issue — but only
  1 confirmed instance so far, not evidence of a widespread pattern yet.
- **Categories_vs_Gloss_mismatch: 6 hits**, mostly rows where the classifier's own `Notes`
  already admitted the assigned category was a loose/weak fit (pure hydroelectric-dam
  content tagged `Rural_Development`, wildlife/biodiversity human-interest tagged
  `Agroecology`, animal-welfare content tagged `TR_agroGov`) — these are the known,
  previously-flagged stretch cases, not new problems. **One is a genuine new finding: a
  cross-row inconsistency** — "does irrigation prevent migration" framing got tagged
  `Migration` in three other rows in the sample, but was explicitly considered and rejected
  for `Migration` in this one row, i.e. the same underlying content type was judged
  differently in different rows. This is evidence of within-run inconsistency (not just
  single-row error), worth keeping in mind for any full-corpus run — the classifier isn't
  perfectly self-consistent even within one run over similar recurring content.
  - **Orhan's caveat, 2026-09-12: this may not be pure model inconsistency.** He pointed out
    the irrigation/migration articles likely differ in whether they explicitly reference
    drought ("draught strokes" = drought impacts) as the migration driver — if only some of
    the 4 rows actually mention drought-driven migration risk in their text while others just
    mention irrigation without that framing, tagging them differently would be *correct*, not
    inconsistent. **Not verified either way yet** — before citing this as a clean
    "inconsistency" example (e.g. in the thesis), pull the actual text of all 4 rows and check
    whether the drought/migration framing is genuinely present or absent across them, rather
    than assuming the consistency-check subagent's "inconsistency" framing was correct.
- **Not yet done:** deciding what to actually do about these 8 rows (fix the labels file
  directly, or just document the error rate as a methodology limitation) — that's Orhan's
  call, not something to silently patch into the labels file without him weighing in, since
  it changes reported category counts.

## Full-text scraping status (as of 2026-09-11)

- `agroministry_news_scrape.ipynb` (renamed from `New Text Document.ipynb`) has two scraper
  functions: the original title/date-only pass (produced `agroforest_ministry_news.xlsx`,
  ~6,900 rows) and a fixed full-text pass, `scrape_tarimorman_news_fulltext`, added
  2026-09-11 by `thesis_log_agroministrynews_agent`.
- The full-text pass fixes a real bug found in Orhan's original pilot code (which produced
  the old `tarimorman_haberleri.csv` / renamed `agroforestministry_news.csv`, 8 rows): that
  code ran `soup.find_all("p")` over the whole page, which also captured footer contact
  emails, address/phone/KEP, and accessibility-menu boilerplate present on every page —
  confirmed by inspecting raw HTML and the old 8-row file, where every row had that
  boilerplate appended to `Paragraphs`. The fix scopes extraction to
  `soup.find("div", class_="itemBody")` first. It also added incremental CSV writes (so a
  crash doesn't lose all progress) and resume-by-skipping-already-scraped-Number (so a rerun
  continues instead of restarting) — the same gap Orhan said also hit `resmigazete_scrape`;
  flagged to `thesis_log_main_agent`, who added a reminder to root `CLAUDE.md`'s
  `resmi_gazete/` entry citing this as the reference pattern.
  - **Known non-issue:** Orhan confirmed (2026-09-11) there are gaps in the `Haber/{number}`
    sequence with no error — some numbers just don't correspond to a published article
    (likely retracted/never-published IDs). The scraper already handles this correctly: a
    non-200 response is silently skipped, no retry storm, nothing to fix here.
- The contaminated 8-row pilot was deleted 2026-09-11 so the fixed scraper re-fetches those
  numbers cleanly as part of the full run.
- Full scrape launched 2026-09-11, covering Number 153–7260 (7260 confirmed by Orhan as the
  current latest article; the bare `/Haber/{number}` URL, no slug, verified to resolve
  correctly for it) into `agroforestministry_news.csv`, **completed 2026-09-11**: 7,107 rows
  (one Number in range got no row — a non-200 skip, expected/known non-issue per above), last
  Number reached 7260. 615 of those rows have an empty `Paragraphs` field (no `itemBody` div
  found, or scoped extraction found no non-empty `<p>` text) — not yet investigated why;
  worth spot-checking a few of those URLs before assuming it's fine (could be a different
  page template, e.g. a gallery/video-only post, or a genuine extraction miss).
- Orhan deleted `agroforest_ministry_news_seed.xlsx` and `agroforest_ministry_news.xlsx`
  (2026-09-11) now that the full-text CSV supersedes the title/date-only scrape and its
  keyword-filtered subset — once full text is available, both should be regenerated from
  `agroforestministry_news.csv` rather than treated as the current source. As of this
  writing neither file exists in the folder; don't reference them as current.

## Scope of the "seed sovereignty" proxy (open question, updated 2026-09-11)

- The original `agroforest_ministry_news_seed.xlsx` (77 rows, title-only match) was deleted
  by Orhan along with the title/date-only scrape it was derived from. It was regenerated as
  `agroforestministry_news_seed.csv` (**807 rows**, final — regenerated once more after the
  full scrape completed) from the full-text corpus, matching "tohum" in **either** `Title` or
  `Paragraphs` (case-insensitive) — the ~10x jump in row count vs. the old title-only version
  is expected and is exactly the "catches body mentions the headline misses" effect flagged
  as a recommendation earlier in this file.
- The original keyword search was a **simple keyword search**, not any text analysis. Orhan
  confirmed (2026-09-11) this was just a first-pass keyword proxy, not a finalized
  methodology.
- Orhan spotted "**Ata Tohumu**" ("ancestral/heirloom seed") among the matched titles while
  reviewing that file. This is worth flagging explicitly: "Ata Tohumu" / "atalık tohum" /
  "yerel tohum" (heirloom, landrace, farmer-saved local seed) is conceptually close to
  *opposite* the "sertifikalı tohum" (certified/commercial seed) framing that dominates most
  of the other "tohum" hits (state-driven certified-seed production and export figures —
  an agricultural-modernization narrative, not a farmer-sovereignty one). A single "tohum"
  keyword currently conflates these two narratives even though, in the food-sovereignty
  literature this thesis draws on (e.g. La Via Campesina-style framing), they arguably point
  in different directions for what "sovereignty" means. Recommendation: when the keyword
  filter is revisited, split it into at least two tagged categories rather than one flat
  "tohum" bucket:
  1. **Heirloom/local-seed terms** — "atalık tohum", "ata tohumu", "yerel tohum", "yerli
     tohum çeşidi", "gen bankası", "tohum bankası", "biyoçeşitlilik" (+ likely more found by
     reading through actual matches rather than guessing a fixed list up front).
  2. **Certified/commercial-seed terms** — "sertifikalı tohum", "tohumluk üretimi",
     "tohumculuk sektörü" (the current dominant hits).
  This split hasn't been implemented or discussed with Orhan yet — it's a brainstorm/
  recommendation from 2026-09-11, not a decision. Worth revisiting once full paragraph text
  is available, since the keyword search itself could then run over full text instead of
  titles only (catching articles where "tohum" appears in the body but not the headline).
- Broader NLP-pipeline direction (topic modeling / embeddings over full text, vs. this
  keyword approach) is still the open, unresolved choice noted below and in the "raw
  paragraph text" section — see that for why a heavier pipeline isn't the default
  recommendation yet.

## Open question: is raw paragraph text usable as-is, or does it need summarization? (added 2026-09-11)

Orhan raised this after seeing what full `Paragraphs` text looks like at scale: raw article
text is long, repetitive across similar press releases, and heavy with quote-framing
("Bakan X, ... dedi") that padding out actual informational content. Whether downstream
analysis (keyword indicator, classification, or index construction) should run on raw text
or on some compressed/summarized representation is open. My recommendation, in order of
what to try first:

1. **Start with the lightest option: keyword frequency/presence over full text**, not a
   generative step. This is directly usable for a food-sovereignty *indicator* (e.g. a
   per-article or per-month count of heirloom-seed-related terms), doesn't require a model,
   and is fully auditable/explainable in the thesis — a real advantage for methodology
   defensibility.
2. **If richer signal is needed, prefer sentence-embedding similarity over full
   summarization.** E.g. embed each article (multilingual sentence-transformers, already in
   `requirements.txt`) and compare against a small hand-picked set of reference sentences
   defining "seed sovereignty" vs. "certified-seed modernization" framings, rather than
   generating a summary first. This avoids introducing a generative/hallucination step
   before analysis, which matters for a thesis where every numeric result needs to be
   traceable back to source text.
3. **Full abstractive summarization (transformer-based) as a later, not first, option.** It
   adds a failure mode (summarization drift/hallucination) on top of an already-noisy
   press-release corpus, and — important precedent — `resmi_gazete/`'s BERTopic/tf-idf
   clustering attempts largely did *not* carry the real signal; most of that strand's actual
   insight came from manual annotation on top of the clustering, per root `CLAUDE.md`. Don't
   assume a bigger model fixes what manual review caught there; if summarization is pursued,
   plan to spot-check summaries against source paragraphs the same way, not trust it
   unsupervised.
- This is unresolved as of 2026-09-11 and needs discussion with Orhan before committing to
  any of the above; recorded here as the open question plus a recommended order to explore
  it in, not a decision.

## NLP pipeline proposal, revised after discussion with Orhan (2026-09-11)

An earlier version of this section proposed reusing all ~44 categories from
`literature_research/literature_annotation.ipynb` (read-only reference, outside this
strand's write scope) plus a ranked method list including sentence-embedding similarity and
zero-shot transformer classification. Orhan reviewed it and pushed back / simplified; this
section replaces that version. Keep both the decisions and the reasoning below — a future
session should not silently re-propose the discarded options without knowing they were
already considered.

**On the literature categories:** using all 44 as-is is not adopted. Correction (Orhan,
2026-09-11): the `TR_` prefix is **not** redundant — it deliberately separates
Turkey-specific literature from global/international literature (e.g. `TR_agroEcon` =
Turkey-focused agro-economics sources, `Agro_econ` = global agro-economics sources). Don't
collapse `TR_*` and non-`TR_*` pairs as duplicates; they're an intentional scope split. (The
per-category `.xlsx` exports like `annots_variables.xlsx` mentioned in that notebook are
just Orhan's own viewing convention, unrelated to the `TR_` naming question.) Separately, (a)
most of the 44 are literature-review meta-categories (`Gender`, `Health`, `Migration`,
`History`, `Methodology`, `Variable`, `Survivorship_bias`, `Interdisciplinary`, etc.) that
don't obviously apply to classifying national ministry press releases, so applying the full
list here is likely overreach — a narrower, hand-picked subset (candidates: `Seed`,
`Buyuksehir_Law`, `Agro_policy`, `Land_Policy`, `Food_Sovereignty`, plus their `TR_*`
counterparts where relevant, e.g. `TR_agroGov`/`TR_ruralGov` — since this news corpus is
entirely Turkey-focused, the `TR_*` variants are likely the more directly applicable half of
each pair) makes more sense, but the exact subset is Orhan's call to make, not something to
guess at. Also confirmed as *not a problem*:
multi-label overlap (one sentence/article legitimately matching e.g. both an economy and a
policy tag) is expected and fine — Orhan's own annotation methodology notes in that notebook
already describe using 2-3 categories per annotation. Any classifier built on this taxonomy
should be multi-label (assign zero or more tags per article), not force a single category.

**Method decision, in order of what to actually try:**

0. **Raw word-frequency bag ("keyword-bag") as a diagnostic, done first — empirically, not
   assumed.** Orhan pushed back on an earlier draft of this note that *assumed* "bakan"
   (minister) would be a common, low-signal word without checking. Correct instinct — don't
   guess corpus statistics, count them. Ran a quick check 2026-09-11 (script:
   `word_freq_check.py`, not checked into the repo — lowercase, Turkish stopwords removed via
   `nltk.corpus.stopwords`, tokens <3 chars dropped) over ~7,000 scraped `Paragraphs` at that
   point. Top results: `orman` (17,881), `tarım` (15,136), `milyon` (13,324), `bin` (13,047),
   `türkiye` (12,789), `bakan` (10,714), then minister surnames `pakdemirli` (10,173),
   `eroğlu` (8,614), `yumaklı` (6,908), `çelik` (3,673) — confirming "bakan" and minister
   names genuinely are extremely recurrent, not an assumption. Also surfaced a concrete case
   for lemmatization: fragments like `nin` (7,231) and `nın` (3,199) showed up as "words" —
   these are Turkish genitive-case suffixes that split off because apostrophed possessives
   like "Türkiye'nin" get tokenized on the apostrophe. That's exactly the kind of noise proper
   lemmatization (not just naive regex tokenization) removes. A "keyword-bag" in this sense —
   plain frequency counts, no weighting — is useful as a first empirical look before building
   anything more structured, and confirmed Orhan's instinct to check rather than assume.
1. **Lemmatization is necessary preprocessing, not optional** (Orhan, 2026-09-11, confirming
   the point above). NLTK's `SnowballStemmer` (already available via `requirements.txt`)
   does **not** support Turkish (checked its `.languages` list directly — Turkish isn't in
   it), so it can't be used here. Candidate real options, not yet chosen: `zeyrek` (a Python
   port of Zemberek's Turkish morphological analyzer — proper lemmatization, handles
   agglutinative suffixes correctly, would need adding to `requirements.txt`) or the lighter
   `TurkishStemmer` package (simpler affix-stripping, less accurate than `zeyrek` but no
   heavier dependency). Recommend starting with `zeyrek` given how much suffix noise showed
   up even in the crude frequency check above; needs Orhan's confirmation before adding a new
   dependency, per repo convention.
   - Orhan asked (2026-09-12) whether a BERT-Turkish model's own tokenizer could be used
     instead. Clarified: no — a transformer tokenizer (WordPiece/BPE, e.g. BERTurk's) is not
     a lemmatizer. It splits words into subword pieces to feed a neural network (e.g.
     `tohumculuk` might become `tohum` + `##culuk`), which is a different goal from reducing
     a word to one canonical dictionary form for counting/TF-IDF purposes — it wouldn't merge
     `tohum`/`tohumu`/`tohumculuk` into a single countable feature the way real lemmatization
     does, and subword splits aren't guaranteed consistent enough for that. (Neural,
     transformer-backed Turkish lemmatizers do exist as a separate thing, e.g. Stanza's or
     spaCy's Turkish pipeline, which output actual lemmas rather than subword tokens — but
     that reintroduces the "trained black-box model" concern Orhan already raised about
     embeddings, for little clear benefit over `zeyrek` at this preprocessing stage.)
     Recommendation stands: `zeyrek` (rule-based, deterministic, no training/black-box
     concern) over any BERT-based option here.
   - Orhan asked again (2026-09-12) specifically spaCy vs. `zeyrek`. Additional practical
     point beyond the black-box concern above: spaCy's Turkish pipeline (`tr_core_news_*`)
     is not transformer-backed — unlike spaCy's English/German pipelines, there's no
     transformer variant for Turkish — and its lemmatizer is a simpler lookup-table approach,
     not a dedicated morphological analyzer. For a highly agglutinative language, a lookup
     table can't cover the productive suffix combinations the way `zeyrek`'s proper
     finite-state morphological analysis can, so spaCy would likely handle the exact problem
     found in the keyword-bag check (suffix fragments like `nin`/`nın`) worse, not just
     differently. Final recommendation: **`zeyrek`** — still pending Orhan's go-ahead to add
     it to `requirements.txt` and actually implement it.
2. **TF-IDF and/or statistical keyword extraction — the near-term method, not embeddings or
   any model.** Orhan asked directly what TF-IDF captures: it is pure word-frequency
   statistics, not meaning. It weighs each literal word/token in a document by how often it
   appears there vs. how common it is across the whole corpus — so yes, it can directly
   capture and score words like "tohum" or "toprak" as explicit features per article, and it
   automatically downweights words so common everywhere that they don't distinguish one
   article from another (the keyword-bag check above is exactly how to find out which words
   those actually are for this corpus, rather than guessing). What it gives back concretely:
   a score per (article, word) pair usable to rank articles by how much they're "about" a
   given word, or to compare articles by shared-word overlap. What it does *not* do:
   understand synonyms, paraphrase, or meaning — and depends on lemmatization (step 1) first,
   or "tohum"/"tohumu"/"tohumculuk" stay separate features and dilute the signal.
3. **For automatic keyword extraction (not just scoring a pre-chosen word list): use an
   unsupervised statistical method like YAKE or RAKE**, not TF-IDF alone and not
   BERT-based extraction (KeyBERT etc. explicitly excluded per Orhan's "no BERT for now").
   YAKE/RAKE surface candidate keywords/keyphrases per document from word co-occurrence
   statistics alone — no training data, no embeddings, no black box — which fits Orhan's
   request for "strong mathematical methods" over manual annotation or model-based
   approaches. Neither is in `requirements.txt` yet; would need adding if adopted (both are
   lightweight, no torch/transformers dependency).
4. **Sentence-embedding similarity and zero-shot transformer classification are paused, not
   ruled out.** Orhan flagged confusion about what "comparing embeddings" even means in
   practice — reasonable, since it's the least transparent of the options (a vector-distance
   comparison, not something you can point to a specific word for) and harder to defend/
   explain by hand. Don't pursue either until TF-IDF/keyword-extraction has been tried on a
   subset first and shown to need something richer.
5. **LDA and BERT-based topic modeling: explicitly ruled out for now** (Orhan, 2026-09-11).
   Consistent with the earlier reasoning that `resmi_gazete/`'s BERTopic/tf-idf clustering
   didn't carry its own signal without manual annotation on top.

**Subset-testing plan:** Orhan confirmed testing on a subset first. The "tohum"-matching
subset was regenerated as `agroforestministry_news_seed.csv` (802 rows, title-or-body match
— see seed-sovereignty section above) after the original 77-row title-only version was
deleted; use that plus a comparable random sample as the test subset, rather than the full
~7,100-article corpus. Since methods 2-3 above are automatic/statistical (no training labels
needed), this doesn't
require manual annotation the way a supervised classifier would — Orhan explicitly said he
doesn't know how to manually annotate and would rather rely on mathematical methods, which
TF-IDF + YAKE/RAKE satisfy without needing a labeled training set.

## Lemmatization implementation, validated (2026-09-12)

`zeyrek` implemented in `agroministry_news_scrape.ipynb` (cell after the full-text scraper):
`lemmatize_text()`, `word_frequency_bag()`, `lemmatize_csv()`. Setup needs
`nltk.download('punkt_tab')` in addition to the existing `nltk.download('stopwords')`
requirement (zeyrek's tokenizer needs it; hit a `LookupError` without it) — flagged to main
agent, should be in root `CLAUDE.md`'s Environment section now.

**Bug found and fixed before trusting any result:** zeyrek returns multiple candidate
analyses per word when morphologically ambiguous, and does **not** order them by likelihood.
A first version of `lemmatize_text()` naively took `candidates[0]`, which silently
mis-lemmatized `tarım` (agriculture — one of the most important words in this entire corpus)
into `tar`, and `bin` (thousand) into `binmek` (to ride/mount) — confirmed by running
`analyzer.lemmatize("tarım")` directly and seeing `['tar', 'tarım']` in that order. Fix:
prefer the candidate that exactly equals the raw surface form when one exists among the
candidates (usually the correct "bare root, no suffix" reading), falling back to
`candidates[0]` otherwise. Re-ran the 807-row seed subset after the fix and confirmed via
direct counts: `tarım` 7,410 / `tar` 1 (was inverted before the fix), `bin` 3,146 / `binmek`
118. The `tohum` family also validated: raw surface variants (`tohum` 1,355 + `tohumu` 233 +
`tohumları` 47 + `tohumculuk` 141 + `tohumluk` 167 + `tohumların` 92 = 2,035 counted
manually) merge into a single lemmatized `tohum` count of 2,941 — higher than my manual
sum because lemmatization also catches inflected forms I didn't think to enumerate by hand
(e.g. "tohuma", "tohumdan"), which is itself a point in favor of lemmatizing over hand-listing
keyword variants.

**Known residual errors — not fixed, flagged not hidden:**
- `yumak` (1,816 occurrences) is almost certainly Minister Yumaklı's surname
  ("Yumaklı" → wrongly split as `yumak` + suffix) — zeyrek's lexicon likely doesn't have this
  proper name, so it falls back to the closest common-noun analysis ("yumak" = ball of yarn).
  Proper nouns not in the lexicon are a known weak spot for this approach.
- `bun` (2,134 occurrences) is a mis-lemmatization of demonstrative pronoun "bu" (this)
  inflected forms (bunun/buna/bunu). The *correct* lemma "bu" is only 2 characters and would
  have been auto-dropped by the `len(w) < 3` short-token filter — but the wrong 3-character
  lemma "bun" slips past that filter instead, so it shows up in frequency lists as if
  meaningful. Worth adding "bun" to `LEMMA_STOPWORDS` directly if it keeps appearing.
- `üremek` (to reproduce/breed) still appears where `üretmek` (to produce) is almost
  certainly meant in an agricultural-production context (e.g. "ürettikleri" → wrongly
  "üremek"). This is genuine ambiguity the exact-surface-match fix can't resolve (neither
  candidate matches the raw surface), and would need real context-based disambiguation to
  fix properly — not attempted, out of scope for the current rule-based approach.
- None of these are severe enough to block moving to TF-IDF (step 8) — recorded so a future
  session doesn't mistake `yumak`/`bun`/`üremek` showing up in results as meaningful signal.

Output: `agroforestministry_news_seed_lemmatized.csv` (807 rows, adds a
`Paragraphs_Lemmatized` column) — this is the input for TF-IDF/YAKE next (roadmap #8-9), not
yet run on the full ~7,100-article corpus.

**NER / entity extraction: discarded (Orhan, 2026-09-11).** An earlier version of this note
proposed running NER over `Paragraphs` (location entities as a possible bridge to
`econometric_models_and_vars/`'s city-level panel, person entities as an administration/
minister-tenure marker, org entities for institutional actors). Orhan decided against it —
concern that it adds noisy, wordy output at the wrong grain; this strand should stay at the
subject/document level (what an article is about) rather than trying to pull out individual
entities within it. Not to be re-proposed without Orhan raising it again.

## Cross-strand coordination outcome, 2026-09-12: how this strand's output will likely get used

Orhan had this session, `thesis_log_officialgazette_agent`, and `thesis_log_econometrics_agent`
each share category thinking with `thesis_log_main_agent` for a coordinating remark. Two
takeaways specific to this strand, from that remark:

- **Framing: "policy activity/attention," not GFSI's "political commitment."**
  `thesis_log_econometrics_agent` had floated the Global Food Security Index's "political
  commitment to adaptation" sub-dimension as a possible model for a missing FSOI political
  category. `thesis_log_officialgazette_agent` pushed back, and main agent agreed: both this
  strand's seed/policy keyword tagging and the Gazette's Agreements/Supports classification
  measure policy *activity/output* (what got announced, legislated, funded), not attitudinal
  *commitment* — forcing either into GFSI's "commitment" label would mischaracterize what's
  actually being measured. Main agent is recommending to Orhan that this become its own
  "policy activity/attention" framing instead of borrowing GFSI's term.
- **Structural: not a 7th FSOI category — a separate national-level companion signal.**
  Because this strand's data is national-level only (see NER/city-tagging decision above —
  declined), it cannot function as a category alongside the other 6 city-year FSOI indicators
  (`econometric_models_and_vars/` — market/production/water/waste/energy/land-use): a
  national-constant value can't explain cross-city variation, which is what the PSM/DiD
  design in that strand relies on. Main agent is recommending to Orhan this become a separate
  national-level companion signal/narrative rather than a slot-in FSOI category.
- **Nothing changes for current work here** — this doesn't block or redirect the
  TF-IDF/keyword-extraction plan above. It's downstream framing for how the eventual output
  gets used/labeled, not a change to what to build next. Recorded so a future session doesn't
  re-litigate "should this be a 7th FSOI category" or reach for GFSI's "political commitment"
  language without knowing this was already discussed and decided against, 2026-09-12.

**Status:** nothing above is implemented yet. TF-IDF/keyword-extraction on a subset is the
agreed next concrete step once Orhan confirms which literature categories (if any) to target
first; embeddings/zero-shot remain paused, not planned.

## Coordination behavior: don't assume CLAUDE.md is unaffected

- When you rename/move/delete a file in this folder, check CLAUDE.md's **current** text
  (re-read it, don't rely on what you last saw or expect) for a reference to that filename
  before telling the main agent "no CLAUDE.md change needed." Twice (2026-09-11) that
  claim turned out to be wrong — CLAUDE.md had a pointer that needed updating both times,
  and the main agent had to catch and fix it after the fact. Only the main agent actually
  edits CLAUDE.md, but a strand agent giving it a wrong "nothing to update" signal defeats
  the point of flagging changes at all.
