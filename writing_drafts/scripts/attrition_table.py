"""Indicator attrition: literature-derived candidates -> matched to a source file -> filtered list.

Also writes a draft appendix table with a rule-based elimination reason per indicator,
derived from the Source / Level columns in the original variable list. The `reason_orhan`
column is left empty for manual correction.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
VARS = ROOT / "econometric_models_and_vars" / "FSOI_Variables_List"
OUT = ROOT / "writing_drafts" / "tables" / "indicator_attrition_draft.xlsx"

orig = pd.read_excel(VARS / "FSOI_Variables_List.xlsx")
clean = pd.read_excel(VARS / "FSOI_Variables_List_Clean.xlsx")
filtered = pd.read_excel(VARS / "FSOI_Variables_List_Clean_Filtered.xlsx")
assert len(orig) == len(clean), "original and clean lists no longer align row by row"

df = clean.assign(
    orig_source=orig["Source"],
    orig_level=orig["Level"],
    orig_problem=orig["Problem"],
)
df = df[df["Variable"].notna()].copy()
kept_keys = set(zip(filtered["Variable"], filtered["Annotation"]))
df["kept"] = [k in kept_keys for k in zip(df["Variable"], df["Annotation"])]
assert df["kept"].sum() == len(filtered), f"matched {df['kept'].sum()} of {len(filtered)} kept rows"

NO_SOURCE = {"?", "-"}
PROVINCE_OR_FINER = {"NUTS3", "NUTS4", "NUTS5"}


def draft_reason(row) -> str:
    if row["kept"]:
        return "kept in 24-indicator list"
    src = row["orig_source"]
    if isinstance(src, str) and src.strip().lower().startswith("survey"):
        return "needs household/farm survey data; no official series"
    if (pd.isna(src) or str(src).strip() in NO_SOURCE) and pd.isna(row["Source_doc"]):
        return "no official source identified"
    level = row["Level"] if pd.notna(row["Level"]) else row["orig_level"]
    if isinstance(level, str) and level.startswith("NUTS") and level not in PROVINCE_OR_FINER:
        return f"source found, only at {level} (not province)"
    return "source found; dropped at data check (years/coverage) - confirm"


df["reason_draft"] = df.apply(draft_reason, axis=1)
df["reason_orhan"] = ""

table = (
    df.groupby("Class")
    .agg(candidates=("Variable", "size"),
         with_matched_source=("Source_doc", lambda s: s.notna().sum()),
         kept=("kept", "sum"))
    .astype(int)
    .sort_values("candidates", ascending=False)
)
table.loc["TOTAL"] = table.sum()

# Provisional grouping of the 27 literature categories into three blocs (Orhan to confirm).
BLOCS = {
    "production and land": ["Land Use", "Crop Type", "Market", "Costs", "Water", "Ecology",
                            "Spatial", "Husbandry"],
    "sovereignty core": ["Land Security", "Autonomy", "Seed Sovereignty", "Cooperative",
                         "Food Sovereignty", "Scale", "Farmer Dynamics", "Agroecology"],
    "social and governance": ["Household", "Demography", "Rural Development", "Tech Capital",
                              "Governance", "Finance", "Regional", "Network", "Income",
                              "Ethnicity", "Gender", "Extras"],
}
bloc_of = {cls: bloc for bloc, classes in BLOCS.items() for cls in classes}
assert set(bloc_of) == set(df["Class"].dropna()), "every category must sit in exactly one bloc"
df["bloc"] = df["Class"].map(bloc_of)
bloc_table = pd.crosstab(df["bloc"], df["reason_draft"], margins=True, margins_name="TOTAL")

if __name__ == "__main__":
    print(table.to_string())
    print()
    print(bloc_table.to_string())
    print()
    print(df["reason_draft"].value_counts().to_string())
    OUT.parent.mkdir(exist_ok=True)
    cols = ["Class", "Variable", "Annotation", "orig_source", "Source_doc", "Level",
            "orig_level", "orig_problem", "reason_draft", "reason_orhan"]
    if OUT.exists():
        print(f"\n{OUT.name} exists and may hold Orhan's corrections; not overwritten.")
        raise SystemExit(0)
    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        df[cols].to_excel(xw, sheet_name="indicators", index=False)
        table.to_excel(xw, sheet_name="summary_by_class")
        ws = xw.sheets["indicators"]
        ws.freeze_panes = "C2"
        ws.auto_filter.ref = ws.dimensions
        for letter, width in zip("ABCDEFGHIJ", [16, 34, 40, 14, 18, 8, 8, 30, 48, 40]):
            ws.column_dimensions[letter].width = width
    print(f"\nwrote {OUT.relative_to(ROOT)} ({len(df)} rows)")
