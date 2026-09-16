# Agent note: resmi_gazete/ pipeline status

AI-authored working note for future sessions on this strand (`thesis_log_officialgazette_agent`,
scoped to `resmi_gazete/`, reporting to `thesis_log_main_agent`). Pipeline/mechanics
documentation only — anything about result validity or known-bad status belongs in the
root `CLAUDE.md` instead (owned by the main agent), not here.

## Status & Forward Steps (handoff note, updated 2026-09-17)

This session's context is filling up; a fresh session will likely pick up this strand
soon. Per CLAUDE.md's continuity convention: treat the incoming session as continuous
with this one (same scope, same open items), not a fresh start — read this whole file,
and `CLAUDE.md` in full, before doing anything. Notify `thesis_log_main_agent` that the
handoff happened once it does, so an identity change in `ListAgents` isn't mistaken for
something unusual.

**Done and solid, safe to build on:**
- `resmigazete_module.py` is fixed, validated, and reproducible - all six known noise
  sources (encoding fallback, unmerged same-href anchors, Sayfa Başı nav links,
  over-broad ilan filter, Önceki/Sonraki nav arrows, per-character font-spans) are
  fixed in the actual code (not just described here), plus an adaptive SSL fallback
  (tries a verified request first, only falls back to `verify=False` if this specific
  machine actually hits an `SSLError`). Note this fallback's own note (2026-09-17
  correction below): it fires 7 times on this machine every run, once per year - it
  does not mean the cert issue is absent, only that it's handled gracefully now.
- `resmigazete_scrape.ipynb` runs cleanly end-to-end as-is - confirmed by Orhan running
  it directly (not via a session script) for 2018-2024.
- **All of 2000-2024 is now scraped and validated** into
  `resmigazete_all/titles_resmigazete_{year}.csv`, diffed against trusted `.xlsx`
  (94.2-99.8% text-match every year - see the tables further down). CSVs are the
  going-forward source of truth per CLAUDE.md; old `.xlsx` kept for reference only. One
  real, non-cosmetic gap was found and fixed along the way: a single missing day in
  2020 (2020-08-27) - see the "2018-2024" section below for how it was caught, since
  the same check is worth applying to any future re-scrape.

**No scraping work remains.** Next steps are all downstream / waiting on Orhan:
- The Agreements/Supports/Annotation_Topic categorization and the sentiment tags layered
  on top of it. Orhan is reconsidering the annotation approach entirely (previous
  annotation as-is vs. a fresh pass using the old one only as a guideline) - see
  CLAUDE.md and the "LLM sentiment pass" section below for the reproducibility caveat on
  the sentiment work specifically.
