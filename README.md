# CodeSphere — SEO-Driven Computer Science Knowledge Base & Internal Link Graph Analyzer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![WordPress 6.x](https://img.shields.io/badge/WordPress-6.x-21759b.svg)](https://wordpress.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Complete](https://img.shields.io/badge/Status-Fully%20Implemented-brightgreen.svg)]()

> **Academic Research Focus:** *“Can a deliberately designed internal-link structure improve page discoverability, reduce click depth, eliminate orphan pages, and improve connectivity between related learning topics?”*

---

## 1. Executive Summary & Project Purpose

**CodeSphere** is an interconnected computer science knowledge base designed specifically for undergraduate CS students and engineering aspirants in India. It serves two distinct but tightly integrated objectives:

1. **A Crawlable, Highly Optimized WordPress Educational Hub:**
   Organized into four structured topic clusters (*Programming*, *Data Structures & Algorithms*, *Web Development*, and *Core Computer Science*) plus foundational roadmaps and career guides. Built with an accessible, high-performance custom WordPress theme (`codesphere`) and an educational semantic link plugin (`codesphere-learning-links`).

2. **A Reproducible Python-Based Internal-Link Graph Analyzer:**
   A standalone research and auditing package (`seo-analyzer`) utilizing `requests`, `BeautifulSoup4`, `pandas`, and `NetworkX`. It models website topology as a directed graph $G = (V, E)$, computes crawl depths, PageRank ($\alpha = 0.85$), orphan URLs, dead ends, and cluster connectivity, and benchmarks structural changes across a rigorous before-and-after experiment of 20+ link updates across 10+ pages.

### Crucial Academic & Professional Disclaimer
* **Internal PageRank is not Google’s Ranking Algorithm:** While PageRank was invented by Larry Page and Sergey Brin at Stanford, Google’s live production search ranking uses hundreds of proprietary signals (RankBrain, MUM, BERT, User Engagement, Helpful Content signals, SpamBrain, EEAT). Internal PageRank in this project is an objective measure of relative link equity flow within our directed graph.
* **No Ranking Guarantees:** Deliberate internal linking improves crawl efficiency, information hierarchy, and user navigation, but organic Google search rankings depend on indexation, competition, search intent, domain history, and external authority.

---

## 2. System Architecture

```
+--------------------------------------------------------------------------------+
|                                  CodeSphere Hub                                |
+--------------------------------------------------------------------------------+
|  Frontend: Semantic HTML5, CSS3 Custom Tokens, Accessible Micro-interactions   |
|  CMS: WordPress 6.x (MariaDB + PHP 8.x + Apache/Nginx + Yoast/RankMath Support)|
|  Custom Theme: `codesphere` (Breadcrumbs, Auto-TOC, Hub Maps, Rich Badges)    |
|  Plugin: `codesphere-learning-links` (Prerequisites, Next Topics, Schema)      |
+--------------------------------------------------------------------------------+
                                       |
                   HTTP GET / HTML Responses (Crawlable)
                                       v
+--------------------------------------------------------------------------------+
|                         Python SEO Analyzer & Graph Engine                     |
+--------------------------------------------------------------------------------+
|  1. Crawler & Normalizer: Canonical URL resolver, polite delays, robots.txt    |
|  2. Graph Engine (NetworkX): In/Out-degree, Shortest Path Depth, PageRank      |
|  3. Auditing & Diagnostics: Orphan detection, Dead-end detection, Broken links  |
|  4. Recommendation Engine: Structural deficit flags & anchor text advisory    |
|  5. Comparative Engine: Delta reporting between Baseline and Final topology    |
|  6. Visualization Exporters: CSV datasets & Gephi Graph Exchange (.gexf)       |
+--------------------------------------------------------------------------------+
```

---

## 3. Repository Structure

