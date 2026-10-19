"""Tests for baseline vs final comparison and delta computation."""

import pandas as pd
import pytest
from seo_analyzer.comparison import compare_runs


def test_compare_runs(tmp_path):
    # Setup synthetic baseline and final metrics CSVs
    base_data = [
        {"url": "http://localhost/codesphere", "in_degree": 2, "out_degree": 2, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/topic-a", "in_degree": 1, "out_degree": 0, "click_depth": 3, "is_orphan": False, "is_dead_end": True},
        {"url": "http://localhost/codesphere/orphan-b", "in_degree": 0, "out_degree": 0, "click_depth": -1, "is_orphan": True, "is_dead_end": True},
    ]
    final_data = [
        {"url": "http://localhost/codesphere", "in_degree": 3, "out_degree": 3, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/topic-a", "in_degree": 2, "out_degree": 1, "click_depth": 1, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/orphan-b", "in_degree": 1, "out_degree": 1, "click_depth": 2, "is_orphan": False, "is_dead_end": False},
    ]

    base_file = tmp_path / "baseline_metrics.csv"
    final_file = tmp_path / "final_metrics.csv"
    out_file = tmp_path / "comparison.csv"

    pd.DataFrame(base_data).to_csv(base_file, index=False)
    pd.DataFrame(final_data).to_csv(final_file, index=False)

    comp_df = compare_runs(str(base_file), str(final_file), str(out_file))

    # Verify orphan reduction
    orphan_row = comp_df[comp_df["metric"] == "Orphan Pages Count"].iloc[0]
    assert orphan_row["baseline"] == 1
    assert orphan_row["final"] == 0
    assert orphan_row["absolute_change"] == -1

    # Verify dead-end reduction
    dead_end_row = comp_df[comp_df["metric"] == "Dead-End Pages (Out-degree = 0)"].iloc[0]
    assert dead_end_row["baseline"] == 2
    assert dead_end_row["final"] == 0
