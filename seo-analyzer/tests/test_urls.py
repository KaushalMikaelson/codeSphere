"""Unit tests for URL normalization and domain classification."""

import pytest
from bs4 import BeautifulSoup
from seo_analyzer.urls import (
    classify_url_type,
    extract_canonical_url,
    is_crawlable_html_resource,
    is_internal_url,
    is_low_value_target,
    is_pagination_url,
    is_topic_hub,
    normalize_url,
)


def test_normalize_url_basic():
    base = "http://localhost/codesphere/"
    raw = "/programming/fundamentals/"
    norm = normalize_url(raw, base)
    assert norm == "http://localhost/codesphere/programming/fundamentals"


def test_normalize_url_strip_fragment():
    base = "http://localhost/codesphere"
    raw = "/dsa/trees#binary-search"
    norm = normalize_url(raw, base)
    assert norm == "http://localhost/codesphere/dsa/trees"


def test_normalize_url_strip_tracking_params():
    url = "http://localhost/codesphere/dsa?utm_source=twitter&utm_medium=cpc&page=2"
    norm = normalize_url(url)
    assert "utm_source" not in norm
    assert "utm_medium" not in norm
    assert "page=2" in norm


def test_normalize_url_invalid_schemes():
    assert normalize_url("javascript:void(0)") == ""
    assert normalize_url("mailto:info@codesphere.org") == ""
    assert normalize_url("tel:+123456789") == ""
    assert normalize_url("#top-of-page") == ""


def test_is_internal_url():
    base = "http://localhost/codesphere"
    assert is_internal_url("http://localhost/codesphere/dsa", base) is True
    assert is_internal_url("http://localhost/other-app", base) is True  # Same host
    assert is_internal_url("https://google.com/search", base) is False
    assert is_internal_url("https://external-resource.in/api", base) is False


def test_is_crawlable_html_resource():
    assert is_crawlable_html_resource("http://localhost/codesphere/dsa") is True
    assert is_crawlable_html_resource("http://localhost/codesphere/style.css") is False
    assert is_crawlable_html_resource("http://localhost/codesphere/script.js") is False
    assert is_crawlable_html_resource("http://localhost/codesphere/image.png") is False
    assert is_crawlable_html_resource("http://localhost/codesphere/wp-admin/index.php") is False
    assert is_crawlable_html_resource("http://localhost/codesphere/wp-login.php") is False


def test_extract_canonical_url():
    html = '<html><head><link rel="canonical" href="http://localhost/codesphere/canonical-page/" /></head></html>'
    soup = BeautifulSoup(html, "html.parser")
    canonical = extract_canonical_url(soup, "http://localhost/codesphere/current-page")
    assert canonical == "http://localhost/codesphere/canonical-page"


def test_normalize_url_subpage_base():
    """Verify that crawling subpages does not duplicate directory paths."""
    base = "http://localhost/codesphere/web-development"
    raw = "/web-development/html"
    norm = normalize_url(raw, base)
    assert norm == "http://localhost/codesphere/web-development/html"

    base_cs = "http://localhost/codesphere/computer-science"
    raw_cs = "/computer-science/sql"
    assert normalize_url(raw_cs, base_cs) == "http://localhost/codesphere/computer-science/sql"

    base_prog = "http://localhost/codesphere/programming-fundamentals"
    raw_prog = "/programming/variables-data-types"
    assert normalize_url(raw_prog, base_prog) == "http://localhost/codesphere/programming/variables-data-types"


def test_is_crawlable_html_resource_text_and_sitemap():
    assert is_crawlable_html_resource("http://localhost/codesphere/robots.txt") is False
    assert is_crawlable_html_resource("http://localhost/codesphere/sitemap.xml") is False
    assert is_crawlable_html_resource("http://localhost/codesphere/about") is True


def test_is_pagination_url():
    assert is_pagination_url("http://localhost/codesphere/category/dsa/page/2") is True
    assert is_pagination_url("http://localhost/codesphere/blog/page/10/") is True
    assert is_pagination_url("http://localhost/codesphere/category/dsa?page=2") is True
    assert is_pagination_url("http://localhost/codesphere/category/dsa?paged=3") is True
    assert is_pagination_url("http://localhost/codesphere/category/dsa") is False
    assert is_pagination_url("http://localhost/codesphere/binary-search-trees") is False


def test_is_low_value_target():
    # Paginated archives
    assert is_low_value_target("http://localhost/codesphere/category/dsa/page/2") is True
    assert is_low_value_target("http://localhost/codesphere/category/dsa?paged=2") is True
    # Uncategorized category / tag
    assert is_low_value_target("http://localhost/codesphere/category/uncategorized") is True
    assert is_low_value_target("http://localhost/codesphere/uncategorized") is True
    # Boilerplate / utility
    assert is_low_value_target("http://localhost/codesphere/hello-world") is True
    assert is_low_value_target("http://localhost/codesphere/sample-page") is True
    assert is_low_value_target("http://localhost/codesphere/privacy-policy") is True
    assert is_low_value_target("http://localhost/codesphere/author/admin") is True
    assert is_low_value_target("http://localhost/codesphere/2026/10/") is True

    # High-value educational destinations should NOT be flagged as low-value
    assert is_low_value_target("http://localhost/codesphere/category/dsa") is False
    assert is_low_value_target("http://localhost/codesphere/category/programming") is False
    assert is_low_value_target("http://localhost/codesphere/binary-trees") is False
    assert is_low_value_target("http://localhost/codesphere/recursion") is False
    assert is_low_value_target("http://localhost/codesphere/dsa-roadmap-for-placements") is False


def test_is_topic_hub():
    assert is_topic_hub("http://localhost/codesphere/category/dsa") is True
    assert is_topic_hub("http://localhost/codesphere/category/web-development") is True
    assert is_topic_hub("http://localhost/codesphere/programming-fundamentals") is True
    assert is_topic_hub("http://localhost/codesphere/dsa-roadmap-for-placements") is True

    # Low-value categories should not be topic hubs
    assert is_topic_hub("http://localhost/codesphere/category/uncategorized") is False
    assert is_topic_hub("http://localhost/codesphere/category/dsa/page/2") is False

    # Standard articles are not topic hubs
    assert is_topic_hub("http://localhost/codesphere/binary-search-trees") is False


def test_classify_url_type():
    assert classify_url_type("http://localhost/codesphere") == "homepage"
    assert classify_url_type("http://localhost/codesphere/category/dsa") == "topic_hub"
    assert classify_url_type("http://localhost/codesphere/category/dsa/page/2") == "archive_pagination"
    assert classify_url_type("http://localhost/codesphere/category/uncategorized") == "utility_archive"
    assert classify_url_type("http://localhost/codesphere/hello-world") == "utility_archive"
    assert classify_url_type("http://localhost/codesphere/binary-search-trees") == "educational_article"
    assert classify_url_type("http://localhost/codesphere/dynamic-programming") == "educational_article"


