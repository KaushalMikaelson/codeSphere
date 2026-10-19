"""Compares baseline vs final graph metrics to quantify internal link experiment deltas."""

import logging
from pathlib import Path
from typing import Dict
import pandas as pd

logger = logging.getLogger(__name__)


def compare_runs(baseline_metrics_path: str, final_metrics_path: str, output_csv: str) -> pd.DataFrame:
    """Compare baseline and final metrics DataFrames and generate comprehensive delta report."""
    base_df = pd.read_csv(baseline_metrics_path)
    final_df = pd.read_csv(final_metrics_path)

    # 1. Summary Key Metrics Calculation
    base_reachable = base_df[base_df["click_depth"] >= 0]
    final_reachable = final_df[final_df["click_depth"] >= 0]

    base_avg_depth = round(base_reachable["click_depth"].mean(), 2) if not base_reachable.empty else 0.0
    final_avg_depth = round(final_reachable["click_depth"].mean(), 2) if not final_reachable.empty else 0.0

    base_max_depth = int(base_reachable["click_depth"].max()) if not base_reachable.empty else 0
    final_max_depth = int(final_reachable["click_depth"].max()) if not final_reachable.empty else 0

    base_orphans = int(base_df["is_orphan"].sum())
    final_orphans = int(final_df["is_orphan"].sum())

    base_dead_ends = int(base_df["is_dead_end"].sum())
    final_dead_ends = int(final_df["is_dead_end"].sum())

    base_weak_in_degree = int(((base_df["in_degree"] <= 1) & (base_df["click_depth"] > 0)).sum())
    final_weak_in_degree = int(((final_df["in_degree"] <= 1) & (final_df["click_depth"] > 0)).sum())

    base_avg_in_degree = round(base_df["in_degree"].mean(), 2)
    final_avg_in_degree = round(final_df["in_degree"].mean(), 2)

    metrics_comparison = [
        {
            "metric": "Total Nodes (Pages)",
            "baseline": len(base_df),
            "final": len(final_df),
            "absolute_change": len(final_df) - len(base_df),
            "percentage_change": f"{((len(final_df) - len(base_df)) / max(1, len(base_df))) * 100:.1f}%",
            "interpretation": "Total inventory scope under analysis.",
        },
        {
            "metric": "Reachable Pages from Home",
            "baseline": len(base_reachable),
            "final": len(final_reachable),
            "absolute_change": len(final_reachable) - len(base_reachable),
            "percentage_change": f"{((len(final_reachable) - len(base_reachable)) / max(1, len(base_reachable))) * 100:.1f}%",
            "interpretation": "Pages discoverable via crawler graph traversal.",
        },
        {
            "metric": "Orphan Pages Count",
            "baseline": base_orphans,
            "final": final_orphans,
            "absolute_change": final_orphans - base_orphans,
            "percentage_change": f"{((final_orphans - base_orphans) / max(1, base_orphans)) * 100:.1f}%" if base_orphans > 0 else "0%",
            "interpretation": "Pages with zero inbound links or unreachable from root (Lower is better).",
        },
        {
            "metric": "Average Click Depth",
            "baseline": base_avg_depth,
            "final": final_avg_depth,
            "absolute_change": round(final_avg_depth - base_avg_depth, 2),
            "percentage_change": f"{((final_avg_depth - base_avg_depth) / max(0.01, base_avg_depth)) * 100:.1f}%",
            "interpretation": "Mean clicks required from homepage to reach an article (Lower is better).",
        },
        {
            "metric": "Maximum Click Depth",
            "baseline": base_max_depth,
            "final": final_max_depth,
            "absolute_change": final_max_depth - base_max_depth,
            "percentage_change": f"{((final_max_depth - base_max_depth) / max(1, base_max_depth)) * 100:.1f}%",
            "interpretation": "Deepest crawl tier across all published content (Lower is better).",
        },
        {
            "metric": "Dead-End Pages (Out-degree = 0)",
            "baseline": base_dead_ends,
            "final": final_dead_ends,
            "absolute_change": final_dead_ends - base_dead_ends,
            "percentage_change": f"{((final_dead_ends - base_dead_ends) / max(1, base_dead_ends)) * 100:.1f}%" if base_dead_ends > 0 else "0%",
            "interpretation": "Pages that trap crawl equity without outbound paths (Lower is better).",
        },
        {
            "metric": "Weakly Linked Pages (In-degree <= 1)",
            "baseline": base_weak_in_degree,
            "final": final_weak_in_degree,
            "absolute_change": final_weak_in_degree - base_weak_in_degree,
            "percentage_change": f"{((final_weak_in_degree - base_weak_in_degree) / max(1, base_weak_in_degree)) * 100:.1f}%",
            "interpretation": "Pages vulnerable to being lost if a single link breaks (Lower is better).",
        },
        {
            "metric": "Average In-Degree per Page",
            "baseline": base_avg_in_degree,
            "final": final_avg_in_degree,
            "absolute_change": round(final_avg_in_degree - base_avg_in_degree, 2),
            "percentage_change": f"{((final_avg_in_degree - base_avg_in_degree) / max(0.01, base_avg_in_degree)) * 100:.1f}%",
            "interpretation": "Average incoming internal links per article (Higher indicates better interlinking).",
        },
    ]

    comp_df = pd.DataFrame(metrics_comparison)
    out_file = Path(output_csv)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    comp_df.to_csv(out_file, index=False)
    logger.info(f"Comparison report saved to {out_file}")
    return comp_df
