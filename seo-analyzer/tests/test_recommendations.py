"""Tests for recommendation engine heuristics."""

import pandas as pd
import pytest
from seo_analyzer.recommendations import InternalLinkRecommender


def test_recommend_orphan_and_deep_pages():
    metrics_data = [
        {"url": "http://localhost/codesphere", "cluster": "Homepage", "in_degree": 3, "out_degree": 2, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/dsa/deep-topic", "cluster": "DSA", "in_degree": 1, "out_degree": 1, "click_depth": 5, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/blog/orphan-page", "cluster": "Roadmaps & Guides", "in_degree": 0, "out_degree": 0, "click_depth": -1, "is_orphan": True, "is_dead_end": True},
    ]
    metrics_df = pd.DataFrame(metrics_data)
    edges_df = pd.DataFrame(columns=["source", "target"])

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
        depth_threshold=3
    )
    rec_df = recommender.generate_recommendations()

    problems = list(rec_df["problem_detected"].values)
    assert "Orphan Page" in problems
    assert "Excessive Crawl Depth" in problems


def test_recommend_affinity_rules():
    metrics_data = [
        {"url": "http://localhost/codesphere/dsa/algorithms/recursion", "cluster": "DSA", "in_degree": 2, "out_degree": 0, "click_depth": 2, "is_orphan": False, "is_dead_end": True},
        {"url": "http://localhost/codesphere/dsa/algorithms/dynamic-programming", "cluster": "DSA", "in_degree": 1, "out_degree": 1, "click_depth": 3, "is_orphan": False, "is_dead_end": False},
    ]
    metrics_df = pd.DataFrame(metrics_data)
    edges_df = pd.DataFrame(columns=["source", "target"])

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
    )
    rec_df = recommender.generate_recommendations()

    # Should recommend connecting recursion -> dynamic programming
    actions = " ".join(rec_df["suggested_action"].values)
    assert "Dynamic Programming" in actions


def test_exclude_low_value_urls_from_recommendations():
    """Verify that paginated archives, uncategorized taxonomy, and utility URLs are excluded by default."""
    metrics_data = [
        {"url": "http://localhost/codesphere", "cluster": "Homepage", "in_degree": 40, "out_degree": 30, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        # Low-value targets that should NOT receive recommendations
        {"url": "http://localhost/codesphere/category/uncategorized", "cluster": "General", "in_degree": 1, "out_degree": 20, "click_depth": 3, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/category/dsa/page/2", "cluster": "DSA", "in_degree": 1, "out_degree": 20, "click_depth": 2, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/hello-world", "cluster": "General", "in_degree": 1, "out_degree": 0, "click_depth": 3, "is_orphan": False, "is_dead_end": True},
        {"url": "http://localhost/codesphere/author/admin", "cluster": "General", "in_degree": 1, "out_degree": 5, "click_depth": 3, "is_orphan": False, "is_dead_end": False},
        # High-value educational content with fragile connectivity
        {"url": "http://localhost/codesphere/dsa/binary-trees", "cluster": "DSA", "in_degree": 1, "out_degree": 5, "click_depth": 1, "is_orphan": False, "is_dead_end": False},
    ]
    metrics_df = pd.DataFrame(metrics_data)
    edges_df = pd.DataFrame(columns=["source", "target"])

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
        depth_threshold=2,
        exclude_low_value=True,
    )
    rec_df = recommender.generate_recommendations()

    recommended_targets = list(rec_df["target_page"].values)

    # Low-value URLs must NOT be recommended
    assert "http://localhost/codesphere/category/uncategorized" not in recommended_targets
    assert "http://localhost/codesphere/category/dsa/page/2" not in recommended_targets
    assert "http://localhost/codesphere/hello-world" not in recommended_targets
    assert "http://localhost/codesphere/author/admin" not in recommended_targets

    # Educational content MUST be recommended
    assert "http://localhost/codesphere/dsa/binary-trees" in recommended_targets

    edu_rec = rec_df[rec_df["target_page"] == "http://localhost/codesphere/dsa/binary-trees"].iloc[0]
    assert edu_rec["problem_detected"] == "Fragile Single Inbound Link"
    assert edu_rec["priority"] == "High"
    assert "Educational In-Degree Vulnerability" in edu_rec["confidence"]


