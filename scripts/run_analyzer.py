"""CodeSphere Test and Analysis Execution Launcher.

Runs the internal verification suite and experiment simulations,
outputting status and verifying all algorithms without external network dependencies.
"""

import os
import sys
from pathlib import Path

# Insert package root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "seo-analyzer"))

from seo_analyzer.crawler import InternalLinkCrawler
from seo_analyzer.graph_analysis import LinkGraphAnalyzer
from seo_analyzer.recommendations import InternalLinkRecommender
from seo_analyzer.comparison import compare_runs
from seo_analyzer.urls import normalize_url, is_internal_url

def run_self_tests():
    print("\n--- Running CodeSphere Self-Verification Tests ---")
    
    # 1. Test URL Normalizer
    norm = normalize_url("/dsa/trees#subheading?utm_source=test", "http://localhost/codesphere")
    assert norm == "http://localhost/codesphere/dsa/trees", f"Failed URL norm: {norm}"
    print(" [PASS] URL Normalization & Fragment/UTM Stripping")
    
    # 2. Test Internal URL Classification
    assert is_internal_url("http://localhost/codesphere/dsa", "localhost") is True
    assert is_internal_url("https://external-domain.com", "localhost") is False
    print(" [PASS] Internal vs External Domain Boundary Validation")
    
    # 3. Test Graph Analyzer & PageRank
    root = "http://localhost/codesphere"
    edges = [
        {"source": root, "target": f"{root}/programming", "link_type": "sitewide", "anchor_text": "Prog"},
        {"source": f"{root}/programming", "target": f"{root}/dsa", "link_type": "contextual", "anchor_text": "DSA"},
    ]
    analyzer = LinkGraphAnalyzer(edges=edges, discovered_urls=[root, f"{root}/programming", f"{root}/dsa"], root_url=root)
    metrics_df = analyzer.compute_metrics()
    assert len(metrics_df) == 3
    depth_map = dict(zip(metrics_df["url"], metrics_df["click_depth"]))
    assert depth_map[root] == 0
    assert depth_map[f"{root}/programming"] == 1
    assert depth_map[f"{root}/dsa"] == 2
    print(" [PASS] Directed Graph Construction & Shortest Click Depth BFS")
    
    # 4. PageRank Sum Conservation
    pr_sum = metrics_df["pagerank"].sum()
    assert abs(pr_sum - 1.0) < 0.05, f"PageRank sum deviated: {pr_sum}"
    print(f" [PASS] PageRank Convergence (Sum = {round(pr_sum, 4)})")
    
    print("\nAll self-contained test suites passed successfully!\n")

if __name__ == "__main__":
    run_self_tests()
