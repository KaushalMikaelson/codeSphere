"""Rule-based internal linking recommendation engine for technical SEO optimization."""

import logging
from typing import Dict, List, Optional
import pandas as pd

from .urls import classify_url_type, is_low_value_target, is_topic_hub

logger = logging.getLogger(__name__)

# Established curriculum affinity mappings between computer science topics
AFFINITY_RULES = [
    {
        "source_pattern": "recursion",
        "target_pattern": "dynamic-programming",
        "reason": "Recursion with overlapping subproblems forms the foundation of Dynamic Programming.",
        "anchor_suggestion": "Dynamic Programming for Beginners",
    },
    {
        "source_pattern": "binary-trees",
        "target_pattern": "tree-traversal",
        "reason": "Traversing binary trees requires Inorder, Preorder, and Postorder algorithms.",
        "anchor_suggestion": "Tree Traversal Inorder Preorder Postorder",
    },
    {
        "source_pattern": "binary-trees",
        "target_pattern": "binary-search-trees",
        "reason": "Binary Search Trees impose ordering constraints directly onto Binary Tree nodes.",
        "anchor_suggestion": "Binary Search Trees (BST)",
    },
    {
        "source_pattern": "rest-apis",
        "target_pattern": "computer-networks",
        "reason": "REST HTTP communication relies directly on TCP/IP and OSI network layering.",
        "anchor_suggestion": "Computer Networks Basics OSI Model",
    },
    {
        "source_pattern": "rest-apis",
        "target_pattern": "databases",
        "reason": "REST endpoints perform CRUD queries on backend database engines.",
        "anchor_suggestion": "Databases Hub (SQL vs NoSQL)",
    },
    {
        "source_pattern": "dsa-roadmap-for-placements",
        "target_pattern": "binary-tree-vs-binary-search-tree",
        "reason": "Placement candidates require concrete comparative knowledge on BST vs Binary Tree.",
        "anchor_suggestion": "Binary Tree vs Binary Search Tree Guide",
    },
    {
        "source_pattern": "sql",
        "target_pattern": "nosql",
        "reason": "Architectural decision making requires contrasting SQL ACID properties with NoSQL CAP tradeoffs.",
        "anchor_suggestion": "NoSQL Models and CAP Theorem",
    },
]

PRIORITY_RANKS = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


