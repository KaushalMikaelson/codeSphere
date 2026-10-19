"""Breadth-First internal HTML crawler for technical SEO and graph construction."""

import logging
import time
from collections import deque
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .urls import (
    extract_canonical_url,
    is_crawlable_html_resource,
    is_internal_url,
    normalize_url,
)

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "CodeSphere-SEO-Auditor/1.0 (+https://github.com/codesphere)"


class InternalLinkCrawler:
    """Polite, breadth-first crawler designed for internal link graph construction."""

    def __init__(
        self,
        start_url: str,
        max_pages: int = 100,
        request_delay: float = 0.05,
        timeout: int = 10,
        user_agent: str = DEFAULT_USER_AGENT,
        session: Optional[requests.Session] = None,
    ):
        self.start_url = normalize_url(start_url)
        self.max_pages = max_pages
        self.request_delay = request_delay
        self.timeout = timeout
        self.user_agent = user_agent
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

        self.base_domain = urlparse(self.start_url).netloc

        # State tracking
        self.visited_urls: Set[str] = set()
        self.queued_urls: Set[str] = {self.start_url}
        self.edges: List[Dict[str, str]] = []  # [{source, target, anchor, link_type}]
        self.broken_links: List[Dict[str, str]] = []  # [{source, target, status, anchor}]
        self.page_statuses: Dict[str, int] = {}
        self.crawl_summary: Dict = {}

    def is_link_contextual(self, tag) -> str:
        """Determine whether an anchor tag is inside main article content or sitewide chrome."""
        parent = tag.parent
        while parent and parent.name != "[document]":
            name = (parent.name or "").lower()
            classes = " ".join(parent.get("class", []))
            tag_id = parent.get("id", "")

            if name in ["header", "footer", "nav"] or "site-header" in classes or "site-footer" in classes or "main-navigation" in classes:
                return "sitewide"
            if name == "article" or "entry-content" in classes or "learning-system-box" in classes or "article-main" in classes:
                return "contextual"
            parent = parent.parent

        return "contextual"

    def parse_links_from_html(self, html: str, source_url: str) -> List[Tuple[str, str, str]]:
        """Extract valid, normalized internal links and anchor text from HTML string."""
        soup = BeautifulSoup(html, "html.parser")
        extracted = []

        for a_tag in soup.find_all("a", href=True):
            raw_href = a_tag["href"]
            anchor_text = a_tag.get_text(strip=True) or "[No Anchor Text]"
            link_type = self.is_link_contextual(a_tag)

            norm_url = normalize_url(raw_href, source_url)
            if not norm_url:
                continue

            if not is_internal_url(norm_url, self.base_domain):
                continue

            if not is_crawlable_html_resource(norm_url):
                continue

            extracted.append((norm_url, anchor_text, link_type))

        return extracted

    def crawl(self) -> Dict:
        """Execute the breadth-first internal crawl."""
        queue = deque([self.start_url])
        start_time = time.time()
        crawled_count = 0

        logger.info(f"Starting crawl at: {self.start_url} (Max pages: {self.max_pages})")

        while queue and crawled_count < self.max_pages:
            current_url = queue.popleft()

            if current_url in self.visited_urls:
                continue

            # Respect request politeness delay
            if self.request_delay > 0 and crawled_count > 0:
                time.sleep(self.request_delay)

            try:
                response = self.session.get(
                    current_url,
                    timeout=self.timeout,
                    allow_redirects=True,
                )
                status_code = response.status_code
                self.page_statuses[current_url] = status_code

                if status_code >= 400:
                    logger.warning(f"HTTP Error {status_code} on {current_url}")
                    self.visited_urls.add(current_url)
                    continue

                # Confirm content type is HTML
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    self.visited_urls.add(current_url)
                    continue

                html = response.text
                final_url = normalize_url(response.url)
                self.visited_urls.add(current_url)
                if final_url != current_url:
                    self.visited_urls.add(final_url)

                crawled_count += 1

                # Parse internal links
                links = self.parse_links_from_html(html, final_url)
                for target_url, anchor, link_type in links:
                    self.edges.append({
                        "source": final_url,
                        "target": target_url,
                        "anchor_text": anchor,
                        "link_type": link_type,
                    })

                    if target_url not in self.visited_urls and target_url not in self.queued_urls:
                        self.queued_urls.add(target_url)
                        queue.append(target_url)

            except requests.RequestException as exc:
                logger.error(f"Failed to fetch {current_url}: {exc}")
                self.page_statuses[current_url] = 0
                self.visited_urls.add(current_url)

        # Inspect broken links across all discovered edges
        for edge in self.edges:
            target = edge["target"]
            status = self.page_statuses.get(target)
            if status is not None and (status >= 400 or status == 0):
                self.broken_links.append({
                    "source_url": edge["source"],
                    "target_url": target,
                    "status_code": status,
                    "anchor_text": edge["anchor_text"],
                })

        elapsed_time = round(time.time() - start_time, 3)

        self.crawl_summary = {
            "start_url": self.start_url,
            "max_pages_limit": self.max_pages,
            "pages_crawled": crawled_count,
            "total_visited": len(self.visited_urls),
            "total_edges_found": len(self.edges),
            "broken_links_count": len(self.broken_links),
            "crawl_duration_seconds": elapsed_time,
        }

        return {
            "visited_urls": sorted(list(self.visited_urls)),
            "edges": self.edges,
            "broken_links": self.broken_links,
            "summary": self.crawl_summary,
            "page_statuses": self.page_statuses,
        }
