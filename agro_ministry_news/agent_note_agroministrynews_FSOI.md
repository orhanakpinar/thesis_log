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
- Full scrape launched 2026-09-11 covering Number 153–7260 (7260 confirmed by Orhan as the
  current latest article; the bare `/Haber/{number}` URL, no slug, verified to resolve
  correctly for it) into `agroforestministry_news.csv`. Check progress via that CSV's row
  count / last `Number`, or ask the running session.
- Orhan is deleting `agroforest_ministry_news_seed.xlsx` and `agroforest_ministry_news.xlsx`
  (2026-09-11) now that the full-text CSV supersedes the title/date-only scrape and its
  keyword-filtered subset — once full text is available, both should be regenerated from
  `agroforestministry_news.csv` rather than treated as the current source.

## Scope of the "seed sovereignty" proxy (open question, updated 2026-09-11)

- The (now superseded) `agroforest_ministry_news_seed.xlsx` (77 rows) was produced by a
  **simple keyword search** — filtering titles containing "tohum" (seed) — not any text
  analysis. Orhan confirmed (2026-09-11) this was just a first-pass keyword proxy, not a
  finalized methodology.
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

## Coordination behavior: don't assume CLAUDE.md is unaffected

- When you rename/move/delete a file in this folder, check CLAUDE.md's **current** text
  (re-read it, don't rely on what you last saw or expect) for a reference to that filename
  before telling the main agent "no CLAUDE.md change needed." Twice (2026-09-11) that
  claim turned out to be wrong — CLAUDE.md had a pointer that needed updating both times,
  and the main agent had to catch and fix it after the fact. Only the main agent actually
  edits CLAUDE.md, but a strand agent giving it a wrong "nothing to update" signal defeats
  the point of flagging changes at all.
