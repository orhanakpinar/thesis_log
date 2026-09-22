"""Measures what the single-keyword `tarım` base filter never surfaced.

Written 2026-09-22 by thesis_log_officialgazette_agent, at Orhan's go-ahead.

Background: the 546-article annotated corpus derives from `resmigazete_tarım_filter.xlsx`,
built with `pattern = r'(?=.*\\btarım\\w*\\b)'` over the master title list. So the base pool
only ever contained titles literally containing "tarım". This script quantifies the recall
gap over the FULL scraped corpus (all 25 year CSVs, ~112k titles), grouped by food-sovereignty
pillar so the gap can be read against the framework rather than as a bare keyword tally.

Key output is the UNIQUE column: titles a keyword matches that `tarım` does NOT, i.e. items
that were structurally invisible to every downstream stage.

Run:  python resmigazete_keyword_recall.py
Reads resmigazete_all/*.csv only; writes nothing.
"""

import glob
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ALL_DIR = os.path.join(HERE, "resmigazete_all")

BASE = r"\btarım\w*"

# Grouped by food-sovereignty pillar. Turkish suffixes are handled with \w* rather than
# exact forms, since these are agglutinative (sulama / sulamaya / sulamasına ...).
PILLARS = {
    "seeds & genetic resources": [
        r"\btohum\w*", r"\bfidan\w*", r"\bçeşit tescil\w*", r"\bgenetik kaynak\w*",
        r"\bıslah\w*",
    ],
    "land": [
        r"\bmera\w*", r"\barazi\w*", r"\btarla\w*", r"\btoprak koruma\w*",
        r"\bkadastro\w*", r"\bkırsal\w*",
    ],
    "water & irrigation": [
        r"\bsulama\w*", r"\bsu ürün\w*", r"\bgölet\w*", r"\bDSİ\b",
    ],
    "livestock & fisheries": [
        r"\bhayvancılık\w*", r"\bhayvan sağlığ\w*", r"\bbesicilik\w*", r"\bsüt\w*",
        r"\bbalıkçılık\w*", r"\bveteriner\w*",
    ],
    "food & nutrition": [
        r"\bgıda\w*", r"\bbeslenme\w*", r"\bhal\w* kanunu", r"\bgıda güvenliğ\w*",
    ],
    "producers & cooperatives": [
        r"\bçiftçi\w*", r"\büretici birliğ\w*", r"\bkooperatif\w*", r"\bköylü\w*",
        r"\bziraat odas\w*",
    ],
    "off-farm inputs": [
        r"\bgübre\w*", r"\bmazot\w*", r"\bzirai ilaç\w*", r"\bpestisit\w*", r"\byem\w*",
        r"\bbitki koruma\w*",
    ],
    "forestry": [
        r"\borman\w*",
    ],
    "other agricultural terms": [
        r"\bzirai\w*", r"\bziraat\w*", r"\bhasat\w*", r"\bekim\w*", r"\bbuğday\w*",
        r"\bfındık\w*", r"\bçay\w*", r"\bşeker pancar\w*", r"\bpamuk\w*", r"\bzeytin\w*",
    ],
}


def load_corpus():
    frames = []
    for f in sorted(glob.glob(os.path.join(ALL_DIR, "titles_resmigazete_*.csv"))):
        df = pd.read_csv(f)
        df["Year"] = int(re.search(r"(\d{4})\.csv$", f).group(1))
        frames.append(df[["Year", "Text"]])
    corpus = pd.concat(frames, ignore_index=True)
    corpus["Text"] = corpus["Text"].astype(str)
    return corpus


def measure(corpus):
    base_hit = corpus["Text"].str.contains(BASE, case=False, regex=True)
    rows = []
    for pillar, pats in PILLARS.items():
        for pat in pats:
            hit = corpus["Text"].str.contains(pat, case=False, regex=True)
            rows.append({
                "pillar": pillar,
                "keyword": pat.replace(r"\b", "").replace(r"\w*", "*"),
                "hits": int(hit.sum()),
                "also_tarim": int((hit & base_hit).sum()),
                "unique": int((hit & ~base_hit).sum()),
            })
    out = pd.DataFrame(rows)
    out["pct_missed"] = [
        ("%.0f%%" % (100.0 * u / h)) if h else "-"
        for u, h in zip(out["unique"], out["hits"])
    ]
    return out, base_hit


def pillar_union(corpus, base_hit):
    """Per-pillar union: unique titles the pillar adds beyond tarım (dedup within pillar)."""
    rows = []
    for pillar, pats in PILLARS.items():
        any_hit = pd.Series(False, index=corpus.index)
        for pat in pats:
            any_hit |= corpus["Text"].str.contains(pat, case=False, regex=True)
        rows.append({
            "pillar": pillar,
            "titles": int(any_hit.sum()),
            "new_beyond_tarim": int((any_hit & ~base_hit).sum()),
        })
    return pd.DataFrame(rows).sort_values("new_beyond_tarim", ascending=False)


def main():
    corpus = load_corpus()
    print("corpus: %d titles, %d years (%d-%d)" % (
        len(corpus), corpus["Year"].nunique(), corpus["Year"].min(), corpus["Year"].max()))

    per_kw, base_hit = measure(corpus)
    print("\nbaseline `tarım` matches: %d titles (%.1f%% of corpus)"
          % (base_hit.sum(), 100 * base_hit.sum() / len(corpus)))

    print("\n=== per keyword (unique = matched but NOT caught by tarım) ===")
    for pillar in PILLARS:
        sub = per_kw[per_kw["pillar"] == pillar].sort_values("unique", ascending=False)
        print("\n-- %s" % pillar)
        print(sub[["keyword", "hits", "also_tarim", "unique", "pct_missed"]]
              .to_string(index=False))

    print("\n=== per pillar: titles added beyond the tarım pool ===")
    print(pillar_union(corpus, base_hit).to_string(index=False))

    # What a widened filter would look like in total.
    everything = pd.Series(False, index=corpus.index)
    for pats in PILLARS.values():
        for pat in pats:
            everything |= corpus["Text"].str.contains(pat, case=False, regex=True)
    widened = everything | base_hit
    print("\n=== corpus-level effect of widening ===")
    print("  tarım only            : %d" % base_hit.sum())
    print("  widened (all pillars) : %d" % widened.sum())
    print("  multiplier            : %.1fx" % (widened.sum() / base_hit.sum()))
    print("\n  NOTE a widened pool needs a precision pass before annotation -- several of"
          "\n  these keywords are deliberately broad (orman, yem, çay, süt, ekim) and will"
          "\n  pull non-agricultural matches. Read the unique samples before adopting any.")


if __name__ == "__main__":
    main()