```
codesphere/
├── README.md                           <- Comprehensive system documentation
├── PROJECT_STATUS.md                   <- Milestone tracking & audit status
├── .gitignore                          <- Git ignore rules for dev & Python caches
├── wordpress/                          <- WordPress Theme & Custom Engineering
│   ├── wp-content/
│   │   ├── themes/
│   │   │   └── codesphere/             <- Custom lightweight, responsive SEO theme
│   │   │       ├── style.css           <- Theme declaration and design tokens
│   │   │       ├── index.php           <- Fallback template
│   │   │       ├── header.php          <- Semantic header, primary navigation, breadcrumbs hook
│   │   │       ├── footer.php          <- Cluster hub footer & accessibility links
│   │   │       ├── functions.php       <- Theme setup, assets, custom menus, SEO hooks
│   │   │       ├── single.php          <- Article layout (TOC, content, learning links)
│   │   │       ├── page.php            <- Generic & hub page template
│   │   │       ├── archive.php         <- Category/Cluster hub template
│   │   │       ├── template-parts/     <- Modular components (TOC, Breadcrumbs, etc.)
│   │   │       └── assets/             <- CSS design system and Vanilla JS
│   │   └── plugins/
│   │       └── codesphere-learning-links/
│   │           ├── codesphere-learning-links.php <- Core plugin entry
│   │           └── includes/           <- Meta boxes, shortcodes, Course/Article Schema
│   └── content-import/
│       ├── codesphere-content.xml      <- Complete 32-article WordPress WXR import file
│       └── import-helper.php           <- Script for automated content provisioning
├── seo-analyzer/                       <- Python Internal Link Graph Engine
│   ├── pyproject.toml                  <- Build system specification
│   ├── requirements.txt                <- Pin dependencies (requests, bs4, networkx, pandas)
│   ├── seo_analyzer/                   <- Python source module
│   │   ├── __init__.py                 <- Package metadata
│   │   ├── cli.py                      <- Command-line interface (`python -m seo_analyzer`)
│   │   ├── urls.py                     <- URL normalization, canonicalization, domain filtering
│   │   ├── crawler.py                  <- BFS/DFS internal link crawler with polite delay
│   │   ├── graph_analysis.py           <- NetworkX topology, PageRank, depth, orphans
│   │   ├── recommendations.py          <- Rule-based internal linking optimization engine
│   │   └── comparison.py               <- Baseline vs. Final delta generator
│   └── tests/                          <- Automated test suite
│       ├── conftest.py                 <- Test fixtures & synthetic server emulation
│       ├── fixtures/                   <- HTML synthetic website snapshots
│       ├── test_urls.py                <- Normalization and resolution tests
│       ├── test_crawler.py             <- Crawler boundary, status code & limit tests
│       ├── test_graph_analysis.py      <- NetworkX calculations & orphan tests
│       ├── test_recommendations.py     <- Recommendation rule validation
│       └── test_comparison.py          <- Before-and-after delta tests
├── data/                               <- Research Datasets & Graph Exports
│   ├── url_inventory.txt               <- Official inventory of published pages (32 URLs)
│   ├── link_changes.csv                <- 20+ documented internal link modifications
│   ├── baseline/                       <- Pre-experiment crawl outputs
│   │   ├── crawl_summary.json
│   │   ├── edges.csv
│   │   ├── metrics.csv
│   │   ├── orphan_pages.csv
│   │   ├── broken_links.csv
│   │   └── graph.gexf
│   ├── final/                          <- Post-experiment crawl outputs
│   │   ├── crawl_summary.json
│   │   ├── edges.csv
│   │   ├── metrics.csv
│   │   ├── orphan_pages.csv
│   │   ├── broken_links.csv
│   │   └── graph.gexf
│   └── comparison.csv                  <- Computed structural metrics comparison
├── docs/                               <- Documentation & Academic Reporting
│   ├── seo/
│   │   ├── keyword-page-map.csv        <- 1:1 Target keyword to page mapping
│   │   ├── search-intent-matrix.csv    <- Intent categorization & funnel stage
│   │   ├── competitor-analysis-template.md <- Academic competitor auditing framework
│   │   ├── content-gap-analysis.md     <- Identified curriculum & topic opportunities
│   │   └── technical-seo-audit-checklist.md <- Comprehensive 25-point audit checklist
│   ├── deployment/
│   │   ├── ubuntu-nginx.md             <- Ubuntu 24.04 LTS + Nginx + PHP-FPM production guide
│   │   └── xampp-windows-setup.md      <- Step-by-step local Windows/XAMPP environment setup
│   └── research/
│       ├── academic-methodology.md     <- Viva defense guide & research methodology
│       └── experiment-findings-report.md <- Analysis of before-and-after graph improvements
└── scripts/                            <- Automation Scripts
    ├── run_analyzer.py                 <- Direct launcher for baseline & final analysis
    └── verify_experiment.py            <- Self-contained validation runner
```

---

## 4. Topic Clusters & URL Architecture

All content is structured into four logical clusters using clean, date-free, hyphen-separated permalinks:

| Cluster | Hub URL | Sample Child URLs |
|---|---|---|
| **Programming** | `/programming/` | `/programming/programming-fundamentals/`, `/programming/variables-data-types/`, `/programming/control-flow/`, `/programming/functions/`, `/programming/object-oriented-programming/` |
| **Data Structures & Algorithms** | `/dsa/` | `/dsa/data-structures/`, `/dsa/arrays/`, `/dsa/linked-lists/`, `/dsa/stacks-and-queues/`, `/dsa/trees/`, `/dsa/trees/binary-trees/`, `/dsa/trees/binary-search-trees/`, `/dsa/trees/tree-traversal/`, `/dsa/algorithms/recursion/`, `/dsa/algorithms/dynamic-programming/`, `/dsa/algorithms/searching-sorting/`, `/dsa/algorithms/graph-algorithms/` |
| **Web Development** | `/web-development/` | `/web-development/html/`, `/web-development/css/`, `/web-development/javascript/`, `/web-development/rest-apis/`, `/web-development/backend-fundamentals/` |
| **Core Computer Science** | `/computer-science/` | `/computer-science/databases/`, `/computer-science/sql/`, `/computer-science/nosql/`, `/computer-science/computer-networks/`, `/computer-science/operating-systems/` |
| **Guides & Comparative** | `/blog/` | `/blog/binary-tree-vs-binary-search-tree/`, `/blog/dsa-roadmap-for-placements/` |
| **System Pages** | Root | `/` (Home), `/about/`, `/search/` |