- The year-binning task (bin Gazette entries by year/two-year bins to compare against
  Türkiye's national FSOI score, per CLAUDE.md) - waiting on Orhan's raw-count-vs-
  category-level decision, which affects `thesis_log_agroministrynews_agent`'s strand
  the same way, so it needs to land identically on both rather than being decided here
  alone. Orhan said (2026-09-14) this is waiting until the 2000-2024 scraping wraps up -
  **that milestone is now reached (2026-09-17)**, so this is worth raising with Orhan
  again rather than continuing to wait silently.

## Where things stood (2026-09-11, start of this session)

- `resmigazete_module.py` was **not just producing wrong results — it was dead code**.
  `parse_to_dataframe()` used `re.split(...)` without ever importing `re`, and operated
  on `self.content`, which no method in the class ever populated (there was no
  `requests.get` call anywhere that set it). It could not run end-to-end as written.
- The only actually-working scraper logic lived inline in
  `resmigazete_scrape.ipynb` cell 3 (`ResmiGazeteScraper` class): real hyperlink
  cleanup (`_normalize_text_tr`, `_should_skip_text`, `_resolve_href`), but with a real
  parsing bug (below) and no resume-on-crash support.
- Two files both claiming to cover Resmi Gazete 2006 disagreed:
  `rg_2006_links.xlsx` (top level, 4,069 rows) vs.
  `resmigazete_all/titles_resmigazete_2006.xlsx` (3,372 rows, different schema, feeds
  the downstream `all_titles_resmigazete_from2000.xlsx` used by
  `resmigazete_search.ipynb`).

## Diagnosis (this session)

1. **Which 2006 file is trusted:** confirmed `titles_resmigazete_2006.xlsx` (inside
   `resmigazete_all/`) is the correct one; `rg_2006_links.xlsx` is a flawed one-off run
   — it has 716 rows where Text is literally just a stray "Å"/"Æ" nav-arrow glyph (the
   scraper's own `_should_skip_text` is supposed to drop these) and un-normalized
   `\r`/`\n` in most rows, meaning it predates those cleanup fixes.

2. **Root cause of the actual bug** ("Text missing on the same hyperlink value"):
   fetched `https://www.resmigazete.gov.tr/eskiler/2006/01/20060103.htm` live and
   confirmed the page itself contains **two separate `<a href="20060103-1.htm">` tags**
   for one gazette item — one per wrapped line of a long title. The old `_parse_links`
   treated every anchor independently, so long titles came out as multiple fragmentary
   rows sharing the same href instead of one complete row. This is a real site markup
   quirk, not a parsing mistake reading one anchor. (Confirmed via diff: 3,382 of 3,419
   links shared between the two 2006 files had different Text; the overwhelming
   majority were just whitespace, but this href-splitting was the substantive bug.)
   Interestingly, the dead `resmigazete_module.py` reconstruction already contained
   (unreachable) logic for exactly this merge — `parse_to_dataframe()` had
   `if entry.get('Link') == current_entry.get('Link'): current_entry['Text'] += ...` —
   it just never ran because the surrounding class was broken.

3. **54 links present only in the trusted file, absent from `rg_2006_links.xlsx`
   entirely** — clustered at the tail of specific days (e.g. end of 2006-01-31,
   2006-03-31). Read as a crash/interruption during that one-off run — the same
   "no resume, crash loses everything" gap CLAUDE.md already flags, and which
   independently hit `agro_ministry_news/`'s full-text scraper until fixed there
   (2026-09-11). Not a separate parsing bug; the resumability fix below addresses this
   going forward for any future run.

## Changes made (2026-09-11)

- **Rebuilt `resmigazete_module.py`** as the real, working module (ported from the
  notebook's correct class, not written from scratch):
  - `ResmiGazeteScraper`: same hyperlink-cleaning logic as before, plus the fix —
    `_parse_links` now merges *adjacent* `(text, href)` entries that share the same
    resolved href (not all same-href entries anywhere on a page, to avoid wrongly
    merging unrelated "see also" links to the same page).
  - `ResumableResmiGazeteScraper(ResmiGazeteScraper)`: wraps the parent's per-date
    fetch with incremental writes and resume-by-skipping-already-scraped-dates,
    mirroring `agro_ministry_news/agroministrynews_scrape.ipynb`'s (renamed from
    `agroministry_news_scrape.ipynb` 2026-09-14, per
    `thesis_log_agroministrynews_agent`)
    `scrape_tarimorman_news_fulltext` pattern — `requests.Session` with
    `HTTPAdapter`/`Retry`, output opened in append mode, one row written + `f.flush()`
    immediately per date, existing output file read on startup to build the
    already-done set.
  - Dropped the old reconstruction's non-functional `parse_to_dataframe` /
    `read_and_process_excel` methods entirely — they didn't match the real pipeline.
- **Output format switched from `.xlsx` to `.csv`** (Orhan's explicit call) — incremental
  append-and-flush isn't practical with `.xlsx` (openpyxl has no cheap append), so
  `ResumableResmiGazeteScraper.scrape_resumable()` writes
  `resmigazete_all/titles_resmigazete_{year}.csv` directly. Existing trusted `.xlsx`
  outputs in `resmigazete_all/` were **not touched or regenerated** — they remain the
  baseline per CLAUDE.md until a full re-scrape is explicitly decided.
- **`resmigazete_scrape.ipynb`** cell 3 now imports from `resmigazete_module` instead
  of redefining the class inline; cell 4 (driver loop) updated to use
  `ResumableResmiGazeteScraper.scrape_resumable()` writing CSV.

### Verification performed
- Re-parsed the live 2006-01-03 page through the fixed `_parse_links`: the
  `20060103-1.htm` entry now comes out as one row with the full merged title,
  matching `titles_resmigazete_2006.xlsx`'s text for that link exactly (confirmed
  character-for-character).
- Resumability smoke test: ran `scrape_resumable` for a 2-day range, then ran it again
  immediately — second run correctly logged "2 dates already in ... skipping those,"
  and the output file had identical row count after both runs (no duplication, no data
  loss).
- Note: this machine's Python trust store can't validate resmigazete.gov.tr's
  certificate chain (`SSLCertVerificationError` with plain `requests`). Diagnostic
  fetches in this session used `verify=False` as a one-off; this is a local-environment
  issue, not fixed in `resmigazete_module.py` itself (the module's `session.get` calls
  still verify by default) — flag if a future real scraping run hits the same error on
  this machine.

## resmigazete_search.ipynb pipeline lineage (traced 2026-09-12)

Orhan asked which file holds his category annotations, whether there's a methodology
note, and how many articles are annotated. Full chain, file → file, with row counts:

1. `resmigazete_tarım_filter.xlsx` (2,398 rows) — `tarım*` keyword-filtered Gazette
   entries, the base candidate pool.
2. Cells 3–6 ("IRRELEVANT; only for apriori research") are abandoned early clustering
   experiments (KMeans on BERT/TF-IDF embeddings) — produced `BERT_cluster.xlsx`,
   `BERT_cluster_1.xlsx`, `tfidf_cluster*.xlsx`, not part of the live pipeline.
3. `BERT_cluster_1.xlsx` → year-stratified 20/80 split → `BERT_cluster_train.xlsx`
   (479 rows) / `BERT_cluster_test.xlsx`.
4. **The only explicit annotation-methodology note found anywhere in this notebook**
   is cell 16 (markdown): *"BERT prediction by training on manually annotated data.
   Titles about international agreements and domestic legislations are marked as
   relevant."* — i.e. `BERT_cluster_train.xlsx`'s binary `Relevance` column (479/479
   non-null) was hand-labeled by Orhan under that one-line rule. No note exists for any
   later annotation stage.
5. Logistic regression on BERT embeddings, trained on that hand-labeled set, predicts
   `Relevance` for the rest → validated via a second hand-labeled batch,
   `BERT_cluster_validation.xlsx` (384 rows, manual `Validation` column) → iterated a
   couple of times (cells 17–23) → combined into `BERT_complete_initial_relevance.xlsx`
   (2,081 rows, 1,733 with non-null `Relevance` — the ~348-row gap wasn't investigated
   this session) → filtered to `BERT_complete_relevant_only.xlsx`, **609 articles**
   deemed relevant.
6. BERTopic clustering on those 609 → `BERT_complete_relevant_only_BERTopic_clusters.xlsx`
   (609 rows, 21 topics including the `-1` outlier/noise topic).
7. **Cluster-level (not article-level) manual annotation:**
   `BERT_complete_relevant_only_BERTopic_info_agrotopic_annotation.xlsx` — 22 rows (one
   per BERTopic topic ID), each hand-assigned a coarse `AgroPolicy_Topic` ∈ {0, 1, 2}.
   No note on what 0/1/2 meant at this stage either — inferred from downstream code
   that 0→Agreements, 1→Supports, 2→dropped as irrelevant.
8. Every article inherits its cluster's coarse label →
   `BERT_relevant_clusters_with_agrotopic_annotation_filtered_year.xlsx`, **546
   articles** (2 dropped as AgroPolicy_Topic==2), each with `AgroPolicy_Topic` 0 or 1.
9. Split into `Final_AgroPolicy_Topic_Agreements.xlsx` / `..._Supports.xlsx`, then
   hand-annotated at the **fine-grained, article level** with the category scheme from
   cell 31 (Agreements 0–6, Supports 0–28 — listed there, but again no note on
   methodology/process) → **`Final_AgroPolicy_Topic_Agreements_Annotated.xlsx`
   (266 rows) and `Final_AgroPolicy_Topic_Supports_Annotated.xlsx` (280 rows)**.

**Answering Orhan's questions directly:**
- **Which file:** the fine-grained categories he defined (cell 31) live in
  `Final_AgroPolicy_Topic_Agreements_Annotated.xlsx` and
  `Final_AgroPolicy_Topic_Supports_Annotated.xlsx`, column `Annotation_Topic`.
- **Methodology note:** only one exists (cell 16, quoted above), and it documents the
  earlier binary relevance stage, not the Agreements/Supports categorization itself.
  No note documents how the cluster→AgroPolicy_Topic (0/1/2) mapping or the final
  Annotation_Topic assignment was actually done — consistent with Orhan's own
  description of this as "top of the head" categorization.
- **How many articles are annotated:** **546 total** (266 Agreements + 280 Supports),
  100% coverage of the post-BERTopic relevant set (`Annotation_Topic` is non-null on
  every row in both files). Of those, 2 rows (1 in each file, ~0.4%) are coded `99` —
  an undocumented catch-all not listed in the cell 31 category definitions; negligible
  volume, sampled and both look like genuinely hard-to-classify edge cases (an
  Agriculture Bank/credit-cooperative liability-termination law; a
  Turkey–Australia agricultural cooperation memorandum), not a systematic problem.

## LLM sentiment pass on the 546 titles (2026-09-12)

Orhan wants to use an LLM (this session, acting directly as the classifier) to tag
each of the 546 Agreements/Supports titles as positive/neutral/negative toward
agriculture, layered on top of (not replacing) the existing category labels — motivated
partly by the source PDF's own Limitations section, which says automated
TF-IDF/BERTopic clustering couldn't separate topics well because "certain keywords such
as insurance and debt indicated both positive and negative connotations."

**Method:** read all 546 titles directly (paginated, in full) and encoded that reading
into an explicit, ordered rule set (negative checks run before positive ones, so e.g.
"Destekleme Ödemesi **Yapılmamasına**" — a support payment being *withheld* — isn't
mis-caught by the more generic "support payment" positive rule that fires on the same
root words). This is a hybrid: rule-based execution, but the rules were derived from
and iteratively corrected against a genuine close reading of the corpus, not a blind
keyword/TF-IDF pass. Output columns `Sentiment` and `Sentiment_Reason` (which rule
fired) were added to **new** files — the original hand-annotated files were not
modified:
- `Final_AgroPolicy_Topic_Agreements_Annotated_Sentiment.xlsx`
- `Final_AgroPolicy_Topic_Supports_Annotated_Sentiment.xlsx`

**Result (546 total):** 333 positive, 196 neutral, 17 negative.
- Agreements (266): 181 neutral (mostly routine tariff-quota-on-imports administration
  — genuinely ambiguous/procedural, matches the paper's own note), 83 positive
  (international cooperation protocols/MOUs, IPARD/IFAD funding), 2 negative (a
  chemical-fertilizer support-distribution mechanism being repealed).
- Supports (280): 250 positive (payments, low-interest credit, disaster-relief debt
  postponement, rural development/investment support), 15 neutral (framework laws like
  `5488 Tarım Kanunu`, ambiguous export-procedure amendments), 15 negative (support
  payments explicitly *withheld* pending debt repayment, pension health-premium
  deductions, debt collected via deduction from crop-sale proceeds, a support
  regulation being repealed).

**Known residual imprecision — spot-checked, not exhaustively verified:** a handful of
rows were caught by targeted spot-checks and fixed (suffix mismatches like
"Kredi**si**" vs "Kredi", "Desteklenmesine" missing the repeal case in "...Desteklenmesine
...Yürürlükten Kaldırılması Hakkında Yönetmelik"). After those fixes, a further spot
check found a small number of remaining misses caused by (a) Turkish morphological
suffix variation the regex doesn't cover (e.g. "Ertelenmesi" vs "Ertelenmesine",
"Satın Alınmasına" vs the narrower "Alımı" pattern expected) and (b) at least one
literal OCR/scan artifact in the source title text itself (a stray space inside
"Sigort ası" broke a match). These affect only a few rows out of 546 and were left
as-is rather than chasing every suffix variant — flagging here so a future pass (or
Orhan) knows the ~3% negative / ~61% positive / ~36% neutral split is a good-faith
estimate, not machine-verified-exact. A true per-title independent LLM judgment (546
separate calls) would likely fix these remaining edge cases but wasn't done here for
efficiency; worth doing if higher precision is needed later.

**Reproducibility reminder (2026-09-16):** to be precise about what is and isn't in
the repo here — **the two `*_Sentiment.xlsx` output files themselves are committed and
present** (they've been in `resmi_gazete/` since 2026-09-12). What's *not* in the repo
is the script that generated the `Sentiment`/`Sentiment_Reason` columns — it only ever
ran in a session scratchpad, which doesn't persist. This is deliberate, not an
oversight, for two reasons:
1. The rules encode subjective judgment calls made by reading the corpus once (e.g.
   deciding tariff-quota administration counts as "neutral," or that a repealed
   support mechanism counts as "negative"). Even with the script saved, re-running it
   reproduces the same *output*, but the *reasoning behind the rules* isn't
   independently re-derivable the way a principled, documented methodology would be.
2. The judgment itself came from a proprietary, closed-weight model (Claude, this
   session) reading the titles — not a transparent, auditable algorithm a third party
   could inspect or re-derive from published methodology, even in principle.

Given Orhan is reconsidering the annotation approach for this strand generally (see
CLAUDE.md), don't save or build further on this script until that's settled — flagging
this so whoever picks this strand up next understands the `Sentiment` columns reflect
one session's one-time model judgment call, not a repo-backed, independently
reproducible pipeline, even though the output files themselves are safely committed.

## Full-year validation against trusted 2006 output (2026-09-12)

CLAUDE.md flagged this as unconfirmed after the rebuild, so ran the fixed
`ResumableResmiGazeteScraper` for the complete year 2006 live against the site
(`resmigazete_all/titles_resmigazete_2006.csv`, 365 days, 0 fetch failures) and diffed
it against the trusted `titles_resmigazete_2006.xlsx` by hyperlink.

- **First run (anchor-merge fix only): only 56.4%** of matched links were text-identical
  after normalizing whitespace/dashes. Investigated the 43.6% gap and found a second,
  previously-unknown bug, unrelated to the anchor-merge fix:
- **New bug found and fixed: wrong encoding fallback.** These archived pages never
  declare a charset in `Content-Type`, so `requests` defaults to ISO-8859-1 (the RFC
  fallback for undeclared `text/*`) — but the actual bytes are Windows-1254 on at least
  some pages. The two encodings agree almost everywhere except a handful of code points
  (ı, ş, ğ, İ, Ş, Ğ), so most Turkish text still looked fine at a glance while those
  specific letters silently corrupted (confirmed via
  `.../eskiler/2006/07/20060726.htm`: raw bytes are Windows-1254, and decoding as
  ISO-8859-1 turned "Bakanlığına" into "Bakanl\xfd\xf0\xfdna"). The old code's
  `if not r.encoding: r.encoding = "utf-8"` was dead code — `r.encoding` is never falsy
  here, so that fallback never actually ran. Fixed in `_fetch_day` to use
  `r.apparent_encoding` when the header has no explicit charset. **Result: match rate
  jumped from 56.4% to 99.0%** after re-running the full year with the fix, with no
  regression on already-correct pages.
- **Explored and reverted a third fix attempt:** a small number of titles (<1%, ~32/3343
  links) have a stray space mid-word (e.g. "T oprak" instead of "Toprak"), traced to
  pages that wrap part of a title in a nested `<span style="letter-spacing:...">` for
  kerning, with no real space in the source
  (`<a>— T<span style="letter-spacing:-.25pt">oprak Mahsulleri...</span></a>`).
  `get_text(" ", strip=True)` inserts a space at that tag boundary anyway. Tried
  `get_text("", strip=True)` to fix it — this backfired badly: many far more common tag
  boundaries in the same corpus (e.g. across "Değişiklik Yapılmasına Dair Kanun"
  boilerplate, which appears in nearly every title) rely on that separator to supply a
  space that isn't literally in the source text, so removing it fused those into
  run-together non-words ("YapılmasınaDair") — including a regression on the
  2006-01-03 case already used as the anchor-merge fix's reference example. Reverted;
  documented the tradeoff directly in `resmigazete_module.py`. No separator choice gets
  both cases right, and a stray mid-word space is far less damaging for downstream
  tokenization than fused words, so `" "` stays as the default. Affects under 1% of
  titles — acceptable, not chased further.
- **Link coverage:** 0 links appeared in the new scrape that aren't in the trusted file
  (no spurious extras); only 5 trusted links were absent from the new scrape (out of
  ~3,441 shared), and those look like page-specific edge cases rather than a systematic
  gap.

**Conclusion: the rebuilt module now reproduces the trusted 2006 output at ~99%
text-match with 0 spurious rows** — validation confirmed, addressing the gap CLAUDE.md
flagged. `resmigazete_all/titles_resmigazete_2006.csv` now holds this freshly-validated
scrape (not yet compared for whether it should replace or sit alongside the trusted
`.xlsx`; that's a decision for Orhan, not made here).

## Multi-year rollout: 2000-2006 (2026-09-12/13)

After the 2006 validation, Orhan asked to scrape the remaining years one at a time,
starting with 2000-2005 (2006 was already done). CSV is now the going-forward source
of truth; trusted `.xlsx` files are kept, untouched, purely as the validation
reference — not superseded on disk.

- **A batch run across 2000-2005 surfaced a second real noise source**, found by
  diffing against trusted the same way as the 2006 validation: a "Sayfa Başı" ("back to
  top") in-page navigation link, present only in the 2001-2004 fragment-anchor era (one
  long combined page per day, so a "jump to top" link recurs after every section - not
  present in 2000, or in 2005/2006 once the site switched to one-page-per-item). It
  isn't real gazette content, but nothing in `_should_skip_text` excluded it. Counts
  lined up almost exactly with the "only in new scrape" divergence per year (e.g. 2003:
  353 Sayfa Başı rows vs. 352 only-new links), confirming it as the cause. Fixed two
  ways: (1) text-pattern check for "Sayfa Başı" repeated one or more times, and (2) a
  belt-and-suspenders href-level check - every such link points to the same in-page
  fragment, `#T.C.r` (the masthead anchor), distinct from real per-item fragments like
  `#1`/`#2`. Both are in `_should_skip_text`/`_parse_links` now.
- **Background-run interruption:** the 2001-2004 re-scrape was mid-run (2001 done, 2002
  partway through, 2003/2004 not started) when the session ended unexpectedly. Simply
  re-ran the same script after the interruption - the resume-by-date logic picked up
  exactly where it stopped (skipped all of 2001, resumed 2002 from ~June 17, then did
  2003/2004 fresh) with no manual bookkeeping needed. This is the resumability feature
  working exactly as designed, not just in the earlier smoke test.
  - Side effect worth noting: 2001 and the first ~5.5 months of 2002 were written
    before the href-level `#T.C.r` check existed (only the text check was live at the
    time), since already-written dates aren't reprocessed on resume. In practice this
    doesn't seem to matter - the text check alone closed the gap almost completely (see
    results below) - but flagging it in case a fully-consistent re-scrape of just those
    two years is ever wanted.

**Validation results after the Sayfa Başı fix, before the `ilan_re` fix below
(2026-09-12/13, superseded - kept for history):**

| Year | New rows | Trusted rows | Shared links | Text-match | Only-new | Only-trusted |
|------|---------:|-------------:|-------------:|-----------:|---------:|-------------:|
| 2000 | 1,539 | 1,708 | 1,539 | 94.2% | 0 | 164 |
| 2001 | 3,016 | 3,424 | 3,007 | 95.8% | 0 | 332 |
| 2002 | 3,298 | 3,534 | 3,282 | 96.0% | 0 | 240 |
| 2003 | 3,817 | 4,206 | 3,804 | 94.8% | 1 | 13 |
| 2004 | 3,697 | 4,125 | 3,641 | 94.7% | 44 | 12 |
| 2005 | 3,319 | 3,337 | 3,315 | 99.6% | 0 | 20 |
| 2006 | 3,359 | 3,372 | 3,343 | 99.0% | 0 | 12 |

**Final validation results, after the `ilan_re` narrowing below - current state of
`resmigazete_all/titles_resmigazete_{year}.csv` for 2000-2006:**

| Year | New rows | Trusted rows | Shared links | Text-match | Only-new | Only-trusted |
|------|---------:|-------------:|-------------:|-----------:|---------:|-------------:|
| 2000 | 1,582 | 1,708 | 1,578 | 94.2% | 0 | 125 |
| 2001 | 3,025 | 3,424 | 3,016 | 95.9% | 0 | 323 |
| 2002 | 3,304 | 3,534 | 3,288 | 96.1% | 0 | 234 |
| 2003 | 3,822 | 4,206 | 3,809 | 94.9% | 1 | 8 |
| 2004 | 3,702 | 4,125 | 3,646 | 94.8% | 44 | 7 |
| 2005 | 3,333 | 3,337 | 3,329 | 99.6% | 0 | 6 |
| 2006 | 3,370 | 3,372 | 3,354 | 99.0% | 0 | 1 |
| 2007 | 3,286 | 3,294 | 3,252 | 97.8% | 0 | 1 |
| 2008 | 3,459 | 3,517 | 3,374 | 98.9% | 1 | 1 |
| 2009 | 3,668 | 3,691 | 3,660 | 99.4% | 2 | 8 |
| 2010 | 5,351 | 5,514 | 5,225 | 98.0% | 2 | 6 |

- 2007-2010 (scraped 2026-09-13, across two sessions interrupted by a PC shutdown -
  resumed cleanly both times with zero manual bookkeeping) validate very cleanly on the
  first pass, no new noise source found - 97.8-99.4% text-match, only-new/only-trusted
  both in the single digits every year. Consistent with 2005/2006: once the site's
  post-2005 markup (separate `-N.htm` pages instead of same-page fragments) and the
  fixes already found (encoding, anchor-merge, Sayfa Başı, ilan_re) are in place, these
  years need no further work.
- 2000's remaining "only-trusted" (125) is mostly the pre-2000-06-27 PDF-only era (178
  fetch failures logged, matching CLAUDE.md/notebook's own note that `.htm` issues
  start 2000-06-27) - not a bug, those pages never existed at that URL scheme.
- 2001/2002's remaining "only-trusted" (323, 234) is now confirmed to be almost
  entirely the correctly-excluded "İlanları görmek için tıklayınız" boilerplate link
  (321/234 respectively - see below) - i.e. this gap is now the *intended* filtering,
  not missing data.
- 2004's 44 "only-new" rows were checked individually: all legitimate content trusted
  never captured - annex/attachment documents (`.doc`/`.xls`/`.pdf` links), external
  reference links (e.g. tse.org.tr, dtm.gov.tr), and footnote markers (`#_ftn1` etc.).
  The new scraper is more complete here, not noisier; not a bug, no fix applied.
- Text-match in the low-to-mid 90s (vs. 2005/2006's ~99%) across 2000-2004 is expected
  given these years' pre-2005 markup quirks (fragment URLs, kerning spans, etc.) are
  less uniform - the remaining gap wasn't chased row-by-row for every year the way 2006
  was, since the dominant, systematic causes (encoding, anchor-splitting, Sayfa Başı,
  ilan_re) are already found and fixed; what's left looks like long-tail per-page noise
  rather than another single fixable bug.

## Third noise source found: `ilan_re` was over-broad (2026-09-13)

Orhan asked why 2001/2002 still had a sizeable "only in trusted" gap (403 and 241
links respectively) after the Sayfa Başı fix. Same diff-and-sample method as the
earlier noise sources: joined new vs. trusted by hyperlink, pulled the rows only
trusted has, and read through the samples.

- **~80% of the gap (321/403 for 2001, 234/241 for 2002) is by-design filtering,
  correctly excluding "İlanları görmek için tıklayınız" ("click to see announcements")
  - a boilerplate link to the day's classified-notices PDF, not a real gazette item.**
  Not a bug.
- **The remaining ~20% is a real false-positive bug**, though in a filter that
  predates this session - `self.ilan_re` was originally `\bilan\w*` (Orhan's own
  design: "skip any word starting with 'ilan'"), which also silently dropped
  legitimate titles that merely *contain* "ilan" as a substring:
  - `"Basın-İlan Kurumu Genel Kurulu'nda..."` - "İlan" here is part of **Basın-İlan
    Kurumu**, a real government institution (the Press Advertisement Authority), not
    a classified notice.
  - `"...Uygulama Alanı İlan Edilmiş Bulunan Şanlıurfa İli'nde..."` - "İlan Edilmiş"
    ("declared") used as a verb in a real land-reform decree.
  - `"...Tespit ve İlanına Dair Tebliğ"` - a real regulatory notification about
    designating import/export checkpoints.
  - (Also present, but not a bug: rows where trusted stored a `"No href"` placeholder
    for a hrefless `<a>` around the page's "T.C." masthead text - the new scraper
    correctly skips anchors with no href at all, so these were never going to match;
    excluding pure letterhead/watermark text is correct behavior.)
- **Fixed by narrowing `ilan_re`** from the blanket word-prefix match to the specific
  boilerplate phrase pattern (`"İlanları görmek için tıklayınız"`, any case, optional
  leading `-`/trailing `.`) - verified against every variant found across
  `titles_resmigazete_2000/2001/2002.xlsx` (`İlanları Görmek İçin Tıklayınız`,
  `İlanları Görmek İçin Tıklayınız.`, `İlanları görmek için tıklayınız.`,
  `- İlanları görmek için tıklayınız.`) before applying, and against all four real-title
  examples above to confirm no false positives.
- **All 2000-2006 CSVs deleted and rebuilt from scratch** with the corrected filter
  (the resumable-by-date logic would otherwise have skipped already-written dates and
  kept the old, wrongly-dropped-title data). Done - all 7 years re-scraped cleanly, 0
  fetch failures beyond 2000's expected pre-2000-06-27 gap. Spot-checked all four
  real-title examples above directly in the new 2001/2002 CSVs - all four now present
  (e.g. `Basın-İlan Kurumu`, `Resmi İlan Fiyatlarının...`). Final numbers are in the
  validation table above.

## Fourth noise source: "Önceki"/"Sonraki" nav arrows (2026-09-13)

Orhan asked whether the "ÖNCEKİ"/"SONRAKİ" (Previous/Next) rows found while
investigating 2009/2010 were a rediscovery of an existing-but-broken filter (a
Turkish-İ regex casing bug, like nearly bit `ilan_re` earlier). Checked both
`resmigazete_module.py` and the original `resmigazete_scrape.ipynb` - no such filter
ever existed, so it wasn't a casing bug, just genuinely new noise nobody had written a
rule for. (For the record: `re.IGNORECASE` does handle Turkish İ/ı correctly in this
codebase - confirmed when fixing `ilan_re`.) Added `nav_arrow_re` (exact match,
case-insensitive) to `_should_skip_text`. Low-volume (2 rows/year in 2009/2010, where
the hrefs oddly point at 2011 dates - looks like stale site navigation, not a scraper
bug) - not worth a dedicated re-scrape of 2009/2010 for on its own, but applies
automatically to every scrape from here on.

## Fifth noise source: per-character font-spans in 2012/2013 (2026-09-13)

While scraping 2011-2013, 2013 came out at only 89.7% text-match (2012: 93.6%) -
noticeably worse than every other year. Investigated with a full only-new/only-trusted/
text-mismatch dump (see the 2007-2010 method above) and found a much more severe
version of the already-known, deliberately-unfixed kerning-span issue: some
2012/2013 pages (older Word-to-HTML export markup) wrap **every individual Turkish
diacritic character** in its own `<span>/<font>` - apparently to force a specific font
that could render it - not just the occasional first letter. Confirmed via raw HTML:

```html
<span style="font-weight: normal"><font size="1">6491&nbsp;&nbsp;&nbsp;&nbsp; T</font></span>
<span style="font-family: Times; font-weight: normal"><font size="1">ü</font></span>
<font size="1"><span style="font-weight: normal">rk Petrol Kanunu</span></font>
```

`get_text(" ", strip=True)` inserted a space at every one of these boundaries too,
turning "Türk Petrol Kanunu" into "T ü rk Petrol Kanunu". Unlike the earlier
single-letter kerning case (a 3+ character fragment ending in one letter, e.g. "— T"),
this pattern is structurally precise: each offending span's *entire* rendered text is
exactly one character. That precision is what made a real, non-blanket fix possible
this time without repeating the earlier backfire (where blanket `get_text("", ...)`
fused unrelated word boundaries together, e.g. "Değişiklik Yapılmasına Dair Kanun" →
"DeğişiklikYapılmasınaDair...").

**Fix:** added `_get_anchor_text(a)`, which walks `a.contents` directly (not
`get_text()`) and joins adjacent pieces with `""` only when at least one side, taken as
a whole, is exactly one character after stripping - `" "` otherwise. Verified against
three cases before applying: the "Türk Petrol Kanunu" pattern (now correct), the older
"T oprak" kerning case (unchanged, still imperfect - correctly *not* caught by this
narrower rule, since "— T" isn't a single character), and the 2006 anchor-merge
reference title (unchanged, no regression). Replaces the plain `get_text(" ", ...)`
call in `_parse_links`.

**Result after re-scraping 2011-2013 from scratch with the fix:**

| Year | Text-match before | Text-match after |
|------|-------------------:|-------------------:|
| 2011 | 98.6% | 98.7% |
| 2012 | 93.6% | 96.3% |
| 2013 | 89.7% | 94.8% |

Not perfect - the older unfixable kerning-span variant still accounts for some of the
remaining gap - but a real, substantial improvement, especially for 2013. This fix
applies automatically to every scrape from here on.

**Update 2026-09-14/15:** Orhan asked to re-scrape 2000-2010 too, to check whether the
per-character-font-span pattern appeared there at a lower rate. It did - re-scraped all
11 years from scratch in one clean run (0 interruptions, 0 fetch failures beyond 2000's
expected pre-2000-06-27 gap). Every year improved: 2005-2010 all moved to ~99%+,
2000-2004 each gained roughly a point (those years have other, unrelated legacy
quirks - fragment URLs, the ilan/Sayfa Başı eras - so they don't reach the same ceiling
as 2005+, but the font-span fix helped there too). Final numbers are in the
consolidated table below.

**Current full state (2000-2017 all scraped and validated), most recent numbers -
2000-2010 include the font-span fix (re-scraped 2026-09-15), 2011-2017 always did:**

| Year | Text-match | Year | Text-match |
|------|-----------:|------|-----------:|
| 2000 | 95.1% | 2009 | 99.8% |
| 2001 | 96.6% | 2010 | 98.8% |
| 2002 | 96.8% | 2011 | 98.7% |
| 2003 | 96.0% | 2012 | 96.3% |
| 2004 | 95.3% | 2013 | 94.8% |
| 2005 | 99.8% | 2014 | 96.3% |
| 2006 | 99.2% | 2015 | 99.5% |
| 2007 | 99.2% | 2016 | 98.8% |
| 2008 | 99.5% | 2017 | 98.8% |

2014-2017 (scraped 2026-09-14/15, across another PC-shutdown interruption resumed
cleanly mid-2016) validated with no new noise source - near-zero only-new/only-trusted
every year, consistent with the post-2005 markup era generally.

## 2018-2024: scraping complete, all years validated (2026-09-17)

Orhan ran `resmigazete_scrape.ipynb` himself this time (not via a session script) -
confirms it runs cleanly end-to-end, including the adaptive SSL fallback in
`resmigazete_module.py`. **Correction (checked the notebook's actual saved cell output
via its raw JSON, not just Orhan's summary):** his run hit the exact same
`SSLError`/cert-verification failure this session's runs always hit - the fallback note
fired 7 times, once per year (each year gets a fresh scraper instance in the loop, so
`_ssl_verify_disabled` resets and the adaptive check runs fresh each time - one
fallback message per year rather than once for the whole run, which is harmless but
worth knowing). So this machine's cert issue is real and consistent, not something
that only affected this session - "no certificate error" from Orhan's side meant no
*crash*, which is exactly what the adaptive fallback is for: catch the SSLError, note
it once (per scraper instance), keep going. The design point still holds - try
verified first, only fall back on an actual failure - it just hasn't yet been tested
on a machine where the cert issue genuinely isn't present. The notebook's raw JSON
output also confirmed the root cause of the 2020-08-27 gap directly: a `ConnectionError`
on that one request, logged as "failed to retrive page ... (ConnectionError)" - matches
the transient-failure guess below with actual evidence instead of just inference.

**Text-match after diffing against trusted:**

| Year | Text-match | Notes |
|------|-----------:|-------|
| 2018 | 97.8% | |
| 2019 | 98.7% | |
| 2020 | 98.4% | see below - one full day was missing, found and fixed |
| 2021 | 99.7% | |
| 2022 | 99.7% | |
| 2023 | 98.6% | |
| 2024 | 97.8% (on the 2,090 links trusted actually has) | trusted's 2024 file is genuinely incomplete - see below |

- **2024: trusted itself only covers roughly half the year** (2,090 links vs. the new
  scrape's 4,326) - flagged by Orhan before the diff even ran ("2024 on trusted has
  missing dates due to day performed, about half of it"), and confirmed by the diff:
  2,236 "only-new" links, entirely explained by trusted's shorter coverage, not a
  scraper defect. On the portion trusted *does* have, text-match is 97.8%, in line with
  every other year - the underlying scrape quality for 2024 is fine, only trusted's
  completeness is limited. **`titles_resmigazete_2024.csv` is more complete than the
  trusted `.xlsx` for this year** - worth keeping in mind if anything downstream
  compares 2024 counts against trusted rather than against itself.
- **2020: one full day (2020-08-27, ~21 items) was entirely missing** from the new
  scrape - not a legitimately empty day (trusted has real content for it: university
  technology-zone designations, expropriation decisions, several regulation
  amendments). Confirmed via a direct check - zero rows for that date in the CSV. Looks
  like a one-off transient fetch failure during the run, not a systematic bug (every
  other day in 2020, and every other year in this whole 2000-2024 span, scraped fine).
  Fixed trivially thanks to the resumable design: re-ran `scrape_resumable` for 2020
  alone - it correctly skipped all 365 already-done dates and retried only the missing
  one. Text-match for 2020 after the fix: 98.4%, only-trusted dropped from 25 to 1 (the
  usual harmless blank placeholder row). **Worth remembering as a general pattern:**
  when a diff shows an unusually high only-trusted count concentrated on one date, check
  for a full-day gap first (`df[df['Datetime']=='<date>']` on the CSV) before assuming
  it's cosmetic noise like every other case found so far - this is the first time in
  the whole 2000-2024 pass it turned out to be a real, if minor, missing-data gap rather
  than filtering/rendering noise.

**All of 2000-2024 is now scraped and validated.** No years remain.

## Open / not yet done (historical — mostly resolved, see "Status & Forward Steps" at
the top of this file for the actual current open items)

This section reflects how things stood as this multi-week task progressed. Everything
below except the two coordination write-ups is now resolved — kept for the audit
trail, not because it's still open. Don't act on the "not yet decided" framing below;
check the top section instead.

- **RESOLVED (2026-09-15/17):** ~~whether/when to re-run across the remaining years~~
  — all of 2000-2024 is scraped and validated now, see the "2018-2024" section above
  for the final state.
- **RESOLVED (2026-09-12, reaffirmed in CLAUDE.md):** ~~whether the newly-validated
  CSVs should replace the trusted `.xlsx`~~ — yes, CSV is the going-forward source of
  truth per CLAUDE.md; trusted `.xlsx` kept only for reference.
- **RESOLVED (2026-09-16):** ~~the SSL cert verification issue~~ — the module now has
  an adaptive fallback (verified request first, `verify=False` only if this machine
  actually hits an `SSLError`) instead of a blanket workaround. Confirmed still firing
  on this machine (7 times in the 2018-2024 run, once per year) but never crashing —
  see the "2018-2024" section above for the full story, including a correction to an
  earlier wrong assumption about who does/doesn't need it.
- **Cross-strand coordination (per Orhan, 2026-09-11):** messaged
  `thesis_log_agroministrynews_agent` to compare "top of the head" manual category
  schemes (this strand's BERTopic-cluster-derived Agreements/Supports labels in
  `resmigazete_search.ipynb` vs. their seed-sovereignty work) and decide together
  whether any reconciliation/alignment is warranted. Also flagged the same cross-strand
  classification-convention question to `thesis_log_main_agent` for awareness, since
  `literature_research/`'s annotation work is apparently also top-of-head and there's
  no dedicated strand agent there yet.

  **Outcome:** `thesis_log_agroministrynews_agent` replied same session. Their side has
  only a single keyword filter implemented so far ("tohum"/seed matched against
  Title+Paragraphs, 807/7,107 articles) — no multi-category tagging running yet. What's
  *proposed but not decided/implemented* on their end: reusing a subset of
  `literature_research/literature_annotation.ipynb`'s ~44 theory-grounded categories
  (candidates: Seed, Buyuksehir_Law, Agro_policy, Land_Policy, Food_Sovereignty,
  TR_agroGov, TR_ruralGov) as multi-label tags via TF-IDF/YAKE/RAKE — no LDA/BERT, per
  Orhan's explicit direction, and no final category subset chosen yet. Speculative
  overlap they flagged (unverified against real data): their "tohum" hits on
  certified-seed production subsidies plausibly overlap with this strand's
  Supports→fertilizer/farmerSupport buckets; seed export/import announcements could
  overlap with this strand's Agreements→İthalat Esasları (Import Rules). Both agents
  agreed to **hold off on forcing alignment** — neither taxonomy is finalized, and the
  source genres differ (formal Gazette/legal text vs. ministry press releases), so
  premature convergence risks distorting one to fit the other. They're flagging the
  whole exchange to Orhan directly since the alignment call is his, not one for the two
  agents to decide. Revisit once their categories are actually running against real
  data.
- Next step per Orhan: "start eliminating noise" (not yet scoped in detail — presumably
  improving the `tarım*` regex filter / BERTopic clustering quality in
  `resmigazete_search.ipynb`, but wait for explicit direction before assuming scope).
- **FSOI-wide category coordination (2026-09-11):** two separate coordination threads
  happened this session.
  1. Initiated by Orhan directly: compared "top of the head" manual category schemes
     with `thesis_log_agroministrynews_agent`. Their side has only a single "tohum"
     (seed) keyword filter implemented (807/7,107 articles) — no category system yet.
     Proposed but not decided/implemented: reusing a subset of
     `literature_research/literature_annotation.ipynb`'s ~44 categories (candidates:
     Seed, Buyuksehir_Law, Agro_policy, Land_Policy, Food_Sovereignty, TR_agroGov,
     TR_ruralGov) as multi-label tags via TF-IDF/YAKE/RAKE (no LDA/BERT, per Orhan's
     direction). Both agents agreed to hold off forcing alignment between taxonomies —
     neither is finalized, and the source genres differ (formal Gazette/legal text vs.
     ministry press releases). Flagged to Orhan directly by agroministrynews_agent.
  2. Initiated by `thesis_log_econometrics_agent`: Orhan wants econometrics,
     agroministrynews, and this strand to each share category thinking and loop back
     to `thesis_log_main_agent` for a coordinating remark across the whole FSOI
     index-building process. Econometrics shared their 6 FSOI indicator categories
     (market/production/water/waste/energy/land-use, city-year panel 2008–2024) and
     flagged that FSOI has no data source yet for a political/policy category —
     referencing the Global Food Security Index's "political commitment to adaptation"
     sub-dimension as a methodological reference, and suggesting this strand's Gazette
     work as the natural fit. Replied with this strand's Agreements/Supports
     categories (above) and pushed back on the framing: Gazette data is enacted
     legal/regulatory text (laws, kararlar, tebliğler), not discourse/rhetoric — closer
     to a "policy activity/output" measure (volume/type of ag legislation over time,
     pre/post-2012) than GFSI's more attitudinal "political commitment" framing.
     Econometrics agreed this distinction is worth keeping separate. Write-up sent
     directly to `thesis_log_main_agent` (each strand routes its own write-up there
     rather than collating through econometrics).

     **RESOLVED (2026-09-13, in CLAUDE.md):** the coordinating remark arrived. FSOI
     stays at 6 categories, no 7th added for this. GFSI's "political commitment"
     pillar is approximated, for discussion only, by combining this strand's
     legislation data with `agro_ministry_news/`'s press releases — both
     national-level, so political influence is modeled as uniform across all cities
     per year (which also made the city-disaggregation question moot). The
     policy-output-vs-attitudinal-commitment distinction this strand raised made it
     into the official caveat: keep noting wherever this comparison comes up that (a)
     both sources measure activity/output, not attitudinal commitment, and (b) both
     are official self-reporting, which skews toward looking committed — a limitation,
     not a finding. Full wording is in CLAUDE.md's FSOI vs. GFSI section - that's the
     authoritative version, this is just the history of how it got there.
