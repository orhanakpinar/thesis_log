"""Reproduces every annotation-layer number cited in agent_note_officialgazette_FSOI.md.

Written 2026-09-21 by thesis_log_officialgazette_agent [ca5df5].

Why this file exists: the validation diff script behind this strand's text-match numbers was
lost because it only ever lived in a session scratchpad (see "How to rebuild the validation
diff" in the agent note). The same was about to happen to the annotation diagnostics below.
CLAUDE.md also requires that any analytical claim displayed in a notebook be computed by the
cell that displays it, never pasted as a literal -- these functions are the intended source
for those cells.

Run:  python resmigazete_annotation_diagnostics.py
Reads only the two hand-annotated .xlsx files; writes nothing.
"""

import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
AGREEMENTS = "Final_AgroPolicy_Topic_Agreements_Annotated.xlsx"
SUPPORTS = "Final_AgroPolicy_Topic_Supports_Annotated.xlsx"

# The rollup's group lists, copied verbatim from resmigazete_search.ipynb.
# NOTE topic 20 appears in BOTH farmerSupport and negative. The notebook assigns groups with
# sequential .loc writes, so the LAST write wins and topic 20 lands in negative -- which is
# why farmerSupport comes out at 76 rather than 83. Order-dependent, hence fragile.
ROLLUP_LISTS = [
    ("generalLaw", [8, 23, 24, 25, 27, 28]),
    ("farmerSupport", [0, 2, 3, 9, 12, 13, 15, 18, 19, 20]),
    ("investment", [11, 17]),
    ("financial", [1, 14]),
    ("negative", [6, 20, 26]),
    ("logistics", [5, 7, 16]),
    ("damageLoss", [4, 10, 21]),
]

# Proposed sovereignty-relevant collapse of the 29 Supports topics (AI-proposed 2026-09-21,
# NOT adopted by Orhan -- do not treat as settled methodology).
SOVEREIGNTY_GROUPS = {
    "resourceControl": [3, 12, 13, 24, 27],
    "producerAutonomy": [0, 2, 5, 9, 15, 16, 17, 18, 19],
    "marketIntegration": [1, 7, 10, 11, 14, 21, 25, 28],
    "riskRetrenchment": [4, 6, 20, 26],
    "frameworkOther": [8, 22, 23],
}


def load():
    ag = pd.read_excel(os.path.join(HERE, AGREEMENTS))
    su = pd.read_excel(os.path.join(HERE, SUPPORTS))
    return ag, su


def rollup_effective(supports):
    """Group counts as the notebook actually computes them (last write wins)."""
    mapping = {}
    for name, ids in ROLLUP_LISTS:
        for t in ids:
            mapping[t] = name          # later lists overwrite earlier ones
    grp = supports["Annotation_Topic"].map(mapping)
    covered = set(mapping)
    orphans = sorted(set(supports["Annotation_Topic"].dropna()) - covered)
    return grp.value_counts(), orphans


def misfiled_rows(agreements, supports):
    """Topic 99 marks items sitting in the wrong file; both known cases are swapped."""
    out = []
    for label, df in (("Agreements", agreements), ("Supports", supports)):
        for _, r in df[df["Annotation_Topic"] == 99].iterrows():
            out.append((label, int(r["Year"]), str(r["Text"]).strip()))
    return out


def sparsity(supports, n_topics=29):
    """Why a 29-category annual series cannot carry a trend."""
    years = supports["Year"].nunique()
    filled = supports.groupby(["Year", "Annotation_Topic"]).size()
    return {
        "years": years,
        "items_per_year": len(supports) / years,
        "cells": n_topics * years,
        "filled": len(filled),
        "pct_filled": 100 * len(filled) / (n_topics * years),
        "median_per_filled_cell": filled.median(),
    }


