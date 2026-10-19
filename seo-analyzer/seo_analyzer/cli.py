"""Command Line Interface for CodeSphere SEO Analyzer."""

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from .comparison import compare_runs
from .crawler import InternalLinkCrawler
from .graph_analysis import LinkGraphAnalyzer
from .recommendations import InternalLinkRecommender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("seo_analyzer")


def load_inventory_file(filepath: str) -> list[str]:
    """Load line-delimited list of published URLs."""
    path = Path(filepath)
    if not path.exists():
        logger.warning(f"Inventory file {filepath} not found.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return urls


def handle_crawl(args):
    """Execute live or local crawl and run graph analysis."""
    inventory = load_inventory_file(args.inventory) if args.inventory else []
    
    crawler = InternalLinkCrawler(
        start_url=args.start_url,
        max_pages=args.max_pages,
        request_delay=args.delay,
        timeout=args.timeout,
    )
    
    print(f"\n=======================================================")
    print(f" CodeSphere SEO Analyzer: Starting Internal Crawl")
    print(f" Target: {args.start_url}")
    print(f" Max Pages Cap: {args.max_pages}")
    print(f" Output Directory: {args.output_dir}")
    print(f"=======================================================\n")
    
    crawl_result = crawler.crawl()
    
    analyzer = LinkGraphAnalyzer(
        edges=crawl_result["edges"],
        discovered_urls=crawl_result["visited_urls"],
        root_url=args.start_url,
        inventory_urls=inventory,
        exclude_sitewide=args.exclude_sitewide,
    )
    
    metrics_df = analyzer.compute_metrics()
    summary = analyzer.get_summary_statistics(metrics_df)
    summary["crawl_meta"] = crawl_result["summary"]
    
    analyzer.export_data(
        output_dir=args.output_dir,
        metrics_df=metrics_df,
        summary=summary,
        broken_links=crawl_result["broken_links"],
    )
    
    print("\n--- Crawl & Graph Topology Summary ---")
    for k, v in summary.items():
        if k != "crawl_meta":
            print(f"  {k:30}: {v}")
    print(f"\nAll datasets and Gephi graph exported to {args.output_dir}/\n")


def handle_compare(args):
    """Compare baseline vs final metrics."""
    print(f"\nComparing Baseline ({args.baseline}) with Final ({args.final})...")
    df = compare_runs(args.baseline, args.final, args.output)
    print("\n--- Baseline vs Final Delta Summary ---")
    for _, row in df.iterrows():
        print(f"  {row['metric']:35}: {row['baseline']} -> {row['final']} (Change: {row['absolute_change']}, {row['percentage_change']})")
    print(f"\nFull comparison CSV written to: {args.output}\n")


def handle_recommend(args):
    """Generate internal linking recommendations."""
    metrics_df = pd.read_csv(args.metrics)
    edges_df = pd.read_csv(args.edges) if args.edges and Path(args.edges).exists() else pd.DataFrame()
    broken_df = pd.read_csv(args.broken) if args.broken and Path(args.broken).exists() else None

    exclude_low_val = getattr(args, "exclude_low_value", True)

    recommender = InternalLinkRecommender(
        metrics_df=metrics_df,
        edges_df=edges_df,
        depth_threshold=args.depth_threshold,
        broken_links_df=broken_df,
        exclude_low_value=exclude_low_val,
    )
    
    rec_df = recommender.generate_recommendations()
    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    rec_df.to_csv(out_file, index=False)
    
    filter_note = " (excluding low-value archive/utility URLs)" if exclude_low_val else " (including low-value archive/utility URLs)"
    print(f"\nGenerated {len(rec_df)} internal linking recommendations{filter_note} -> {args.output}")
    if not rec_df.empty:
        print("\nTop 5 Priority Recommendations:")
        for idx, row in rec_df.head(5).iterrows():
            priority_tag = f"[{row['priority']}] " if "priority" in row and pd.notna(row["priority"]) else ""
            print(f"  {priority_tag}[{row['problem_detected']}] {row['target_page']}")
            print(f"    Action: {row['suggested_action']}")
    else:
        print("\nAll educational articles and topic hubs meet internal linking, depth, and connectivity standards.")


def main():
    parser = argparse.ArgumentParser(
        prog="seo-analyzer",
        description="CodeSphere Internal Link Graph Analyzer & Technical SEO Auditor"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: crawl
    crawl_parser = subparsers.add_parser("crawl", help="Crawl internal pages and compute graph metrics")
    crawl_parser.add_argument("--start-url", required=True, help="Homepage or start URL")
    crawl_parser.add_argument("--max-pages", type=int, default=100, help="Maximum pages to crawl")
    crawl_parser.add_argument("--delay", type=float, default=0.05, help="Polite delay between requests (seconds)")
    crawl_parser.add_argument("--timeout", type=int, default=10, help="Request timeout (seconds)")
    crawl_parser.add_argument("--inventory", default="", help="Path to url_inventory.txt")
    crawl_parser.add_argument("--output-dir", default="data/baseline", help="Directory to save CSV and GEXF")
    crawl_parser.add_argument("--exclude-sitewide", action="store_true", help="Exclude header/footer links")
    crawl_parser.set_defaults(func=handle_crawl)

    # Subcommand: compare
    compare_parser = subparsers.add_parser("compare", help="Compare baseline and final crawl metrics")
    compare_parser.add_argument("--baseline", required=True, help="Path to baseline metrics.csv")
    compare_parser.add_argument("--final", required=True, help="Path to final metrics.csv")
    compare_parser.add_argument("--output", default="data/comparison.csv", help="Output comparison CSV path")
    compare_parser.set_defaults(func=handle_compare)

    # Subcommand: recommend
    rec_parser = subparsers.add_parser("recommend", help="Generate internal link recommendations")
    rec_parser.add_argument("--metrics", required=True, help="Path to metrics.csv")
    rec_parser.add_argument("--edges", default="", help="Path to edges.csv")
    rec_parser.add_argument("--broken", default="", help="Path to broken_links.csv")
    rec_parser.add_argument("--depth-threshold", type=int, default=3, help="Max desired click depth")
    rec_parser.add_argument("--output", default="data/recommendations.csv", help="Output recommendations CSV")
    rec_parser.add_argument("--include-low-value", dest="exclude_low_value", action="store_false", default=True, help="Include and deprioritize low-value archive/utility URLs")
    rec_parser.add_argument("--exclude-low-value", dest="exclude_low_value", action="store_true", default=True, help="Exclude low-value archive/utility URLs (default: True)")
    rec_parser.set_defaults(func=handle_recommend)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
