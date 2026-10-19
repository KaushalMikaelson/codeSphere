"""NetworkX-based internal link graph analysis and topological metrics engine."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse

import networkx as nx
import pandas as pd

from .urls import normalize_url

logger = logging.getLogger(__name__)


def classify_topic_cluster(url: str) -> str:
    """Classify URL into one of the four educational clusters or system categories."""
    path = urlparse(url).path.lower()
    if "/blog" in path:
        return "Roadmaps & Guides"
    elif "/programming" in path:
        return "Programming"
    elif "/dsa" in path:
        return "DSA"
    elif "/web-development" in path:
        return "Web Development"
    elif "/computer-science" in path:
        return "Core CS"
    elif path.rstrip("/") in ["", "/codesphere"]:
        return "Homepage"
    return "General"


class LinkGraphAnalyzer:
    """Constructs and analyzes the directed internal link graph G = (V, E)."""

    def __init__(
        self,
        edges: List[Dict[str, str]],
        discovered_urls: List[str],
        root_url: str,
        inventory_urls: Optional[List[str]] = None,
        exclude_sitewide: bool = False,
    ):
        self.root_url = normalize_url(root_url)
        self.exclude_sitewide = exclude_sitewide
        self.inventory_urls = [normalize_url(u) for u in (inventory_urls or []) if normalize_url(u)]

        # Filter edges if requested
        valid_edges = []
        for e in edges:
            if self.exclude_sitewide and e.get("link_type") == "sitewide":
                continue
            src = normalize_url(e["source"])
            tgt = normalize_url(e["target"])
            if src and tgt and src != tgt:  # Exclude self-loops
                valid_edges.append({
                    "source": src,
                    "target": tgt,
                    "anchor_text": e.get("anchor_text", ""),
                    "link_type": e.get("link_type", "contextual"),
                })

        self.raw_edges = valid_edges

        # Initialize NetworkX Directed Graph
        self.graph = nx.DiGraph()

        # Add all discovered nodes and inventory nodes
        all_nodes = set(normalize_url(u) for u in discovered_urls if normalize_url(u))
        all_nodes.update(self.inventory_urls)
        all_nodes.add(self.root_url)

        for node in all_nodes:
            self.graph.add_node(node, cluster=classify_topic_cluster(node))

        # Add edges (deduplicating parallel edges in simple DiGraph)
        self.unique_edges_dict = {}
        for e in self.raw_edges:
            pair = (e["source"], e["target"])
            if pair not in self.unique_edges_dict:
                self.unique_edges_dict[pair] = e
                self.graph.add_edge(e["source"], e["target"])

    def compute_metrics(self) -> pd.DataFrame:
        """Compute in-degree, out-degree, shortest click depth, PageRank, and flags for all nodes."""
        # 1. Shortest click depth from root
        depths = {}
        if self.root_url in self.graph:
            try:
                shortest_paths = nx.single_source_shortest_path_length(self.graph, self.root_url)
                for node in self.graph.nodes():
                    depths[node] = shortest_paths.get(node, -1)  # -1 represents unreachable
            except nx.NetworkXError:
                for node in self.graph.nodes():
                    depths[node] = -1
        else:
            for node in self.graph.nodes():
                depths[node] = -1

        # 2. PageRank with damping factor alpha = 0.85
        try:
            if len(self.graph) > 0 and self.graph.number_of_edges() > 0:
                pageranks = nx.pagerank(self.graph, alpha=0.85, max_iter=100, weight=None)
            else:
                pageranks = {node: 1.0 / max(1, len(self.graph)) for node in self.graph.nodes()}
        except Exception as exc:
            logger.warning(f"PageRank computation fallback: {exc}")
            pageranks = {node: 0.0 for node in self.graph.nodes()}

        # 3. Compile DataFrame
        records = []
        for node in sorted(self.graph.nodes()):
            in_deg = self.graph.in_degree(node)
            out_deg = self.graph.out_degree(node)
            depth = depths.get(node, -1)
            pr = round(pageranks.get(node, 0.0), 6)
            cluster = classify_topic_cluster(node)

            # An orphan page is a page with zero incoming links (in_deg == 0) that is not root,
            # or an inventory page that is completely unreachable from the root.
            is_orphan = (in_deg == 0 and node != self.root_url) or (depth == -1 and node != self.root_url)
            is_dead_end = (out_deg == 0)

            records.append({
                "url": node,
                "cluster": cluster,
                "in_degree": in_deg,
                "out_degree": out_deg,
                "click_depth": depth,
                "pagerank": pr,
                "is_orphan": is_orphan,
                "is_dead_end": is_dead_end,
            })

        df = pd.DataFrame(records)
        return df

    def get_summary_statistics(self, metrics_df: pd.DataFrame) -> Dict:
        """Calculate aggregate structural indicators for the website."""
        reachable_df = metrics_df[metrics_df["click_depth"] >= 0]
        orphan_df = metrics_df[metrics_df["is_orphan"] == True]
        dead_ends_df = metrics_df[metrics_df["is_dead_end"] == True]
        weak_in_degree = metrics_df[(metrics_df["in_degree"] <= 1) & (metrics_df["url"] != self.root_url)]

        avg_depth = round(reachable_df["click_depth"].mean(), 2) if not reachable_df.empty else 0.0
        max_depth = int(reachable_df["click_depth"].max()) if not reachable_df.empty else 0

        # Topic connectivity: Cross-cluster edges between non-homepage nodes
        cross_cluster_edges = 0
        total_cluster_edges = 0
        for u, v in self.graph.edges():
            c_u = classify_topic_cluster(u)
            c_v = classify_topic_cluster(v)
            if c_u != "Homepage" and c_v != "Homepage":
                total_cluster_edges += 1
                if c_u != c_v:
                    cross_cluster_edges += 1

        topic_connectivity_ratio = round(
            cross_cluster_edges / max(1, total_cluster_edges), 3
        ) if total_cluster_edges > 0 else 0.0

        return {
            "total_nodes": int(self.graph.number_of_nodes()),
            "total_unique_edges": int(self.graph.number_of_edges()),
            "average_in_degree": round(float(metrics_df["in_degree"].mean()), 2),
            "average_out_degree": round(float(metrics_df["out_degree"].mean()), 2),
            "reachable_pages_count": len(reachable_df),
            "average_click_depth": avg_depth,
            "maximum_click_depth": max_depth,
            "orphan_pages_count": len(orphan_df),
            "dead_end_pages_count": len(dead_ends_df),
            "weak_in_degree_count": len(weak_in_degree),
            "topic_connectivity_ratio": topic_connectivity_ratio,
        }

    def export_data(
        self,
        output_dir: str,
        metrics_df: pd.DataFrame,
        summary: Dict,
        broken_links: Optional[List[Dict]] = None,
    ):
        """Export all datasets: metrics.csv, edges.csv, orphan_pages.csv, broken_links.csv, graph.gexf, crawl_summary.json."""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        # 1. metrics.csv
        metrics_df.to_csv(out_path / "metrics.csv", index=False)

        # 2. edges.csv
        edges_rows = list(self.unique_edges_dict.values())
        edges_df = pd.DataFrame(edges_rows)
        if edges_df.empty:
            edges_df = pd.DataFrame(columns=["source", "target", "anchor_text", "link_type"])
        edges_df.to_csv(out_path / "edges.csv", index=False)

        # 3. orphan_pages.csv
        orphan_df = metrics_df[metrics_df["is_orphan"] == True]
        orphan_export = orphan_df[["url", "cluster", "in_degree", "click_depth"]].copy()
        orphan_export["detection_reason"] = orphan_export.apply(
            lambda r: "Zero incoming links" if r["in_degree"] == 0 else "Unreachable from homepage", axis=1
        )
        orphan_export.to_csv(out_path / "orphan_pages.csv", index=False)

        # 4. broken_links.csv
        broken_df = pd.DataFrame(broken_links or [])
        if broken_df.empty:
            broken_df = pd.DataFrame(columns=["source_url", "target_url", "status_code", "anchor_text"])
        broken_df.to_csv(out_path / "broken_links.csv", index=False)

        # 5. crawl_summary.json
        with open(out_path / "crawl_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        # 6. Gephi graph export (.gexf)
        for _, row in metrics_df.iterrows():
            node = row["url"]
            if node in self.graph:
                self.graph.nodes[node]["in_degree"] = int(row["in_degree"])
                self.graph.nodes[node]["out_degree"] = int(row["out_degree"])
                self.graph.nodes[node]["click_depth"] = int(row["click_depth"])
                self.graph.nodes[node]["pagerank"] = float(row["pagerank"])
                self.graph.nodes[node]["cluster"] = str(row["cluster"])

        nx.write_gexf(self.graph, str(out_path / "graph.gexf"))
        logger.info(f"Graph analysis exports successfully saved to: {out_path}")
