# Agent note: agro_ministry_news scope and pipeline (AI-authored working note)

This file is AI-authored pipeline documentation for future sessions working on this strand.
Anything about result validity should live in the root `CLAUDE.md`, not here.

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

**NER / entity extraction: discarded (Orhan, 2026-09-11).** An earlier version of this note
proposed running NER over `Paragraphs` (location entities as a possible bridge to
`econometric_models_and_vars/`'s city-level panel, person entities as an administration/
minister-tenure marker, org entities for institutional actors). Orhan decided against it —
concern that it adds noisy, wordy output at the wrong grain; this strand should stay at the
subject/document level (what an article is about) rather than trying to pull out individual
entities within it. Not to be re-proposed without Orhan raising it again.

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