def sovereignty_composition(supports, cut=2012):
    """Group totals and pre/post-cut shares. Shares, not counts: total volume roughly
    doubles across the cut, so raw counts would mostly restate that."""
    mapping = {t: g for g, ids in SOVEREIGNTY_GROUPS.items() for t in ids}
    df = supports.copy()
    df["grp"] = df["Annotation_Topic"].map(mapping)
    df["era"] = df["Year"].apply(lambda y: "pre%d" % cut if y < cut else "post%d" % cut)
    counts = pd.crosstab(df["grp"], df["era"])
    shares = (100 * counts / counts.sum()).round(1)
    unmapped = sorted(set(df.loc[df["grp"].isna(), "Annotation_Topic"].dropna()))
    return df["grp"].value_counts(dropna=False), counts, shares, unmapped


def per_year_density(supports, agreements):
    """Can this strand support a per-year CATEGORY series, or only raw counts?

    Unlike agro_ministry_news/, these 546 items are the full annotated population, not a
    sample -- so per-year category counts carry NO sampling error and are exact as
    description. The limit here is different: inferring a trend from counts this small is
    weak even when the counts are exact, because a year of 2 vs 4 items is not a
    distinguishable change in any underlying propensity.
    """
    mapping = {t: g for g, ids in SOVEREIGNTY_GROUPS.items() for t in ids}
    su = supports.copy()
    su["grp"] = su["Annotation_Topic"].map(mapping)
    cells = su.dropna(subset=["grp"]).groupby(["Year", "grp"]).size()
    years = sorted(su["Year"].unique())
    out = {
        "years": len(years),
        "supports_per_year_min": su.groupby("Year").size().min(),
        "supports_per_year_median": su.groupby("Year").size().median(),
        "supports_per_year_max": su.groupby("Year").size().max(),
        "agreements_per_year_median": agreements.groupby("Year").size().median(),
        "cell_min": cells.min(),
        "cell_median": cells.median(),
        "cell_max": cells.max(),
        "cells_possible": len(years) * len(SOVEREIGNTY_GROUPS),
        "cells_filled": len(cells),
        "cells_lt_3": int((cells < 3).sum()),
        "cells_lt_5": int((cells < 5).sum()),
    }
    return out, cells


def law6360_density(supports, agreements):
    """Density of Law-6360 / metropolitan-governance content in the annotated corpus.

    agro_ministry_news/ found a per-year Buyuksehir_Law series unviable (4 hits in 500
    rows). Checking the equivalent here. There is no Buyuksehir category in the codebook,
    so this is a keyword probe over the annotated titles instead.
    """
    pat = r"büyükşehir|buyuksehir|6360|mahalle|köy tüzel|belediye"
    rows = []
    for label, df in (("Agreements", agreements), ("Supports", supports)):
        hit = df[df["Text"].str.contains(pat, case=False, na=False, regex=True)]
        rows.append((label, len(hit), sorted(hit["Year"].astype(int).unique().tolist())))
    return pat, rows


def law6360_vs_agriculture_in_full_corpus():
    """Does the Gazette ever link Law 6360 / metropolitan governance to agriculture?

    Probes the FULL scraped corpus (all 25 CSVs, ~112k titles), not the annotated 546, so
    this is independent of any annotation or filtering choice. The answer is the intersection
    count: how many titles mention both metropolitan governance and agriculture.
    """
    import glob
    import re
    all_dir = os.path.join(HERE, "resmigazete_all")
    frames = []
    for f in sorted(glob.glob(os.path.join(all_dir, "titles_resmigazete_*.csv"))):
        df = pd.read_csv(f)
        df["Year"] = int(re.search(r"(\d{4})\.csv$", f).group(1))
        frames.append(df[["Year", "Text"]])
    corpus = pd.concat(frames, ignore_index=True)
    corpus["Text"] = corpus["Text"].astype(str)

    metro = corpus["Text"].str.contains(r"büyükşehir|6360", case=False, regex=True)
    agri = corpus["Text"].str.contains(r"\btarım\w*\b", case=False, regex=True)
    return {
        "corpus_rows": len(corpus),
        "metro_rows": int(metro.sum()),
        "agri_rows": int(agri.sum()),
        "intersection": int((metro & agri).sum()),
        "metro_by_year": corpus.loc[metro].groupby("Year").size(),
        "law_itself": corpus.loc[
            corpus["Text"].str.contains(r"^6360|^6447", regex=True), ["Year", "Text"]],
    }


