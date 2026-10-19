"""Unit and integration tests for internal link crawler."""

from unittest.mock import MagicMock, patch
import pytest
import requests
from seo_analyzer.crawler import InternalLinkCrawler


def test_parse_links_from_html(sample_homepage_html):
    crawler = InternalLinkCrawler(start_url="http://localhost/codesphere", max_pages=10)
    links = crawler.parse_links_from_html(sample_homepage_html, "http://localhost/codesphere")

    # Should extract internal links: /programming, /dsa, /dsa/trees, /broken-link, /about
    # External link (https://external-site.com) should be ignored
    targets = [link[0] for link in links]
    assert "http://localhost/codesphere/programming" in targets
    assert "http://localhost/codesphere/dsa" in targets
    assert "http://localhost/codesphere/dsa/trees" in targets
    assert "https://external-site.com/docs" not in targets


def test_is_link_contextual(sample_homepage_html):
    crawler = InternalLinkCrawler(start_url="http://localhost/codesphere")
    links = crawler.parse_links_from_html(sample_homepage_html, "http://localhost/codesphere")

    for target, anchor, link_type in links:
        if "trees" in target:
            assert link_type == "contextual"  # Inside <article>
        elif "programming" in target:
            assert link_type == "sitewide"   # Inside <nav>
        elif "about" in target:
            assert link_type == "sitewide"   # Inside <footer>


def test_crawler_max_pages_enforcement():
    # Mock requests session to simulate recursive internal links
    mock_session = MagicMock()

    def mock_get(url, *args, **kwargs):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "text/html; charset=utf-8"}
        mock_resp.url = url
        # Each page links to the next numbered page
        curr_num = int(url.split("/")[-1]) if url.split("/")[-1].isdigit() else 0
        next_num = curr_num + 1
        mock_resp.text = f'<html><body><a href="http://localhost/page/{next_num}">Next</a></body></html>'
        return mock_resp

    mock_session.get.side_effect = mock_get

    crawler = InternalLinkCrawler(
        start_url="http://localhost/page/0",
        max_pages=5,
        request_delay=0.0,
        session=mock_session
    )

    result = crawler.crawl()
    assert result["summary"]["pages_crawled"] == 5
    assert len(result["visited_urls"]) == 5


def test_crawler_broken_links_detection():
    mock_session = MagicMock()

    def mock_get(url, *args, **kwargs):
        mock_resp = MagicMock()
        if "broken-page" in url:
            mock_resp.status_code = 404
            mock_resp.text = "Not Found"
        else:
            mock_resp.status_code = 200
            mock_resp.headers = {"Content-Type": "text/html"}
            mock_resp.url = url
            mock_resp.text = '<html><body><a href="http://localhost/broken-page">Broken Link Anchor</a></body></html>'
        return mock_resp

    mock_session.get.side_effect = mock_get

    crawler = InternalLinkCrawler(
        start_url="http://localhost/valid-page",
        max_pages=10,
        request_delay=0.0,
        session=mock_session
    )

    result = crawler.crawl()
    assert len(result["broken_links"]) == 1
    assert result["broken_links"][0]["status_code"] == 404
    assert result["broken_links"][0]["anchor_text"] == "Broken Link Anchor"
