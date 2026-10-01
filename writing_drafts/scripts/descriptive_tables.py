"""Descriptive tables for Chapter 5, computed from the FSOI exports of the econometrics notebook.

Reads econometric_models_and_vars/fsoi_track_{C,A}_perHousehold.csv (full index = C,
long-panel index = A). Descriptive only: no inference.
"""
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
ECON = ROOT / "econometric_models_and_vars"
GROUPS = ["Non-metropolitan", "Old-metropolitan", "New-metropolitan (2012)"]
CATS_FULL = ["production", "land_use", "market", "external_input", "municipal_burden"]

full = pd.read_csv(ECON / "fsoi_track_C_perHousehold.csv")
long = pd.read_csv(ECON / "fsoi_track_A_perHousehold.csv")
prov_full = full[full["Treated_Label"].isin(GROUPS)]
prov_long = long[long["Treated_Label"].isin(GROUPS)]

assert prov_full["Location_Name"].nunique() == 81
assert (prov_full.groupby("Treated_Label")["Location_Name"].nunique().to_dict()
        == {"Non-metropolitan": 51, "Old-metropolitan": 16, "New-metropolitan (2012)": 14})


def group_means(df, value="FSOI"):
    t = df.pivot_table(index="Year", columns="Treated_Label", values=value, aggfunc="mean")[GROUPS]
    return t


# Table 5.1: full index, group means by year, plus the national aggregate row
t51 = group_means(prov_full)
t51["Türkiye (aggregate)"] = full[full["Treated_Label"] == "Türkiye"].set_index("Year")["FSOI"]
assert abs(t51.loc[2020, "Non-metropolitan"] - 0.511) < 0.0005
assert abs(t51.loc[2020, "Old-metropolitan"] - 0.446) < 0.0005
assert abs(t51.loc[2020, "New-metropolitan (2012)"] - 0.439) < 0.0005

# Table 5.2: full index, 2020, category sub-index means by group
t52 = prov_full[prov_full["Year"] == 2020].groupby("Treated_Label")[CATS_FULL + ["FSOI"]].mean().loc[GROUPS]
assert abs(t52.loc["Non-metropolitan", "municipal_burden"] - 0.744) < 0.0005

# Spread across provinces by year (full index)
spread = prov_full.groupby("Year")["FSOI"].agg(["mean", "std", "min", "max"])

# Top and bottom 10 provinces, full index 2020
y20 = prov_full[prov_full["Year"] == 2020].sort_values("FSOI", ascending=False)
top10 = y20.head(10)[["Location_Name", "Treated_Label", "FSOI"]]
bottom10 = y20.tail(10)[["Location_Name", "Treated_Label", "FSOI"]]
top_counts = top10["Treated_Label"].value_counts()
bottom_counts = bottom10["Treated_Label"].value_counts()

# Rank stability 2008 -> 2020, full index
w = prov_full.pivot(index="Location_Name", columns="Year", values="FSOI")
rho_08_20 = spearmanr(w[2008], w[2020]).statistic
rose = (w[2020] > w[2008]).mean()

# Long-panel index, group means 2008 vs 2024 and change
t53 = group_means(prov_long).loc[[2008, 2012, 2024]]
t53.loc["change 2008-2024"] = t53.loc[2024] - t53.loc[2008]
tk_long = long[long["Treated_Label"] == "Türkiye"].set_index("Year")["FSOI"]

# Pooled 2008-2020 full-index group means (the 'tied-lowest' view)
pooled_full = prov_full.groupby("Treated_Label")["FSOI"].mean().loc[GROUPS]

# Table 5.3: full index, category means across provinces by year, and each category's
# contribution to the 2008-2020 change in the mean FSOI (category change / number of categories)
cat_trend = prov_full.groupby("Year")[CATS_FULL + ["FSOI"]].mean()
contrib = (cat_trend.loc[2020, CATS_FULL] - cat_trend.loc[2008, CATS_FULL]) / len(CATS_FULL)
assert abs(contrib.sum() - (cat_trend.loc[2020, "FSOI"] - cat_trend.loc[2008, "FSOI"])) < 1e-9

# Category profiles of the bottom 10 and the national median, full index 2020
bottom_profile = y20.tail(10).set_index("Location_Name")[CATS_FULL + ["FSOI"]]
median_2020 = y20[CATS_FULL + ["FSOI"]].median()

if __name__ == "__main__":
    pd.set_option("display.width", 200)
    fmt = lambda x: f"{x:.3f}"
    print("Table 5.1  full index, group means by year\n", t51.to_string(float_format=fmt), "\n")
    print("Table 5.2  full index 2020, category means by group\n", t52.to_string(float_format=fmt), "\n")
    print("Spread across provinces, full index\n", spread.to_string(float_format=fmt), "\n")
    print("Top 10, 2020\n", top10.to_string(index=False, float_format=fmt))
    print("group counts:", top_counts.to_dict(), "\n")
    print("Bottom 10, 2020\n", bottom10.to_string(index=False, float_format=fmt))
    print("group counts:", bottom_counts.to_dict(), "\n")
    print(f"Spearman rank 2008 vs 2020 (full index): {rho_08_20:.3f}")
    print(f"Share of provinces with higher FSOI in 2020 than 2008: {rose:.3f}\n")
    print("Long-panel index, group means\n", t53.to_string(float_format=fmt))
    print("Türkiye aggregate, long-panel:", tk_long.round(3).to_dict(), "\n")
    print("Pooled 2008-2020 full index group means:", pooled_full.round(3).to_dict(), "\n")
    print("Table 5.3  full index, category means by year\n", cat_trend.to_string(float_format=fmt))
    print("Contribution to FSOI change 2008-2020:\n", contrib.round(4).to_string(),
          "\n total", round(contrib.sum(), 4), "\n")
    print("Bottom 10 profiles, 2020\n", bottom_profile.to_string(float_format=fmt))
    print("Median 2020\n", median_2020.to_string(float_format=fmt))
