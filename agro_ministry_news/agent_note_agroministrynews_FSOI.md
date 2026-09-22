# Agent note: agro_ministry_news scope and pipeline (AI-authored working note)

This file is AI-authored pipeline documentation for future sessions working on this strand.
Anything about result validity should live in the root `CLAUDE.md`, not here.

**How this file is organized (restructured 2026-09-19).** The file had grown to ~1,265 lines
of mixed current-status and historical record, with the current status buried among dated
entries it had already superseded. It is now in three parts:

- **Part 1 — Current State:** what is true right now. Open decisions, live data inventory,
  next steps. **This part wins wherever it disagrees with anything below it.**
- **Part 2 — Reference:** stable facts that don't change batch to batch — pipeline
  architecture, module contents, schema, category codebook, standing rules.
- **Process history** — the dated record of how the strand got here — now lives in a separate
  file, **`agent_note_agroministrynews_history.md`** (split out 2026-09-21 to keep this file
  loadable). You do not need it to start work; go there for the reasoning behind a decision,
  for methodology write-up material, or before re-proposing an approach that may already have
  been tried and abandoned.

**No content has been deleted across any of these reorganisations** — sections were moved, and
where prose was condensed the original was moved to the history file verbatim. If the history
file contradicts Part 1, **Part 1 is correct** and the history text is a record of what was
true at its own date.

---

# PART 1 — CURRENT STATE

*Last updated 2026-09-22. Figures here were verified directly against the files rather than
carried over on trust; where a claim was measured, the measurement is named.*