def test_deprioritize_low_value_urls_when_included():
    """Verify that when exclude_low_value=False, low-value URLs are marked with Low priority and confidence."""
    metrics_data = [
        {"url": "http://localhost/codesphere", "cluster": "Homepage", "in_degree": 40, "out_degree": 30, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/category/uncategorized", "cluster": "General", "in_degree": 1, "out_degree": 20, "click_depth": 3, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/dsa/binary-trees", "cluster": "DSA", "in_degree": 1, "out_degree": 5, "click_depth": 1, "is_orphan": False, "is_dead_end": False},
    ]
    metrics_df = pd.DataFrame(metrics_data)
    edges_df = pd.DataFrame(columns=["source", "target"])

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
        depth_threshold=2,
        exclude_low_value=False,
    )
    rec_df = recommender.generate_recommendations()

    # Both targets should now be present
    targets = list(rec_df["target_page"].values)
    assert "http://localhost/codesphere/category/uncategorized" in targets
    assert "http://localhost/codesphere/dsa/binary-trees" in targets

    # Educational content must be ranked above low-value utility
    edu_row = rec_df[rec_df["target_page"] == "http://localhost/codesphere/dsa/binary-trees"].iloc[0]
    uncat_rows = rec_df[rec_df["target_page"] == "http://localhost/codesphere/category/uncategorized"]

    assert edu_row["priority"] == "High"
    for _, uncat_row in uncat_rows.iterrows():
        assert uncat_row["priority"] == "Low"
        assert "Deprioritized: Low-Value Archive/Utility URL" in uncat_row["confidence"]


def test_topic_hub_depth_and_orphan_handling():
    """Verify that topic hubs are properly recognized and prioritized for excessive depth and orphan status."""
    metrics_data = [
        {"url": "http://localhost/codesphere", "cluster": "Homepage", "in_degree": 40, "out_degree": 30, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/category/dsa", "cluster": "DSA", "in_degree": 1, "out_degree": 25, "click_depth": 4, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/category/web-development", "cluster": "Web Development", "in_degree": 0, "out_degree": 10, "click_depth": -1, "is_orphan": True, "is_dead_end": False},
    ]
    metrics_df = pd.DataFrame(metrics_data)
    edges_df = pd.DataFrame(columns=["source", "target"])

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
        depth_threshold=2,
        exclude_low_value=True,
    )
    rec_df = recommender.generate_recommendations()

    # Topic hub excessive depth
    depth_recs = rec_df[rec_df["problem_detected"] == "Excessive Crawl Depth"]
    assert len(depth_recs) == 1
    assert depth_recs.iloc[0]["target_page"] == "http://localhost/codesphere/category/dsa"
    assert depth_recs.iloc[0]["priority"] == "High"

    # Topic hub orphan
    orphan_recs = rec_df[rec_df["problem_detected"] == "Orphan Page"]
    assert len(orphan_recs) == 1
    assert orphan_recs.iloc[0]["target_page"] == "http://localhost/codesphere/category/web-development"
    assert orphan_recs.iloc[0]["priority"] == "High"


def test_well_linked_educational_site_no_false_alarms():
    """Verify that reachable, well-linked educational articles with connected affinities produce zero false recommendations."""
    metrics_data = [
        {"url": "http://localhost/codesphere", "cluster": "Homepage", "in_degree": 40, "out_degree": 32, "click_depth": 0, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/binary-search-trees", "cluster": "General", "in_degree": 7, "out_degree": 20, "click_depth": 1, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/binary-trees", "cluster": "General", "in_degree": 40, "out_degree": 21, "click_depth": 1, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/tree-traversal", "cluster": "General", "in_degree": 8, "out_degree": 21, "click_depth": 1, "is_orphan": False, "is_dead_end": False},
        # Low-value URLs that would have triggered naive metrics
        {"url": "http://localhost/codesphere/category/uncategorized", "cluster": "General", "in_degree": 1, "out_degree": 20, "click_depth": 3, "is_orphan": False, "is_dead_end": False},
        {"url": "http://localhost/codesphere/category/dsa/page/2", "cluster": "DSA", "in_degree": 1, "out_degree": 20, "click_depth": 2, "is_orphan": False, "is_dead_end": False},
    ]
    edges_data = [
        {"source": "http://localhost/codesphere/binary-trees", "target": "http://localhost/codesphere/tree-traversal"},
        {"source": "http://localhost/codesphere/binary-trees", "target": "http://localhost/codesphere/binary-search-trees"},
    ]
    metrics_df = pd.DataFrame(metrics_data)
    edges_df = pd.DataFrame(edges_data)

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
        depth_threshold=2,
        exclude_low_value=True,
    )
    rec_df = recommender.generate_recommendations()

    # Zero false recommendations generated because all content is reachable and connected,
    # and low-value archives are cleanly excluded.
    assert len(rec_df) == 0