def main():
    ag, su = load()
    print("Agreements n=%d  fine topics: %s" % (
        len(ag), sorted(ag["Annotation_Topic"].dropna().astype(int).tolist()[:0] or
                        set(ag["Annotation_Topic"].dropna().astype(int)))))
    print("Supports   n=%d  fine topics: %s" % (
        len(su), sorted(set(su["Annotation_Topic"].dropna().astype(int)))))

    print("\n--- rollup as the notebook computes it (last write wins) ---")
    counts, orphans = rollup_effective(su)
    print(counts.to_string())
    print("sum of groups: %d of %d rows" % (counts.sum(), len(su)))
    print("orphaned topics (in no group list):", orphans)

    print("\n--- topic 99: misfiled items (both swapped between files) ---")
    for where, year, text in misfiled_rows(ag, su):
        print("  [%s %d] %s" % (where, year, text[:110] + ("..." if len(text) > 110 else "")))

    print("\n--- sparsity of the 29-topic scheme ---")
    s = sparsity(su)
    print("  %d years, %.1f items/year" % (s["years"], s["items_per_year"]))
    print("  %d of %d year-topic cells filled (%.1f%%), median %.1f item(s) per filled cell"
          % (s["filled"], s["cells"], s["pct_filled"], s["median_per_filled_cell"]))

    print("\n--- proposed sovereignty collapse (NOT adopted -- for discussion) ---")
    totals, counts2, shares, unmapped = sovereignty_composition(su)
    print(totals.to_string())
    if unmapped:
        print("  WARNING unmapped topics:", unmapped)
    print("\n  counts by era:")
    print(counts2.to_string())
    print("\n  shares by era (%):")
    print(shares.to_string())
    print("\n  Caveat: resourceControl n is small; this is exploratory, not a finding.")

    print("\n--- per-year density: can a per-year CATEGORY series be supported? ---")
    dens, cells = per_year_density(su, ag)
    print("  years: %d | supports/year min %d, median %.1f, max %d | agreements/year median %.1f"
          % (dens["years"], dens["supports_per_year_min"], dens["supports_per_year_median"],
             dens["supports_per_year_max"], dens["agreements_per_year_median"]))
    print("  year x group cells: %d filled of %d possible"
          % (dens["cells_filled"], dens["cells_possible"]))
    print("  filled cell size: min %d, median %.1f, max %d"
          % (dens["cell_min"], dens["cell_median"], dens["cell_max"]))
    print("  filled cells with <3 items: %d | with <5 items: %d"
          % (dens["cells_lt_3"], dens["cells_lt_5"]))
    print("  NOTE these are population counts, not sample estimates -- exact as description,")
    print("       weak as inference about an underlying yearly propensity.")

    print("\n--- Law 6360 / metropolitan-governance density in the annotated corpus ---")
    pat, rows = law6360_density(su, ag)
    print("  pattern: %s" % pat)
    for label, n, years in rows:
        print("  %-11s %d hit(s)%s" % (label, n, (" in years %s" % years) if n else ""))

    print("\n--- full corpus: does the Gazette link Law 6360 to agriculture at all? ---")
    fc = law6360_vs_agriculture_in_full_corpus()
    print("  corpus titles: %d" % fc["corpus_rows"])
    print("  mention büyükşehir|6360: %d" % fc["metro_rows"])
    print("  mention tarım: %d" % fc["agri_rows"])
    print("  mention BOTH: %d  <-- the intersection" % fc["intersection"])
    print("  Law 6360 / 6447 themselves appear as:")
    for _, r in fc["law_itself"].iterrows():
        print("    [%d] %s" % (r["Year"], r["Text"][:100]))


if __name__ == "__main__":
    main()