**Two open decisions closed since the 2026-09-19 handoff:** annotation UX (#1, tool built) and
year-binning (#2, settled by measurement plus Orhan's direction). What remains genuinely open
is the golden-corpus round 2, the `Metropolitan_Law` rename, and the smaller items — see
"Open decisions" below.

## Data inventory, verified 2026-09-19

Re-checked by direct row/column count at handoff, not assumed from the previous note:

| File | State |
|---|---|
| `agroforestministry_news.csv` | Scraped rows **7,107**, of which **6,492 are usable articles** (have both text and a date). 615 have empty `Paragraphs` — diagnosed 2026-09-21, see below |
| `annotate_tool.py` | Local annotation UI for the `Orhan_Category` column — see Part 2 |
| `agroforestministry_news_validation_sample.csv` | **500 rows, 500 distinct Numbers, zero duplicates.** Columns: `Number, URL, Title, Date, Paragraphs` |
| `agroforestministry_news_validation_sample_CLAUDE_LABELS.csv` | **500 rows, 500 distinct Numbers, zero duplicates.** Columns: `Number, Categories, Ceremonial_Political, Comment, Orhan_Category` |
| `agroministrynews_module.py` | The pipeline code — `TarimOrmanScraper`, `ValidationSampleBuilder` |
| `agroministrynews_scrape.ipynb` | Example-usage cells importing from the module |

**Classification coverage: 500 / 6,492 usable articles = ~7.7%.** All 500 are classified;
`Orhan_Category` is **empty in all 500 rows** — Orhan's annotation pass has not started.

### The 615 empty-`Paragraphs` rows: diagnosed 2026-09-21 (closes roadmap #5)

Open and untouched since 2026-09-11. Investigated directly; it splits cleanly in two, and
**most of it is not an extraction failure at all**:

- **559 rows — dead URLs, not scraper bugs.** These have no date and no usable title either.
  375 carry the site's own removal notice as their title (*"Aradığınız içerik yayından
  kaldırılmış veya silinmiş olabilir"* — "the content you are looking for may have been
  removed or deleted"); the other 184 are completely blank. The ministry site returns **HTTP
  200 with a removal page** rather than a 404, so the scraper had no way to tell these from
  real articles. Nothing to fix and nothing to recover — **exclude them.**
- **56 rows — genuine extraction misses, worth a look if anyone needs them.** These have a
  valid date *and* a real article title, but no body text was extracted. Spread thinly across
  2013–2026. A visible cluster is older ALL-CAPS-titled posts from the *Orman ve Su İşleri
  Bakanlığı* era, which suggests a different page template the `itemBody` selector doesn't
  match. At 56 rows (0.9% of usable articles) this is low-priority, but it is the only part of
  the 615 that represents actually-lost content.

**Consequence for any counting work: the denominator is 6,492, not 7,107.** Quoting 7,107 as
the corpus size overstates it by ~9%, since 559 of those rows are dead URLs.

**Also confirmed: zero rows have article text but no parseable date.** So year-binning has no
missing-date problem — every article that can be analysed can also be placed in a year. The
`Date` column parses as `%d.%m.%Y` (e.g. `27.06.2013`, with a trailing space).

### Per-year article counts (computed 2026-09-21)

Raw counts across the usable corpus. Originally computed so the year-binning decision could be
made against real numbers rather than in the abstract; it did settle that decision (open
item #2). **This is still a diagnostic, not an adopted output** — no raw-count series has been
produced as a deliverable.

| Year | Articles | With text | In sample | Sample % |
|---|---|---|---|---|
| 2013 | 155 | 151 | 21 | 13.9 |
| 2014 | 103 | 99 | 22 | 22.2 |
| 2015 | 225 | 223 | 24 | 10.8 |
| 2016 | 748 | 741 | 47 | 6.3 |
| 2017 | 1,043 | 1,041 | 64 | 6.1 |
| 2018 | 772 | 770 | 52 | 6.8 |
| 2019 | 674 | 672 | 42 | 6.2 |
| 2020 | 582 | 580 | 40 | 6.9 |
| 2021 | 273 | 273 | 25 | 9.2 |
| 2022 | 478 | 467 | 37 | 7.9 |
| 2023 | 446 | 444 | 33 | 7.4 |
| 2024 | 325 | 324 | 30 | 9.3 |
| 2025 | 393 | 388 | 33 | 8.5 |
| 2026 | 331 | 319 | 30 | 9.4 |

**Two things this makes concrete, both relevant to the pending decision:**

1. **Publication volume is wildly uneven — 2017 has 1,043 articles, 2014 has 103, a 10x
   spread.** A raw count per year measures ministry *publishing behaviour* at least as much as
   policy activity. Whatever is built, it likely needs a rate or share rather than a bare
   count, or an explicit caveat that the denominator moves.
2. **Per-year sample sizes are small and uneven (21–64 rows, 6.1%–22.2%).** This is the
   concrete argument against extrapolating *category* rates per year from the current 500-row
   sample: a category appearing in 3 of 21 articles in 2013 cannot be compared to one
   appearing in 40 of 64 in 2017 without very wide error bars. Per-year category counts really
   do need full-corpus classification, not clever reuse of the pilot sample.

### Can per-year *category* rates actually carry a trend? Quantified 2026-09-21 — mostly no

The point above ("per-year sample sizes are small, so category rates would be noisy") was an
assertion until it was measured. Measured, it was stronger than expected — and it **did**
settle open item #2 (Orhan, 2026-09-22: qualitative approach for category-level work; raw
counts unaffected).

Wilson 95% confidence intervals on per-year category rates from the current 500-row sample:

| Category | Rate range across years | Typical 95% CI half-width |
|---|---|---|
| `Agro_econ` | 17%–64% | **±10 to ±19 pp** |
| `Rural_Development` | 9%–41% | ±9 to ±16 pp |
| `Seed` | 0%–16% | ±3 to ±14 pp |
| `Metropolitan_Law` | 0%–7% | ±3 to ±10 pp |

A ±15pp interval on a rate that only moves 20pp across the whole period cannot support a
claim about any individual year. `Agro_econ` in 2021 reads 64% [45%, 80%] on n=25 — the
apparent spike is not separable from sampling noise.

**How much classification would fix it?** To distinguish a 20% rate in one year from a 30%
rate in another at 95% confidence needs **~293 classified articles per year**, i.e. **~4,100
in total** — against 500 done, and 63% of the usable corpus.

**The part that cannot be fixed by more classification:** four years don't *contain* 293
usable articles, even if every one were classified — **2013 (151), 2014 (99), 2015 (223),
2021 (273)**. This is a hard ceiling set by how much the ministry published, not by effort.
Two-year bins only partly help: 2013+2014 is still only 250.

**What follows for open item #2:**
- **Raw article counts per year are sound** — no sampling error at all, since they count the
  whole corpus. Available immediately.
- **Per-year category rates are not currently supportable**, and would need ~8x the existing
  classification to become marginal rather than good. If they're wanted anyway, they need
  published confidence intervals and probably two-year bins, presented as indicative rather
  than as a measured trend.
- **A per-year `Metropolitan_Law` series is not viable at any realistic sample size** — 4 hits
  in 500 rows, 0 in most years. Treat that category qualitatively (the specific articles, read
  and quoted) rather than as a time series. Given it is the thesis's most important category,
  this is worth knowing before anyone plans a chart around it.

**Reproduce:** the script is not checked in; it joins the sample's `Date` to the labels'
`Categories`, computes Wilson intervals per year, and solves the two-proportion sample size.
Regenerate rather than trusting these figures if the sample grows.

**Coverage note: the corpus starts in 2013**, so it cannot observe the pre-Law-6360 baseline
(the law passed 2012, effective 2014). This strand can show post-law policy-activity
variation but not a before/after comparison on its own. Structural, not a data-quality
problem — no better scraping fixes it, and it holds whichever binning option is chosen.

**The overlap with `resmi_gazete/` is narrower than either strand alone (noted 2026-09-21).**
Root `CLAUDE.md` records the Gazette strand's validated coverage as **2000–2024**; this
strand runs **2013–2026**. The two combine only over **2013–2024**:

- **2000–2012** — Gazette only. This is the entire pre-law period, so any before/after
  framing rests on the Gazette strand alone. This strand contributes nothing to it.
- **2013–2024** — both. The only window where a combined "policy activity" signal is
  genuinely supported by both sources.
- **2025–2026** — this strand only (~724 articles). Beyond the Gazette's validated range.

**Practical consequence:** when the two strands are combined for the GFSI
"political commitment" discussion (see the cross-strand sections in Part 2 and root
`CLAUDE.md`), the defensible joint series is 2013–2024, not either strand's full extent.
Don't present a combined series running 2000–2026 — it would be single-sourced at both ends
while appearing continuous. Worth confirming with `thesis_log_officialgazette_agent` whether
2025–2026 Gazette data could be added, since that would close the late gap; the early gap
cannot be closed at all.

**`Metropolitan_Law` tagged in 4 rows** (Haber/4207, 3757, 3666, and 392 after its manual
correction). Verified by direct count. See the Haber/392 saga in the history file before
reporting this number anywhere — the category is systematically easy to miss in this corpus.

## The one thing most likely to be misread

**Classification is not automated and cannot be.** Scraping and sample-building are plain
Python with no LLM involved. `build_classification_prompt()` returns a prompt *string* — it
does not call any model. Actual classification is a manual `Agent`-tool call made by whichever
session is running this strand, because Orhan has Claude Code Pro only, with no separate
Anthropic API key. **It will never happen by calling a function.** Full mechanics in Part 2.

**To get the prompt text when spawning a subagent**, see Part 2 → "The classification prompt,
in full" — the complete prompt is pasted there (snapshot 2026-09-21), along with the launch
settings (`subagent_type="general-purpose"`, `model="sonnet"` = **Sonnet 5**) and the
regeneration snippet. `agroministrynews_module.py` stays the source of truth: if the prompt or
category list ever changes, change it there and regenerate that block rather than editing the
pasted text by hand.

## Open decisions — need Orhan's input, do not guess

Ranked by what is actually blocking, not by age.

1. ~~**Annotation UX**~~ — **RESOLVED 2026-09-21, tool built.** Orhan, 2026-09-15: *"I will
   need to find an easy to annotate way to add my labels since CSV not easily readable by
   me."* Resolved by building **`annotate_tool.py`** — see "Annotation tool" in Part 2 for how
   to run it and how it works. Orhan chose the local-server design over a no-server HTML file
   specifically so annotations save as he types into their own separate
   `..._ORHAN_LABELS.csv` (his call — Claude's labels file is never written), rather than
   needing an export step. **This no longer blocks his 500-row pass.**
2. ~~**Year-binning**~~ — **effectively settled 2026-09-22 by Orhan, after measurement.** Open
   since 2026-09-17. Resolved not by picking an option but by the precision analysis above
   ("Can per-year *category* rates actually carry a trend?") showing what the data can bear.
   Orhan's direction: *"So year based trend is impossible. We need to take a qualitative
   approach."* **What that does and does not mean — get this right, the distinction is easy to
   over-apply:**
   - **Category-level per-year series: not supportable.** ±10–19pp confidence intervals, ~8x
     the current classification needed to become marginal, and four years that don't contain
     enough articles at any level of effort. A `Metropolitan_Law` per-year series is not viable
     at all. These go qualitative — specific articles read and quoted.
   - **Raw article counts per year remain sound and are NOT covered by "impossible."** They
     count the whole corpus, so they carry no sampling error whatsoever. Orhan's phrasing was
     about trends in *category rates*; confirmed with him and independently flagged to him by
     `thesis_log_main_agent` the same day. **Don't discard the raw-count series on the strength
     of the qualitative turn** — if it's used, the live caveats are the 10x publication-volume
     spread (a bare count partly measures the ministry's own publishing behaviour, so prefer a
     rate/share or state the caveat) and excluding 2026 as a partial year.
   - **Nothing has actually been built yet.** No raw-count series has been produced as a
     deliverable — the per-year table above is a diagnostic. Ask before building one.
   - **Cross-strand note:** `resmi_gazete/` reaches the same "no per-year category trend"
     conclusion by a different route — it has *no* sampling error (its annotated set is the
     full population, so counts are exact) but the population is sparse. It can carry coarse
     era-binned category composition that this strand cannot. Per root `CLAUDE.md`, the agreed
     convention is raw counts per year for cross-strand comparability, plus era-binned
     composition for the Gazette only, labelled as a different granularity rather than
     silently mixed.
3. **"Golden corpus" validation round 2.** Orhan's proposal: he hand-annotates the existing
   500, then a fresh random 500 is drawn and classified for a blind validation pass
   (agreement statistic), netting ~1,000. He asked "how does that sound" and got a positive
   reaction; that was never a go-ahead to execute. Two practical constraints stand: (a) for
   round 2 to be genuinely blind, his annotation must happen independently of seeing Claude's
   labels for the same set — confirm the intended order before starting; (b) a 100-article
   batch already hit the Pro rate limit once, so 500 more means budgeting across multiple
   sessions.
4. ~~**`Buyuksehir_Law` → `Metropolitan_Law` rename**~~ — **DONE 2026-09-22.** Orhan authorised
   it for this strand specifically: *"I will rename once I get literature_research, so for you
   it is Metropolitan_Law is okay."* Applied in three places together so they cannot drift:
   `CATEGORY_LIST` and both prompt references in `agroministrynews_module.py`; the 4 tagged
   rows in the labels CSV (Haber/392, 3757, 3666, 4207 — verified no other field changed, row
   count and order preserved, backup taken first); and the pasted prompt snapshot in Part 2,
   regenerated from the module rather than hand-edited.
   **Known and accepted divergence:** `literature_research/literature_annotation.ipynb` still
   uses `Buyuksehir_Law`. That is deliberate, not an oversight — Orhan will rename it there
   himself when he next works on that folder, which has no strand agent and is read-only here.
   **Until he does, the two taxonomies genuinely differ**, so don't "fix" the literature
   notebook, and expect the old name when reading it or any pre-2026-09-22 output.
5. **Smaller, all still open:** the tentative `Water_Security` category idea; the tentative
   `Magazine_events` catch-all; the acknowledged ethnicity/traditional-events scope gap (a
   deliberate limitation of the lit review's scope, not a bug to fix by inventing a category);
   whether to re-run batches 1–2 to regenerate their `Comment` field in the richer
   free-flowing style (Orhan: *"let's stay same no need to do it now"* — revisit only if he
   raises it). **Topic glossary** is downgraded to "probably redundant given Comments +
   `KNOWN_GAP_TYPES`" — not an active task.

## Why `Metropolitan_Law` is near-absent — Orhan's interpretation, 2026-09-22

**This reframes the strand's central negative result, and should be carried into the thesis
rather than treated as a data limitation.** Orhan, on being shown the 4-hits-in-500 count and
the finding that no per-year series is viable:

> *"I expect that Buyuksehir Law did not yield any results. It is a governmental policy, and
> only theoretical research interpret is as a rural problem."*

**The argument:** Law 6360 is framed by the state as **administrative/municipal reform**. Its
reading as a *rural* or *agricultural* problem is a scholarly interpretation — the one this
thesis's literature review adopts — not a framing the government itself uses. So the near-total
absence of the law from agricultural policy discourse is **what the theory predicts**, not a
failure of the corpus or of classification.

**Two measurements support it — but they are NOT equally strong, and the difference matters
(Orhan, 2026-09-22).**

- **This strand — the stronger evidence.** 4 hits in 500 articles, zero in most years,
  measured **over full article text**, not headlines. We know the full-text read works for
  this specifically: Haber/392's hit was a single buried quote near the end of an article
  about an agricultural fair, invisible from its title. So a near-zero count here is a
  genuine statement about article *content*.
- **`resmi_gazete/` — weaker than it first appears.** The result (of 112,157 Gazette titles
  2000–2024, 195 mention `büyükşehir`/`6360`, 2,416 mention `tarım`, **0 mention both**) is
  measured on **titles only**. The Gazette corpus *is* titles — full text exists only as long
  PDFs that have not been gathered, and Orhan's assessment is that collecting them may not be
  feasible at all. **A legislative title is a short, formulaic naming string**, so it would
  frequently fail to mention two domains even where the body text connects them. The zero
  intersection is therefore **consistent with** disjoint domains but cannot distinguish that
  from "titles are too short and formulaic to co-mention anything." Suggestive, not probative.

**So state the claim at the strength the evidence supports.** The defensible version is that
**ministry press releases — full text, 500 sampled — almost never connect Law 6360 to
agriculture**, and that Gazette *titles* show the same pattern, with the title-only limitation
stated plainly. What is **not** supported is a flat assertion that agricultural and
metropolitan-governance language are disjoint across all official state text; that would be
claiming a full-text result from title-only data. An examiner would find that quickly, and the
weaker honest claim is still interesting.

**Do not let the two measurements be presented as equal or "converging."** They differ in
kind: one is full-text and can support a content claim, the other is a title-level probe.

**The distinction that must not be lost when writing this up: discursive absence is not causal
absence.** These two strands measure what the state *says*. They cannot show that Law 6360 had
no material effect on agricultural outcomes — that question belongs to
`econometric_models_and_vars/` and the TÜİK panel, which can still find effects in the data
regardless of whether any ministry press release or Gazette title ever connected the two.
Stating or implying "no discourse, therefore no effect" would be a real error. The honest
formulation is: *the state did not frame Law 6360 as an agricultural policy; whether it
functioned as one is a separate, empirical question.*

## Known risk worth carrying into any full-corpus run

**`Metropolitan_Law` / `Metropolitan_Law` is the category most directly tied to the thesis's
research question, and the one this corpus hides best.** The strongest confirmed evidence in
the pilot (Haber/392) was a buried quote from a local official near the end of an article
about an agricultural fair — a careful classification pass missed it entirely, and it was
recovered only by a full-text re-read hunting specifically for büyükşehir/6360 language. A
cheap Categories-vs-Comment consistency check **would not** have caught it; this was tested.
Planning implication: catching these at full-corpus scale needs a dedicated targeted pass for
this category, not general classification plus a post-hoc audit. Full account in the history
file.

## Handoff status

Current session took over this strand on 2026-09-19 (clean handoff, nothing mid-flight);
`thesis_log_main_agent` was notified. Detail in the history file.

**Standing note:** this file contains deliberate "this was true then, corrected here"
annotations. They look like clutter but each marks a real past error — don't strip one without
preserving what it warns about.

---

# PART 2 — REFERENCE

*Stable facts. Change these only when the underlying thing actually changes.*

## Annotation tool — `annotate_tool.py` (built 2026-09-21)

**What it is.** A local annotation UI for recording Orhan's own category labels. Built because
raw CSV was not a workable editing surface for 500 rows of long Turkish article text (Part 1,
open decision #1, now resolved). Run it from `agro_ministry_news/`:

```
python annotate_tool.py
```

It starts a local server, opens the browser, and shows one article at a time: full scraped
text, title/date/link to the original, and Claude's `Categories`, `Ceremonial_Political` and
`Comment` beside a free-text box. It resumes at the first unannotated article.

**Files — this is the important part:**

| File | Access |
|---|---|
| `..._validation_sample.csv` | read (article text) |
| `..._validation_sample_CLAUDE_LABELS.csv` | **read only, never written** |
| `..._validation_sample_ORHAN_LABELS.csv` | **written — the only file this tool modifies** |

**Orhan's labels live in their own separate file** (his call, 2026-09-21: *"I don't want to
change claude label file, let's keep it separate"*). The first version of this tool wrote
`Orhan_Category` back into the Claude labels file; he caught that and asked for separation
before starting. **He was right** — keeping the machine labels and the human labels in
physically separate files means the human annotation is a genuinely independent artifact, the
classification work cannot be damaged by a bug in this tool, and the comparison between the
two is a join rather than a diff against a mutated file. Join on `Number`.
Columns: `Number, Orhan_Category, Annotated_At`. Only annotated rows are written, so the
file's row count is the progress count.

**Design choices — don't undo these without asking:**
- **Local server, not a standalone HTML file.** Orhan's choice, 2026-09-21. A page opened via
  `file://` cannot write to disk, so a no-server version would have needed an export step and
  a manual move out of Downloads. The server saves each answer as he types (~600ms debounce).
- **Random presentation order, fixed seed** (`SHUFFLE_SEED = 42`), so it is identical on every
  run. Orhan asked whether file order would do, since the sample was already randomly drawn —
  it nearly would, but not quite: file order is batch order, and **batches 1–2 were
  year-stratified while 3–5 were plain random**, so the first 170 rows are not a random
  subset. Randomising the presentation means that if annotation stops partway (likely, at 500
  rows), whatever is finished is still a representative sample of the 500 rather than skewed
  toward the year-stratified early batches. Note the order depends on the row set — if the
  sample ever grows past 500, the order changes.
- **Free text, deliberately NOT constrained to the 44-category codebook**, no dropdown or
  autocomplete. That is the entire point of the column: new candidate categories are meant to
  emerge from concrete rows (see "New workflow" below). Orhan was offered clickable category
  chips and declined them.
- **Writes are atomic** (temp file + `os.replace`), with a timestamped `.backup_` copy before
  the first write of each session.
- **Automatic free-port selection.** Closing the browser tab does *not* stop the server, so
  re-running while an old copy is alive is the normal case — it would otherwise fail with an
  "address in use" traceback and never open the browser. This actually happened to Orhan on
  2026-09-21 (an orphaned process from an earlier run held port 8000). The tool now scans
  8000–8009 and prints whichever URL it used.
- **`os.chdir` to the script's own directory at startup**, so it behaves the same from a
  terminal, VS Code's Run button, or a double-click.
- **Standard library only**, except `openpyxl` (already a dependency) for the optional
  `.xlsx` export. Nothing to add to `requirements.txt`.

**The `.xlsx` export is a formatted snapshot for reading/sharing, not a source of truth** —
it joins article + Claude labels + Orhan labels into `..._sample_ANNOTATED.xlsx` and is never
read back in.

**Verified 2026-09-21** against sandbox *copies*, never the real files: 500 articles load and
join correctly; the Claude labels file is byte-identical (SHA-256) after writes; values with
commas, quotes, embedded newlines and Turkish characters round-trip exactly; presentation
order is confirmed non-file-order, stable across restarts, and a permutation of the same row
set; timestamps survive reload; clearing a value removes its row; the backup is made once with
no `.tmp` left behind; port fallback was exercised against a live server; and all HTTP
endpoints were driven end-to-end.

## Pipeline architecture, in one paragraph

**Pipeline architecture, in one paragraph — read this before touching anything:**
Scraping (`TarimOrmanScraper`) and sample-building (`ValidationSampleBuilder.grow_sample` /
`get_unclassified` / `append_labels`, all in `agroministrynews_module.py`) are **plain
Python, fully automatic, no LLM involved.** The one exception is
`build_classification_prompt()` — it only *returns a prompt string*, it does **not** call any
model. **Actual classification (reading articles, deciding categories, writing the output
CSV) is not code at all — it's a manual step done by whichever session is running this
strand, via the Claude Code `Agent` tool** (Orhan has Claude Code Pro only, no separate
Anthropic API key, so there's no way to automate this with a script). Concretely: take the
string `build_classification_prompt()` returns, pass it to the `Agent` tool
(`subagent_type="general-purpose"`, `model="sonnet"`), wait for it to write the output CSV,
then call `append_labels()` on that file. A future session must do this step itself every
time — it will never happen by just calling a function.

## Code consolidation, 2026-09-14: `agroministrynews_module.py`

Orhan pointed out the sample-drawing scripts (`draw_batch*.py`) only ever existed as
session-local scratchpad files, never committed — meaning the actual scrape/sample/classify
pipeline was implicitly documented in this note and in prompt text, with no real code artifact
in the repo. Fixed by creating **`agroministrynews_module.py`** (mirrors
`resmi_gazete/resmigazete_module.py`'s class-based style, which itself already cited this
strand's scraper as its reference pattern):

- **`TarimOrmanScraper`** — the full-text scraper (`scrape_resumable`), moved out of the
  notebook. Same logic as before (itemBody-scoped extraction, retry adapter, resume-by-
  skipping-Number), just as a proper class instead of a notebook cell.
- **`ValidationSampleBuilder`** — everything around building the cumulative validation
  sample: `grow_sample()` (plain random, excludes already-sampled Numbers, ends with the
  mandatory duplicate check above), `get_unclassified()` (Number set-difference between the
  cumulative sample and cumulative labels files — this is what to feed a classification
  subagent next), `build_classification_prompt()` (returns the exact prompt text for the
  `Agent` tool — **does not call an LLM itself**, since Orhan has Claude Code Pro only, no
  separate Anthropic API key; classification stays an interactive-session subagent call, not
  something this module can do on its own), and `append_labels()`. **No batch numbering** —
  see the "No batch numbering" section in Part 2; an earlier
  version of this class (`draw_batch`/`extract_batch`/`append_batch_labels`, all tagging rows
  with a `Batch` column) was replaced 2026-09-14, and both cumulative CSVs had their `Batch`
  column stripped to match. The 44-category codebook and the accumulated `KNOWN_GAP_TYPES`
  list are class constants (`CATEGORY_LIST`, `KNOWN_GAP_TYPES`) — **update these in the
  module when they change, and update the prompt-template documentation below in the same
  edit**, so the two can't drift apart the way the old copy-pasted-per-batch prompts did
  (see the "Standardized subagent classification prompt" section's own note about that
  exact failure mode).

**Sanity-checked against real data before trusting it:** ran `check_duplicates()` against the
actual 500-row cumulative file and confirmed it reproduces the known result (320, 1215) before
relying on the module for anything.

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

### Where the classification prompt lives

**`agroministrynews_module.py`'s `build_classification_prompt()` is the single source of
truth.** The full prompt text is pasted below as a dated snapshot at Orhan's request
(2026-09-21) — when the prompt, `CATEGORY_LIST` or `KNOWN_GAP_TYPES` change, change them in
the module and regenerate that block; never hand-edit the pasted copy.

**Why this rule is stated so firmly:** a hand-maintained copy of the prompt used to live in
this note and went stale *twice* — once caught when Orhan asked "are you giving the same
prompt every time?", then again after the batch-numbering redesign. Re-syncing a second copy
doesn't fix that pattern, it just delays the next failure.

#### The classification prompt, in full (Orhan's request, 2026-09-21)

**Why this copy exists.** The prompt previously lived only in
`agroministrynews_module.py`, because a hand-maintained copy in this note went stale twice
(see the correction note immediately above). Orhan asked for it to be visible here anyway —
his reason: it is harder to track down when spawning a subagent if it only exists inside the
`.py` file, and the category list and prompt wording are not expected to change again
("we will not be changing probably afterwards").

**So this is a deliberate, accepted tradeoff, not an oversight.** The rule that prevents the
old drift bug from returning:

> **`agroministrynews_module.py` remains the single source of truth.** If the prompt,
> `CATEGORY_LIST`, or `KNOWN_GAP_TYPES` ever DO change, change them in the module and
> regenerate this block — never edit the text below by hand.

**Snapshot regenerated 2026-09-22** directly from
`ValidationSampleBuilder.build_classification_prompt(100, "to_classify.csv", "new_labels.csv")`
— pasted verbatim from that call's output, not retyped. 4,801 characters. The three arguments
(`n_rows`, `input_csv_path`, `output_csv_path`) are interpolated into the text, so change
those three values to match the actual run.

**Which model to use — clarified by Orhan, 2026-09-21: Sonnet 5.** Every classification
subagent is launched with the `Agent` tool, `subagent_type="general-purpose"`, `model="sonnet"`.
Orhan confirmed the intended model is **Sonnet 5** (`claude-sonnet-5`); the `Agent` tool's
`model` parameter only accepts the short alias `sonnet`, which resolves to the current Sonnet
generation, so `model="sonnet"` is how you request it — there is no way to pin an exact
version string through this parameter.

**How strong is the evidence that the 500 classified rows were Sonnet 5? Moderate — state it
carefully in the write-up.** Orhan's basis (2026-09-21): *"It was probably sonnet 5 I only had
that model visible in vs code."* That is consistent with Sonnet 5, but it is not proof, for a
specific reason worth understanding: **the `Agent` tool's `model` argument is independent of
whatever model the interactive session itself is running.** The model shown in the VS Code
picker governs the orchestrating session, not the subagent — a session running as Opus still
spawns `model="sonnet"` subagents. So "only Sonnet 5 was visible in VS Code" tells us about
the parent session, not directly about the subagents. Combined with the alias resolving to the
current Sonnet generation, Sonnet 5 is the most likely answer for recent work and is
**confirmed as the intended model going forward**. For the batches run 2026-09-12/13, the
honest statement is "Claude Sonnet, via Claude Code's subagent mechanism; the exact minor
version was not pinned or logged at the time" rather than asserting a specific version.
Don't overstate this in a methodology section — an unverifiable precise claim is worse than a
verifiable general one.

Note also there is no `effort` parameter available on the `Agent` tool (see "Model and effort
settings" above).

```text
You are helping with an MA thesis on Turkey's Food Sovereignty Index. Part of the project scrapes press releases from the Turkish Ministry of Agriculture and Forestry (tarimorman.gov.tr) and classifies what each article is about, using a fixed category codebook from a separate literature-review strand (literature_research/literature_annotation.ipynb). This is a batch of 100 newly-added, not-yet-classified articles from an ongoing pilot — the researcher reviews this output and adds his own additional categories on top of it afterward (an `Orhan_Category` column gets added downstream, not by you), so your job is a careful first-pass classification, not a final answer.

Read this CSV file in full (100 rows, will need multiple Read calls with offset/limit — read every row, don't stop partway):
to_classify.csv

Columns: Number, URL, Title, Date, Paragraphs.

For EACH row, read Title and Paragraphs and produce:
1. `Categories`: zero or more labels, semicolon-separated, chosen ONLY from this exact 44-category list (do not invent new names, multi-label is normal, 2-3 tags per article is typical):
Agro_econ, Agro_international, Agro_policy, Agro_tech, Agroecology, Autonomy, Big_agro, Metropolitan_Law, Collectives, Cooperatives, Debt, Deruralization, Education, Food_Network, Food_Security, Food_Sovereignty, Gender, Health, History, Interdisciplinary, Land_Consolidation, Land_Policy, Land_Use, Migration, Monoculture, Monoculture_Poli, Policy_Access, Risks_Global, Rural_Development, Rural_Family, Rural_Livelihood, Rural_Policy, Rurban, Seed, Shortfood, Small_holder, Survivorship_bias, TR_agroEcon, TR_agroGov, TR_landUse, TR_ruralGov, TR_Peasant, Urbanization, Variable

Guidance on recurring content without an obvious single-category home — multi-tag onto the closest existing categories rather than inventing new ones:
- Irrigation/dam/flood-control infrastructure -> TR_ruralGov, Rural_Development, Agro_policy, or Land_Policy depending on framing
- Wildfire/forestry-disaster response -> Risks_Global, TR_agroGov, or leave uncategorized if nothing fits
- Livestock/animal husbandry/veterinary content -> Agro_econ, TR_agroGov, TR_ruralGov, Rural_Livelihood, Agroecology depending on angle
- Ceremonial/political content: don't assume ceremonial framing means no category applies — a ceremonial village visit can still genuinely touch e.g. Rural_Livelihood; tag what's substantively present even if the framing is ceremonial. Only leave zero categories for content with truly no agricultural/rural substance.
- Most of the 44 are literature-review meta-categories that may rarely apply — don't force usage.
- Food_Sovereignty: apply strictly and rarely — near-universally top-down state framing in this corpus, genuine bottom-up content is very rare.
- Watch specifically for Turkey's 2012 Metropolitan Law (büyükşehir belediyesi/belediyeleri gaining new agricultural/rural responsibilities, "6360", or similar) even as a small buried detail in an otherwise unrelated article — this is the single most important category for this thesis, and real hits have been found buried deep in unrelated-seeming articles. Read every article's full text with this specifically in mind, not just its main topic. Tag Metropolitan_Law if found and quote/describe the relevant passage explicitly in the Comment.

2. `Ceremonial_Political`: "yes"/"no" — primarily ceremonial/photo-op/personal messaging with little substantive policy content? Can co-occur with a real category.
3. `Comment`: a few sentences (not just one) covering what the article is actually about, independent of the category list, plus anything ambiguous, low-confidence, or where a category was a stretch to fit, plus explicitly flag topics that don't fit any of the 44 categories well. Known recurring gap types found in prior batches — name these explicitly when you see them: water security/infrastructure, forestry/wildfire-disaster management, cross-institution/inter-ministry collaboration or policy councils (Şura/forum/commission format), food-waste/sustainability content, refugee/migration-driven resource demand, overseas farmland leasing/investment, dam-driven cultural-heritage resettlement, wildlife/biodiversity monitoring with only incidental farmland relevance, routine food-safety/inspection announcements. Also flag any NEW gap type not on this list if you see one.

Write output as a CSV to:
new_labels.csv

Columns: Number, Categories, Ceremonial_Political, Comment

Be deliberate and consistent. Process all 100 rows, no sampling/skipping. When done, report: rows processed, full category tally, count of Ceremonial_Political=yes, how many rows got zero categories, any Metropolitan_Law hits (quote the relevant passage), and a list of rows flagging any of the known gap types or new ones not seen before.
```

**To regenerate this block** (the only supported way to update it) run from
`agro_ministry_news/`:

```python
from agroministrynews_module import ValidationSampleBuilder
b = ValidationSampleBuilder(
    "agroforestministry_news.csv",
    "agroforestministry_news_validation_sample.csv",
    "agroforestministry_news_validation_sample_CLAUDE_LABELS.csv",
)
print(b.build_classification_prompt(100, "to_classify.csv", "new_labels.csv"))
```

Full launch sequence for a classification run:

```python
b.get_unclassified("to_classify.csv")   # what still needs labels (set difference by Number)
# -> hand the prompt above to the Agent tool: subagent_type="general-purpose", model="sonnet"
# -> wait for it to write new_labels.csv, then:
b.append_labels("new_labels.csv")
```

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

**The full 44-category codebook is NOT reproduced here — deliberately.** It lives in
`agroministrynews_module.py` as `CATEGORY_LIST`, and appears in full inside the pasted
classification prompt above. A third copy in this section was removed 2026-09-21: it had
become the same duplication problem that already caused two staleness incidents in this
strand. The codebook originates in `literature_research/literature_annotation.ipynb` cell 1 —
re-verify against that notebook if the list is ever suspected stale, and update the module,
not this file.

**How to apply it** (this is the part worth keeping in prose):
- **Most of the 44 are literature-review meta-categories** (`Gender`, `Health`, `Migration`,
  `History`, `Interdisciplinary`, `Survivorship_bias`, etc.) that may rarely or never apply to
  ministry press releases. That's expected — don't force usage just to spread across the list.
- **`Food_Sovereignty` specifically: apply strictly, don't stretch it.** Batches 1–2 found it
  applies almost never to this corpus (0/70, then 0/100). Treat continued near-zero usage as a
  **finding about the data source** — a ministry's own press office does not publish in
  food-sovereignty framing — not as a sign the classifier is missing things.

## Model and effort settings for classification subagents

**Model/effort settings for classification subagents — clarified 2026-09-19.** The `Agent`
tool used to spawn every classification subagent only exposes a `model` parameter
(`sonnet`/`opus`/`haiku`/`fable`) — there is **no `effort` parameter available**, so no
session has ever chosen an effort/reasoning-depth level for these subagents; whatever depth
they ran at was the harness's own default for a `general-purpose` subagent, not a deliberate
choice. What *was* deliberately and consistently set on every call: `model="sonnet"`,
explicitly, independent of whatever model the orchestrating/interactive session itself runs
as (e.g. switching the interactive session to Opus-5 does **not** change what the
classification subagents use unless the `Agent` call's `model` argument is also changed).
If Orhan wants an effort-controlled comparison for the annotation task specifically, that
needs the raw Anthropic API (`output_config.effort`) — not reachable through this pipeline's
Claude-Code-subagent architecture as currently built.

## No batch numbering

**No batch numbering — eliminated 2026-09-14, Orhan's call** ("seems redundant to say it's
arbitrary and still apply it, we may delete it" — correct instinct, it wasn't actually
necessary). The `Batch` column has been stripped from both sample CSVs entirely (renamed
2026-09-14 from "cumulative" to "sample" too — see the module's docstring for why). Growing
the sample and finding what still needs classifying are both just set operations on article
`Number` now (`grow_sample()` / `get_unclassified()`) — there's nothing to number, track, or
avoid colliding with. If you see any reference to `batch_num`, `draw_batch`, `extract_batch`,
`append_batch_labels`, `cumulative_csv`, or `cumulative_labels_csv` anywhere (this note
included, below this point, or your own memory of earlier in this session) — those are old
method/parameter names from before this redesign, already replaced in the actual code.

## Duplicate-check rule for sample growth

**Duplicate-check rule for batch draws (Orhan, 2026-09-14): mandatory going forward.**
Checked the full 500-row cumulative sample directly: **2 duplicate Numbers exist — 320 and
1215, both Batch 1 + Batch 2.** These predate the dedup fix: batches 1 and 2 were each drawn
independently (different seeds, no exclusion of the other's numbers) before batch 3 started
excluding already-sampled Numbers from the eligible pool. **Batches 3, 4, and 5 are
confirmed clean — zero duplicates**, since their draw scripts already read the cumulative
file's existing Numbers and excluded them before sampling (see the `draw_batch*.py` pattern
in scratchpad). So this isn't an ongoing bug, just two known legacy rows — but Orhan is right
that nothing was *automatically verifying* this, it was only caught by manually checking when
asked.

**Rule, effective immediately: every sample growth must end with an explicit duplicate check
that prints its result**, not just rely on the exclusion logic being correct.
**Superseded by the module below** — `ValidationSampleBuilder.grow_sample()` now calls
`check_duplicates()` automatically every time, so this is enforced in code, not just as a
note to remember. If new duplicates appear beyond the known 320/1215 pair, stop and
investigate before classifying anything new — don't classify a set that might contain an
accidental re-draw.

## Full-text scrape — durable facts

The scrape itself is done and is not going to be re-run. What a future session needs:

- **The corpus is `agroforestministry_news.csv`**, covering `Haber/` Numbers 153–7260,
  completed 2026-09-11. For row counts and what is actually usable, see Part 1's data
  inventory — **don't quote a corpus size from anywhere else in this file.**
- **Extraction is scoped to `soup.find("div", class_="itemBody")`, deliberately.** Scraping
  `<p>` tags across the whole page pulls in footer contact details and accessibility-menu
  boilerplate that appear on every page. If extraction is ever rewritten, keep this scoping.
- **Gaps in the `Haber/{number}` sequence are normal, not errors** (Orhan confirmed
  2026-09-11): some numbers were never published or were retracted. A non-200 response is
  silently skipped — correct behaviour, nothing to fix.
- **The scraper is resumable** and writes incrementally, so a crash or rerun continues rather
  than restarting. `resmi_gazete/`'s module was later built on this same pattern.

*The narrative of how the original pilot scraper's boilerplate bug was found and fixed, and
the intermediate file renames, moved to the history file 2026-09-21.*

## Cross-strand decisions — see root `CLAUDE.md`

**These decisions are recorded in root `CLAUDE.md` and are not restated here.** A copy in this
note would be a future stale copy; a pointer cannot drift. (This strand has now twice caught
`CLAUDE.md` carrying claims that were false for ten days, so duplication is a demonstrated
problem, not a theoretical one.) Read `CLAUDE.md` for the current wording of:

- **FSOI stays at 6 categories, no 7th** — this strand's output does not become a category in
  `econometric_models_and_vars/`'s city-year panel. Political influence is modelled as uniform
  across cities, matching this strand's national-only scope.
- **The GFSI "political commitment" approximation and its two mandatory caveats** — that both
  sources measure policy activity/output rather than attitudinal commitment, and that both are
  official-source self-reporting and so skew toward appearing committed. `CLAUDE.md` is the
  authority on how these must be phrased.
- **`zeyrek` removed from `requirements.txt`** and the switch from rule-based lemmatization to
  Claude-based classification.

**Year-binning** is an open decision, not a settled one — see Part 1, open decision #2, for
its current status and the numbers bearing on it. (An earlier version of this section
described it using a 7,107-article corpus figure, which is wrong: 7,107 is the scraped row
count and 6,492 is the usable article count. See Part 1's data inventory.)

**File status note — kept here because this is its only record:** Orhan deleted
`agroforestministry_news_seed.csv` (the 807-row "tohum" keyword subset) and
`agroforestministry_news_seed_lemmatized.csv` (its `zeyrek`-lemmatized version) — confirmed
gone. Both belonged to the lemmatization/TF-IDF branch superseded by the LLM classification
pivot; nothing in the current pipeline reads either file. Don't go looking for them or treat
their absence as something broken. If the "tohum" subset is ever needed again it is one line
to regenerate: filter `agroforestministry_news.csv` for "tohum" in `Title` or `Paragraphs`.

## If you are a new session picking this up

**If you are a new session picking this up:** notify `thesis_log_main_agent` that a handoff
happened (per root `CLAUDE.md`'s continuity section) so an identity change in `ListAgents`
isn't mistaken for something unusual.

**Read Part 1 and Part 2 of this file in full before doing anything.** They are short and both
are load-bearing — the pipeline design and the reasoning behind several corrected mistakes
live there, and skipping either has already caused real repeated errors (e.g. the
`Metropolitan_Law` miss on Haber/392, caught only by manual re-reading).

**You do not need to read `agent_note_agroministrynews_history.md` to start work** — it is the
dated record, split out 2026-09-21. Go to it when you need to know *why* something was decided,
when writing methodology, or before re-proposing an approach (several were tried and
abandoned for recorded reasons).

## Coordination behavior: don't assume CLAUDE.md is unaffected

- When you rename/move/delete a file in this folder, check CLAUDE.md's **current** text
  (re-read it, don't rely on what you last saw or expect) for a reference to that filename
  before telling the main agent "no CLAUDE.md change needed." Twice (2026-09-11) that
  claim turned out to be wrong — CLAUDE.md had a pointer that needed updating both times,
  and the main agent had to catch and fix it after the fact. Only the main agent actually
  edits CLAUDE.md, but a strand agent giving it a wrong "nothing to update" signal defeats
  the point of flagging changes at all.

---

# Process history

Moved to **`agent_note_agroministrynews_history.md`** on 2026-09-21 — nothing was deleted.

It holds the dated record: the batch-by-batch classification results, the pivot from
rule-based NLP to LLM classification, the `zeyrek` bugs, the Haber/392 Metropolitan Law saga,
the category-scheme evolution, and the superseded status sections. Read it when you need the
reasoning behind a decision, when writing up methodology, or before re-proposing an approach —
not to start work.
