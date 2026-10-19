"""Pytest fixtures and synthetic HTML mocks for crawler testing."""

import pytest


@pytest.fixture
def sample_homepage_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <title>CodeSphere - Home</title>
    <link rel="canonical" href="http://localhost/codesphere/" />
</head>
<body>
    <header class="site-header">
        <nav class="main-navigation">
            <a href="/codesphere/programming/">Programming</a>
            <a href="/codesphere/dsa/">DSA</a>
            <a href="https://external-site.com/docs">External Resource</a>
        </nav>
    </header>
    <main class="site-content">
        <article class="entry-content">
            <h1>Welcome to CodeSphere</h1>
            <p>Read about <a href="/codesphere/dsa/trees/">Tree Data Structures</a> in depth.</p>
            <p>Check out our <a href="/codesphere/broken-link">Broken Topic</a>.</p>
        </article>
    </main>
    <footer class="site-footer">
        <a href="/codesphere/about/">About</a>
    </footer>
</body>
</html>"""


@pytest.fixture
def sample_article_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Binary Trees - CodeSphere</title>
</head>
<body>
    <main>
        <article class="entry-content">
            <h1>Binary Trees</h1>
            <p>Requires understanding <a href="/codesphere/dsa/algorithms/recursion">Recursion</a>.</p>
            <p>Next topic is <a href="/codesphere/dsa/trees/tree-traversal">Tree Traversal</a>.</p>
        </article>
    </main>
</body>
</html>"""
