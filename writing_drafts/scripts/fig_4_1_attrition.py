"""Figure 4.1: candidate indicators by bloc at three stages (candidates, matched to a source, kept)."""
from pathlib import Path
import matplotlib.pyplot as plt

from attrition_table import df, ROOT

OUT = ROOT / "writing_drafts" / "figures" / "fig_4_1_attrition.png"
BLOC_ORDER = ["production and land", "social and governance", "sovereignty core"]
LABELS = {"production and land": "Production and land",
          "social and governance": "Social and governance",
          "sovereignty core": "Core of sovereignty"}
STAGES = [("Candidates", "#86b6ef"), ("Matched to a source", "#2a78d6"), ("Kept (24)", "#104281")]
INK, INK2, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"

d = df.dropna(subset=["bloc"])
counts = {
    b: [int((d["bloc"] == b).sum()),
        int(((d["bloc"] == b) & d["Source_doc"].notna()).sum()),
        int(((d["bloc"] == b) & d["kept"]).sum())]
    for b in BLOC_ORDER
}
assert sum(c[0] for c in counts.values()) == 184
assert sum(c[1] for c in counts.values()) == 88
assert sum(c[2] for c in counts.values()) == 24

fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=300)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
bar_h, gap = 0.24, 0.03
for i, bloc in enumerate(BLOC_ORDER):
    for j, (stage, color) in enumerate(STAGES):
        y = i + (j - 1) * (bar_h + gap)
        v = counts[bloc][j]
        ax.barh(y, v, height=bar_h, color=color, label=stage if i == 0 else None)
        ax.text(v + 1, y, str(v), va="center", ha="left", fontsize=8, color=INK)

ax.set_yticks(range(len(BLOC_ORDER)))
ax.set_yticklabels([LABELS[b] for b in BLOC_ORDER], fontsize=9, color=INK)
ax.invert_yaxis()
ax.set_xlabel("Number of indicators", fontsize=9, color=INK2)
ax.set_xlim(0, 82)
ax.tick_params(axis="x", labelsize=8, colors=INK2)
ax.tick_params(axis="y", length=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#d6d5d0")
ax.xaxis.grid(True, color="#ebeae6", linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor=INK)
fig.tight_layout()

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, facecolor=SURFACE)
    print({b: c for b, c in counts.items()})
    print(f"wrote {OUT.relative_to(ROOT)}")