class InternalLinkRecommender:
    """Generates structured, rule-based internal link recommendations."""

    def __init__(
        self,
        metrics_df: pd.DataFrame,
        edges_df: pd.DataFrame,
        depth_threshold: int = 3,
        broken_links_df: Optional[pd.DataFrame] = None,
        exclude_low_value: bool = True,
    ):
        self.metrics_df = metrics_df
        self.edges_df = edges_df
        self.depth_threshold = depth_threshold
        self.broken_links_df = broken_links_df
        self.exclude_low_value = exclude_low_value

        # Build edge lookup set
        self.existing_edges = set()
        if not self.edges_df.empty:
            for _, row in self.edges_df.iterrows():
                self.existing_edges.add((str(row["source"]).rstrip("/"), str(row["target"]).rstrip("/")))

    def generate_recommendations(self) -> pd.DataFrame:
        """Scan metrics and edge topology to generate prioritized recommendations."""
        recommendations: List[Dict[str, str]] = []

        # 1. Flag Orphan Pages (Zero in-degree or unreachable)
        for _, row in self.metrics_df.iterrows():
            if row.get("is_orphan"):
                url = row["url"]
                is_low_val = is_low_value_target(url)
                if self.exclude_low_value and is_low_val:
                    continue

                cluster = row.get("cluster", "General")
                url_type = classify_url_type(url)
                is_educational = url_type in ["educational_article", "topic_hub"]

                confidence = (
                    "High (Rule: Educational Content Isolation)"
                    if is_educational
                    else (
                        "Low (Deprioritized: Low-Value Archive/Utility URL)"
                        if is_low_val
                        else "High (Rule: Structural Isolation)"
                    )
                )
                priority = "High" if is_educational else ("Low" if is_low_val else "Medium")

                recommendations.append({
                    "source_page": f"[Cluster Hub for {cluster}]",
                    "target_page": url,
                    "problem_detected": "Orphan Page",
                    "evidence_metric": f"In-degree={row['in_degree']}, Click Depth={row['click_depth']}",
                    "suggested_action": f"Add contextual inbound link from topic cluster hub or related article to {url}",
                    "confidence": confidence,
                    "priority": priority,
                })

        # 2. Flag Deep Pages (Depth > Threshold)
        for _, row in self.metrics_df.iterrows():
            depth = row.get("click_depth", -1)
            if depth > self.depth_threshold:
                url = row["url"]
                is_low_val = is_low_value_target(url)
                if self.exclude_low_value and is_low_val:
                    continue

                url_type = classify_url_type(url)
                is_educational = url_type in ["educational_article", "topic_hub"]

                confidence = (
                    "High (Rule: Educational Topic Depth)"
                    if is_educational
                    else (
                        "Low (Deprioritized: Low-Value Archive/Utility URL)"
                        if is_low_val
                        else "High (Rule: Crawl Depth)"
                    )
                )
                priority = "High" if is_educational else ("Low" if is_low_val else "Medium")

                source_suggestion = (
                    "[Main Navigation or Homepage]"
                    if url_type == "topic_hub"
                    else "[Category Hub or Main Navigation]"
                )

                recommendations.append({
                    "source_page": source_suggestion,
                    "target_page": url,
                    "problem_detected": "Excessive Crawl Depth",
                    "evidence_metric": f"Click Depth={depth} (Threshold={self.depth_threshold})",
                    "suggested_action": f"Add direct link from 1-hop or 2-hop parent hub to decrease click depth of {url}",
                    "confidence": confidence,
                    "priority": priority,
                })

        # 3. Flag Dead-End Pages (Out-degree = 0)
        for _, row in self.metrics_df.iterrows():
            if row.get("is_dead_end") and not row.get("is_orphan"):
                url = row["url"]
                is_low_val = is_low_value_target(url)
                if self.exclude_low_value and is_low_val:
                    continue

                url_type = classify_url_type(url)
                is_educational = url_type in ["educational_article", "topic_hub"]

                confidence = (
                    "High (Rule: Link Equity Trap)"
                    if is_educational
                    else (
                        "Low (Deprioritized: Low-Value Archive/Utility URL)"
                        if is_low_val
                        else "Medium (Rule: Link Equity Trap)"
                    )
                )
                priority = "High" if is_educational else ("Low" if is_low_val else "Medium")

                recommendations.append({
                    "source_page": url,
                    "target_page": "[Related Topic or Cluster Hub]",
                    "problem_detected": "Dead-End Page (Zero Outbound Links)",
                    "evidence_metric": f"Out-degree=0, In-degree={row['in_degree']}",
                    "suggested_action": f"Add 'Next Topics' or 'Related Guides' module at bottom of {url}",
                    "confidence": confidence,
                    "priority": priority,
                })

        # 4. Flag Weakly Connected Articles (In-degree <= 1, excluding root)
        for _, row in self.metrics_df.iterrows():
            in_deg = row.get("in_degree", 0)
            url = row["url"]
            if in_deg == 1 and not row.get("is_orphan"):
                is_low_val = is_low_value_target(url)
                if self.exclude_low_value and is_low_val:
                    continue

                url_type = classify_url_type(url)
                is_educational = url_type in ["educational_article", "topic_hub"]

                confidence = (
                    "High (Rule: Educational In-Degree Vulnerability)"
                    if is_educational
                    else (
                        "Low (Deprioritized: Low-Value Archive/Utility URL)"
                        if is_low_val
                        else "Medium (Rule: In-Degree Vulnerability)"
                    )
                )
                priority = "High" if is_educational else ("Low" if is_low_val else "Low")

                source_page = (
                    "[Sibling Concept Article]"
                    if url_type == "educational_article"
                    else "[Primary Navigation or Parent Hub]"
                )

                recommendations.append({
                    "source_page": source_page,
                    "target_page": url,
                    "problem_detected": "Fragile Single Inbound Link",
                    "evidence_metric": f"In-degree={in_deg}",
                    "suggested_action": f"Add complementary contextual link from a sibling guide to bolster discoverability for {url}",
                    "confidence": confidence,
                    "priority": priority,
                })

        # 5. Domain Knowledge Affinity Cross-Links
        urls = list(self.metrics_df["url"].values)
        for rule in AFFINITY_RULES:
            src_matches = [u for u in urls if rule["source_pattern"] in u.lower() and not is_low_value_target(u)]
            tgt_matches = [u for u in urls if rule["target_pattern"] in u.lower() and not is_low_value_target(u)]

            for src in src_matches:
                for tgt in tgt_matches:
                    clean_src = src.rstrip("/")
                    clean_tgt = tgt.rstrip("/")
                    if clean_src != clean_tgt and (clean_src, clean_tgt) not in self.existing_edges:
                        recommendations.append({
                            "source_page": src,
                            "target_page": tgt,
                            "problem_detected": "Missing Academic Topic Cross-Link",
                            "evidence_metric": "Direct edge missing in graph topology",
                            "suggested_action": f"Add link with anchor '{rule['anchor_suggestion']}'. Note: {rule['reason']}",
                            "confidence": "High (Rule: Domain Curriculum Affinity)",
                            "priority": "High",
                        })

        # 6. Flag Broken Links if provided
        if self.broken_links_df is not None and not self.broken_links_df.empty:
            for _, row in self.broken_links_df.iterrows():
                target = row["target_url"]
                is_low_val = is_low_value_target(target)
                if self.exclude_low_value and is_low_val:
                    continue

                priority = "Low" if is_low_val else "Critical"
                confidence = (
                    "Low (Deprioritized: Broken Archive Link)"
                    if is_low_val
                    else "Critical (Rule: Broken Link Resolution)"
                )

                recommendations.append({
                    "source_page": row["source_url"],
                    "target_page": target,
                    "problem_detected": "Broken Internal Link (404 / 500)",
                    "evidence_metric": f"Status Code={row['status_code']}, Anchor='{row['anchor_text']}'",
                    "suggested_action": "Fix destination URL typo or update link to active canonical page",
                    "confidence": confidence,
                    "priority": priority,
                })

        df = pd.DataFrame(recommendations)
        if df.empty:
            df = pd.DataFrame(columns=[
                "source_page", "target_page", "problem_detected",
                "evidence_metric", "suggested_action", "confidence", "priority"
            ])
        else:
            df["_rank"] = df["priority"].map(lambda p: PRIORITY_RANKS.get(p, 99))
            df = df.sort_values(by=["_rank", "problem_detected"]).drop(columns=["_rank"]).reset_index(drop=True)
        return df