---

## 5. Quick Start: Local Setup

### 5.1 Local WordPress Setup (Windows / XAMPP)
1. Install [XAMPP](https://www.apachefriends.org/) on Windows and start **Apache** and **MySQL**.
2. Download official [WordPress](https://wordpress.org/download/) and extract to `C:\xampp\htdocs\codesphere`.
3. Create a database in phpMyAdmin: `codesphere_db`.
4. Copy `wordpress/wp-content/themes/codesphere` into `C:\xampp\htdocs\codesphere\wp-content\themes\`.
5. Copy `wordpress/wp-content/plugins/codesphere-learning-links` into `C:\xampp\htdocs\codesphere\wp-content\plugins\`.
6. Access `http://localhost/codesphere/` in your browser and complete standard WordPress 5-minute setup.
7. Go to **Settings > Permalinks** and choose **Post name** (`/%postname%/`).
8. Go to **Appearance > Themes** and activate **CodeSphere**.
9. Go to **Plugins** and activate **CodeSphere Learning Links**.
10. Go to **Tools > Import > WordPress** and upload `wordpress/content-import/codesphere-content.xml` to populate all 32 articles immediately!

### 5.2 Python SEO Analyzer Setup
1. Open PowerShell / Command Prompt and navigate to the project directory:
   ```powershell
   cd e:\Projects\codeSphere\seo-analyzer
   ```
2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the automated test suite:
   ```powershell
   pytest -v
   ```

---

## 6. How to Run the Crawl & Internal Link Experiment

### Step 1: Run Baseline Crawl
```powershell
python -m seo_analyzer crawl --start-url http://localhost/codesphere/ --inventory ../data/url_inventory.txt --output-dir ../data/baseline --max-pages 100
```
This crawls the site, evaluates current graph topology, identifies orphan URLs, calculates initial click depth, and saves `data/baseline/metrics.csv` and `graph.gexf`.

### Step 2: Implement Deliberate Link Improvements
Review `data/link_changes.csv`. In WordPress, apply the 20 planned contextual link additions across the 10 target articles (e.g., connecting Recursion $\to$ Dynamic Programming, Binary Trees $\to$ Tree Traversal, REST APIs $\to$ Computer Networks, and resolving orphan guides).

### Step 3: Run Final Crawl
```powershell
python -m seo_analyzer crawl --start-url http://localhost/codesphere/ --inventory ../data/url_inventory.txt --output-dir ../data/final --max-pages 100
```

### Step 4: Compare Baseline vs. Final
```powershell
python -m seo_analyzer compare --baseline ../data/baseline/metrics.csv --final ../data/final/metrics.csv --output ../data/comparison.csv
```

### Step 5: Generate Actionable Recommendations
```powershell
python -m seo_analyzer recommend --edges ../data/final/edges.csv --metrics ../data/final/metrics.csv --output ../data/recommendations.csv
```

---

## 7. Automated Test Suite

The Python analyzer includes comprehensive unit and integration tests using synthetic HTML fixtures (no active network required):
* `test_urls.py`: URL canonicalization, trailing slash standardization, fragment removal, query stripping, and internal vs external domain checks.
* `test_crawler.py`: Polite BFS crawl behavior, response status handling (200, 301, 404, 500), broken link tracking, max-page cap enforcement, and exclusion of `/wp-admin/` or `#` hashes.
* `test_graph_analysis.py`: In-degree, out-degree, shortest path depth from root, PageRank sum convergence, dead-end detection, and orphan URL identification against official inventory.
* `test_recommendations.py`: Discovery of deep pages (depth > 3), weak in-degree links (in-degree $\le$ 1), and missing reciprocal cluster connections.
* `test_comparison.py`: Accurate calculation of net changes, percentage improvements in depth, and orphan elimination.

Run all tests:
```powershell
cd seo-analyzer
pytest --tb=short
```

---

## 8. Viva & Interview Defense Notes

When presenting this project to evaluators:
1. **Differentiate Crawl Depth from URL Path Depth:** A page at `/dsa/trees/binary-trees/` has a URL path depth of 3, but if linked directly from the homepage, its crawl/click depth is **1**. Search engine crawlers navigate links, not directory slashes.
2. **Explain Orphan Resolution:** An orphan page exists in the published inventory but has an in-degree of 0. Search bots relying on traversal will never discover or re-crawl it without an XML sitemap or contextual inbound link.
3. **Address PageRank Conservation:** The damping factor $\alpha = 0.85$ models a user following links 85% of the time and jumping to a random page 15% of the time. Adding bidirectional links between relevant topics concentrates link equity in authoritative learning hubs.
4. **Why Not Automate Link Insertion:** Educational context matters. Algorithmic link spam dilutes relevance and hurts user experience. All links must use descriptive anchor text matching search intent.
