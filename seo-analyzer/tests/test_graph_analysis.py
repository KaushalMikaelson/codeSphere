"""Tests for NetworkX graph analysis, PageRank, click depth, and orphan detection."""

import pytest
import pandas as pd
from seo_analyzer.graph_analysis import LinkGraphAnalyzer, classify_topic_cluster


def test_classify_topic_cluster():
    assert classify_topic_cluster("http://localhost/codesphere/programming/fundamentals") == "Programming"
    assert classify_topic_cluster("http://localhost/codesphere/dsa/trees") == "DSA"
    assert classify_topic_cluster("http://localhost/codesphere/web-development/rest-apis") == "Web Development"
    assert classify_topic_cluster("http://localhost/codesphere/computer-science/databases") == "Core CS"
    assert classify_topic_cluster("http://localhost/codesphere/blog/dsa-roadmap") == "Roadmaps & Guides"
    assert classify_topic_cluster("http://localhost/codesphere") == "Homepage"


def test_graph_analyzer_metrics_and_depth():
    root = "http://localhost/codesphere"
    page_a = f"{root}/programming/functions"
    page_b = f"{root}/dsa/recursion"
    orphan_page = f"{root}/blog/isolated-guide"

    # Topology: Root -> A -> B
    # orphan_page is in inventory, but has NO links
    edges = [
        {"source": root, "target": page_a, "anchor_text": "Functions", "link_type": "contextual"},
        {"source": page_a, "target": page_b, "anchor_text": "Recursion", "link_type": "contextual"},
        # Duplicate edge to verify deduplication
        {"source": page_a, "target": page_b, "anchor_text": "Recursion Duplicate", "link_type": "contextual"},
    ]

    discovered = [root, page_a, page_b]
    inventory = [root, page_a, page_b, orphan_page]

    analyzer = LinkGraphAnalyzer(
        edges=edges,
        discovered_urls=discovered,
        root_url=root,
        inventory_urls=inventory
    )

    metrics_df = analyzer.compute_metrics()

    # Verify nodes
    assert len(metrics_df) == 4

    # Verify duplicate edge deduplication in DiGraph
    assert analyzer.graph.number_of_edges() == 2

    # Check depths
    depth_map = dict(zip(metrics_df["url"], metrics_df["click_depth"]))
    assert depth_map[root] == 0
    assert depth_map[page_a] == 1
    assert depth_map[page_b] == 2
    assert depth_map[orphan_page] == -1  # Unreachable

    # Check orphan flags
    orphan_map = dict(zip(metrics_df["url"], metrics_df["is_orphan"]))
    assert orphan_map[root] is False
    assert orphan_map[page_a] is False
    assert orphan_map[page_b] is False
    assert orphan_map[orphan_page] is True

    # Check dead-end flag (page_b has out-degree 0)
    dead_end_map = dict(zip(metrics_df["url"], metrics_df["is_dead_end"]))
    assert dead_end_map[page_b] is True
    assert dead_end_map[page_a] is False

    # Check PageRank sum is approximately 1.0
    pr_sum = metrics_df["pagerank"].sum()
    assert pytest.approx(pr_sum, rel=1e-2) == 1.0


def test_get_summary_statistics():
    root = "http://localhost/codesphere"
    page_a = f"{root}/programming/intro"
    page_b = f"{root}/dsa/trees"

    edges = [
        {"source": root, "target": page_a, "link_type": "sitewide"},
        {"source": page_a, "target": page_b, "link_type": "contextual"},
    ]

    analyzer = LinkGraphAnalyzer(
        edges=edges,
        discovered_urls=[root, page_a, page_b],
        root_url=root,
    )
    metrics_df = analyzer.compute_metrics()
    summary = analyzer.get_summary_statistics(metrics_df)

    assert summary["total_nodes"] == 3
    assert summary["total_unique_edges"] == 2
    assert summary["maximum_click_depth"] == 2
    assert summary["average_click_depth"] == 1.0  # (0 + 1 + 2) / 3 = 1.0
    assert summary["dead_end_pages_count"] == 1  # page_b
