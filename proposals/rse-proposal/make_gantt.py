#!/usr/bin/env python3
"""Render the proposed GANTT chart for the AY27 SPECFEM++ RSE renewal.
Run with: uv run --with matplotlib draft/make_gantt.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proposed_gantt.png")

# --- palette -------------------------------------------------------------
C_R1 = "#2C6FBB"   # RSE-1 (frequency solver)
C_R2 = "#E07B1A"   # RSE-2 (3D / performance)
C_SH = "#2E8B57"   # shared
C_ST = "#9AA0A6"   # stretch
C_MS = "#C0392B"   # milestones
C_HDR = "#222222"

# --- rows (top -> bottom) ------------------------------------------------
# (kind, label, segments[list of (start,end)], color, is_band)
rows = [
    ("header", "D1 · Frequency-domain solver  (RSE-1)", None, C_R1, False),
    ("bar", "Frequency-domain formulation & core solver", [(0, 8)], C_R1, False),
    ("bar", "Verification vs. analytic & normal-mode benchmarks", [(6, 13)], C_R1, False),
    ("bar", "Adjoint / inversion coupling + production hardening", [(12, 18)], C_R1, False),
    ("bar", "Release + documentation of new capability", [(18, 24)], C_R1, False),
    ("header", "D2 · Global-scale physics & maintenance  (RSE-2)", None, C_R2, False),
    ("bar", "DG for globe (extend Cartesian DG to global scale)", [(2, 13)], C_R2, False),
    ("bar", "3D/global maintenance: fixes, Kokkos & new-arch perf upkeep", [(0, 24)], C_R2, True),
    ("bar", "Regression-benchmark & CI upkeep", [(0, 24)], C_R2, True),
    ("header", "D3 · New physics with scientists & adoption  (shared)", None, C_SH, False),
    ("bar", "RSE partnership: land new physics w/ scientists (Cosserat, couplings)", [(2, 22)], C_SH, False),
    ("bar", "Advanced tutorials / workshops / contributor onboarding", [(9, 11), (20, 22)], C_SH, False),
    ("bar", "Release engineering (v0.7 → v1.0)", [(0, 24)], C_SH, True),
    ("bar", "Transition to community maintenance (governance, contributor docs)", [(14, 24)], C_SH, False),
    ("header", "Stretch · candidate new physics (opportunistic, Year 2)", None, C_ST, False),
    ("dash", "MOR · wavefield compression · new couplings · auto mesh-layer", [(15, 24)], C_ST, False),
]

milestones = [
    (0,  "M0", "Award start — baseline: GLOBE parity + near-native perf + DG-Cartesian (AY26–27)"),
    (8,  "M1", "Frequency-domain core solver complete → v0.8"),
    (13, "M2", "DG-for-globe delivered & freq solver verified → v0.9"),
    (18, "M3", "Frequency solver in production (adjoint/inversion)"),
    (24, "M4", "v1.0 release + community-maintenance handoff"),
]

# --- figure --------------------------------------------------------------
n = len(rows)
fig, ax = plt.subplots(figsize=(13, 7.0))
BAR_H = 0.62

# Year background bands
ax.axvspan(0, 12, color="#f4f6f8", zorder=0)
ax.axvspan(12, 24, color="#eef1f4", zorder=0)

# quarter gridlines
for q in range(0, 25, 3):
    ax.axvline(q, color="#d0d5da", lw=0.8, zorder=1)
ax.axvline(12, color="#9aa0a6", lw=1.4, zorder=1)  # year boundary

# milestone vertical lines
for m, _, _ in milestones:
    ax.axvline(m, color=C_MS, lw=1.0, ls=(0, (4, 3)), alpha=0.5, zorder=1)

# rows
for i, (kind, label, segs, color, band) in enumerate(rows):
    y = i
    if kind == "header":
        ax.axhspan(y - 0.5, y + 0.5, color=color, alpha=0.10, zorder=1)
        ax.text(-0.015, y, label, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=9.5, fontweight="bold", color=C_HDR)
        continue
    # task label
    ax.text(-0.015, y, label, transform=ax.get_yaxis_transform(),
            ha="right", va="center", fontsize=8.2, color="#333333")
    if kind == "dash":
        for (s, e) in segs:
            ax.add_patch(Rectangle((s, y - BAR_H / 2), e - s, BAR_H,
                                   facecolor=color, alpha=0.20, edgecolor=color,
                                   lw=1.2, ls="--", hatch="//", zorder=3))
    else:
        alpha = 0.42 if band else 0.92
        ax.broken_barh([(s, e - s) for (s, e) in segs], (y - BAR_H / 2, BAR_H),
                       facecolors=color, alpha=alpha, edgecolor="white", lw=0.6, zorder=3)

# milestones lane (above everything)
my = -1.35
for m, tag, _ in milestones:
    ax.plot(m, my, marker="D", ms=11, color=C_MS, zorder=5, clip_on=False)
    ax.text(m, my - 0.72, tag, ha="center", va="center", fontsize=8.5,
            fontweight="bold", color=C_MS, clip_on=False)

# year titles
ax.text(6, -3.25, "Year 1  ·  2027–28", ha="center", va="center",
        fontsize=11, fontweight="bold", color="#444")
ax.text(18, -3.25, "Year 2  ·  2028–29", ha="center", va="center",
        fontsize=11, fontweight="bold", color="#444")

# axes cosmetics
ax.set_xlim(0, 24)
ax.set_ylim(n - 0.5, -3.7)   # inverted: row 0 on top, milestone lane above
xticks = list(range(0, 25, 3))
xlabels = ["Jul'27", "Oct'27", "Jan'28", "Apr'28", "Jul'28", "Oct'28", "Jan'29", "Apr'29", "Jun'29"]
ax.set_xticks(xticks)
ax.set_xticklabels(xlabels, fontsize=8.5)
ax.set_yticks([])
for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis="x", length=0)
ax.xaxis.tick_bottom()

# legend
legend_elems = [
    Patch(facecolor=C_R1, label="RSE-1 (frequency solver)"),
    Patch(facecolor=C_R2, label="RSE-2 (3D / performance)"),
    Patch(facecolor=C_SH, label="Shared"),
    Patch(facecolor=C_ST, alpha=0.35, hatch="//", edgecolor=C_ST, label="Stretch"),
    Line2D([0], [0], marker="D", color="w", markerfacecolor=C_MS, markersize=10, label="Milestone"),
]
ax.legend(handles=legend_elems, loc="lower center", bbox_to_anchor=(0.5, -0.16),
          ncol=5, frameon=False, fontsize=9, handletextpad=0.5, columnspacing=1.4)

ax.set_title("SPECFEM++ — Proposed RSE work plan (AY27 renewal, 2 RSEs × 2 years)",
             fontsize=12.5, fontweight="bold", pad=14)

plt.subplots_adjust(left=0.37, right=0.985, top=0.90, bottom=0.14)
fig.savefig(OUT, dpi=170)
print("wrote", OUT)
