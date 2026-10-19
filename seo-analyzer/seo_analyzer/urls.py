"""URL normalization, filtering, and canonicalization utilities."""

import re
from urllib.parse import urljoin, urlparse, urlunparse

IGNORED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico",
    ".css", ".js", ".map", ".json", ".xml", ".txt",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".woff", ".woff2", ".ttf", ".eot"
}

ADMIN_PATTERNS = [
    r"/wp-admin",
    r"/wp-login\.php",
    r"/wp-json",
    r"/feed/?$",
    r"/xmlrpc\.php",
    r"/trackback/?$",
    r"javascript:",
    r"mailto:",
    r"tel:"
]

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "msclkid", "ref", "source"
}

PAGINATION_PATTERNS = [
    r"/page/\d+(/|$)",
    r"[?&]paged?=\d+",
]

LOW_VALUE_PATTERNS = [
    r"/page/\d+(/|$)",
    r"[?&]paged?=\d+",
    r"/category/uncategorized(/|$)",
    r"/uncategorized(/|$)",
    r"/tag(/|$)",
    r"/author(/|$)",
    r"/users(/|$)",
    r"/\d{4}/\d{2}(/\d{2})?(/|$)",
    r"/hello-world(/|$)",
    r"/sample-page(/|$)",
    r"/privacy-policy(/|$)",
    r"/terms-of-service(/|$)",
    r"/cookie-policy(/|$)",
]


def normalize_url(raw_url: str, base_url: str = "") -> str:
    """Normalize a raw or relative URL to a standard canonical internal representation.
    
    1. Resolves relative paths using base_url.
    2. Strips fragments (#...).
    3. Lowercases scheme and network location.
    4. Strips tracking query parameters.
    5. Standardizes path (removes redundant slashes, trims trailing slash unless root).
    """
    if not raw_url:
        return ""

    raw_url = raw_url.strip()

    # Reject mailto, javascript, tel
    if any(raw_url.lower().startswith(p) for p in ["javascript:", "mailto:", "tel:", "#"]):
        return ""

    # Resolve relative URL against base if provided
    if base_url:
        base_parsed = urlparse(base_url)
        # Determine the application root prefix (e.g., "/codesphere" for "http://localhost/codesphere/...")
        base_segments = [seg for seg in base_parsed.path.split("/") if seg]
        app_root = f"/{base_segments[0]}" if base_segments else ""

        if app_root and raw_url.startswith("/"):
            if not raw_url.startswith(app_root + "/") and raw_url != app_root:
                raw_url = app_root + raw_url
        full_url = urljoin(base_url, raw_url)
    else:
        full_url = raw_url

    parsed = urlparse(full_url)
    if not parsed.scheme or not parsed.netloc:
        return ""

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Clean path
    path = parsed.path or "/"
    # Collapse multiple consecutive slashes
    path = re.sub(r"/+", "/", path)
    # Strip trailing slash if not root
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")

    # Filter query parameters
    query = ""
    if parsed.query:
        kept_pairs = []
        for pair in parsed.query.split("&"):
            if not pair:
                continue
            k = pair.split("=")[0].lower()
            if k not in TRACKING_PARAMS:
                kept_pairs.append(pair)
        if kept_pairs:
            query = "&".join(sorted(kept_pairs))

    # Reconstruct normalized URL without fragment
    normalized = urlunparse((scheme, netloc, path, "", query, ""))
    return normalized


def is_internal_url(url: str, base_domain: str) -> bool:
    """Check if the URL belongs to the internal target base domain."""
    if not url:
        return False
    parsed = urlparse(url)
    target_parsed = urlparse(base_domain) if "://" in base_domain else urlparse(f"http://{base_domain}")

    target_host = target_parsed.netloc.lower()
    current_host = parsed.netloc.lower()

    if not current_host:
        return False

    return current_host == target_host or current_host.endswith(f".{target_host}")


def is_crawlable_html_resource(url: str) -> bool:
    """Determine whether the URL targets a crawlable HTML page rather than an asset or admin endpoint."""
    if not url:
        return False

    parsed = urlparse(url)
    path = parsed.path.lower()

    # Check administrative patterns
    for pattern in ADMIN_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return False

    # Check file extensions
    for ext in IGNORED_EXTENSIONS:
        if path.endswith(ext):
            return False

    return True


def extract_canonical_url(soup, current_url: str) -> str:
    """Extract <link rel='canonical' href='...'> if present in HTML head."""
    if not soup:
        return current_url
    canonical_tag = soup.find("link", rel=lambda val: val and "canonical" in val.lower())
    if canonical_tag and canonical_tag.get("href"):
        return normalize_url(canonical_tag["href"], current_url)
    return current_url


def is_pagination_url(url: str) -> bool:
    """Determine whether the URL is a paginated listing (e.g. /page/2, ?paged=2)."""
    if not url:
        return False
    parsed = urlparse(url)
    path = parsed.path.lower()
    if re.search(r"/page/\d+(/|$)", path):
        return True
    if parsed.query and re.search(r"(^|[&?])paged?=\d+", parsed.query.lower()):
        return True
    return False


def is_low_value_target(url: str) -> bool:
    """Determine whether the URL is a low-value utility, pagination, or default archive."""
    if not url:
        return False
    parsed = urlparse(url)
    path = parsed.path.lower()
    full_str = f"{path}?{parsed.query}" if parsed.query else path

    for pattern in LOW_VALUE_PATTERNS:
        if re.search(pattern, full_str, re.IGNORECASE):
            return True
    return False


def is_topic_hub(url: str) -> bool:
    """Determine whether the URL is a primary category hub or curriculum pillar."""
    if not url or is_low_value_target(url):
        return False
    parsed = urlparse(url)
    path = parsed.path.lower().rstrip("/")
    if not path:
        return False
    if re.search(r"/category/[^/]+$", path):
        return True
    hub_indicators = ["-fundamentals", "-hub", "roadmap", "/topics/"]
    if any(ind in path for ind in hub_indicators):
        return True
    return False


def classify_url_type(url: str, root_url: str = "") -> str:
    """Classify URL into an SEO role: homepage, topic_hub, educational_article, archive_pagination, or utility_archive."""
    if not url:
        return "unknown"
    if root_url and normalize_url(url) == normalize_url(root_url):
        return "homepage"
    parsed = urlparse(url)
    path = parsed.path.lower().rstrip("/")
    if not path or path == "/codesphere":
        return "homepage"
    if is_pagination_url(url):
        return "archive_pagination"
    if is_low_value_target(url):
        return "utility_archive"
    if is_topic_hub(url):
        return "topic_hub"
    return "educational_article"

