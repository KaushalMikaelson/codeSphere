# CodeSphere: Prioritized Action Plan & Remaining Work

**Auditor:** Strict Project Auditor & Academic Evaluator  
**Document Purpose:** Clear roadmap to achieve 40/40 marks across Milestone I and Milestone II.  

---

## 1. Priority P0 — Critical Tasks (High Mark Impact / Currently Blocked)

### Task P0-1: Obtain Designated External Backlink Domains & Execute Outreach
* **Rubric Item:** Milestone II, Criterion 4 — *Backlinks on designated external domains (3 Marks)*
* **Current Status:** **BLOCKED** (Awaiting instructor/institutional list of designated external domains)
* **Expected Outcome:** 3–5 live external backlinks pointing to CodeSphere articles with keyword-rich, non-spam anchor text on approved external platforms.
* **Exact Implementation Steps:**
  1. Retrieve the list of designated external domains from your course instructor or syllabus guidelines.
  2. For each target domain, select a relevant topic from CodeSphere:
     - Anchor: `binary tree vs binary search tree` pointing to `/blog/binary-tree-vs-binary-search-tree/`
     - Anchor: `DSA roadmap for placements` pointing to `/blog/dsa-roadmap-for-placements/`
     - Anchor: `how do REST APIs work` pointing to `/web-development/rest-apis/`
  3. Draft an educational context article (300–500 words) referencing CodeSphere as an authoritative curriculum source.
  4. Publish/submit to the designated platforms and confirm the link is `dofollow` and crawlable.
* **Relevant Files/Services:** Target external domains, [`keyword-page-map.csv`](file:///e:/Projects/codeSphere/docs/seo/keyword-page-map.csv).
* **How to Test:** Run `curl -IL <backlink-url>` and inspect HTML to ensure `rel="nofollow"` is absent and link resolves HTTP 200.
* **Evidence to Capture:**
  - Full URLs of the published external posts.
  - Screenshots of the backlink live in the page context.
  - Page source screenshot highlighting `<a href="https://codesphere.../page/">Anchor</a>`.

---

### Task P0-2: VPS Provisioning, Cloudflare DNS & Live WordPress Deployment
* **Rubric Item:** Milestone I, Criterion 5 — *VPS setup, Cloudflare DNS, SSL, and functional WordPress deployment (4 Marks)*
* **Current Status:** **PARTIAL** (Configuration scripts and Nginx server blocks written, live server pending)
* **Expected Outcome:** A publicly reachable HTTPS website running on an Ubuntu 24.04 VPS behind Cloudflare CDN with Full (Strict) SSL.
* **Exact Implementation Steps:**
  1. Spin up an Ubuntu 24.04 LTS VPS instance (DigitalOcean Droplet, AWS EC2, Hetzner, or Linode).
  2. Point your custom domain's nameservers to Cloudflare.
  3. In Cloudflare DNS, add an `A` record pointing `@` and `www` (or your subdomain) to the VPS IP address with Proxy (Orange cloud) enabled.
  4. Follow [`docs/deployment/ubuntu-nginx.md`](file:///e:/Projects/codeSphere/docs/deployment/ubuntu-nginx.md):
     - Install Nginx, MariaDB, and PHP 8.3-FPM.
     - Deploy WordPress to `/var/www/codesphere`.
     - Copy `wordpress/wp-content/themes/codesphere` and `plugins/codesphere-learning-links`.
     - Issue SSL certificate via Certbot: `sudo certbot --nginx -d yourdomain.edu`.
     - Set Cloudflare SSL/TLS to **Full (strict)**.
  5. In WP Admin, set Permalinks to **Post name**, activate theme and plugin, and run **Tools > Import > WordPress** with [`codesphere-content.xml`](file:///e:/Projects/codeSphere/wordpress/content-import/codesphere-content.xml).
* **Relevant Files/Services:** Cloudflare Dashboard, Ubuntu VPS terminal, [`ubuntu-nginx.md`](file:///e:/Projects/codeSphere/docs/deployment/ubuntu-nginx.md), [`codesphere-content.xml`](file:///e:/Projects/codeSphere/wordpress/content-import/codesphere-content.xml).
* **How to Test:**
  - `curl -I https://yourdomain.edu` (Must return HTTP 200, HTTP/2, and valid SSL).
  - Check browser padlock and Cloudflare Ray ID header.
* **Evidence to Capture:**
  - Screenshot of Cloudflare DNS records table.
  - Screenshot of Cloudflare SSL/TLS Overview set to **Full (strict)**.
  - Browser screenshot of live homepage with HTTPS green padlock.
  - Screenshot of WordPress Admin showing 32 published posts.

---

### Task P0-3: Google Search Console (GSC) & GA4 Setup and Verification
* **Rubric Item:** Milestone II, Criterion 5 — *Google Search Console and GA4 setup and reporting (3 Marks)*
* **Current Status:** **BLOCKED / PENDING LIVE DOMAIN**
* **Expected Outcome:** Verified GSC domain property collecting real impressions and GA4 data stream tracking live visitors.
* **Exact Implementation Steps:**
  1. Once the public domain is live, go to [Google Search Console](https://search.google.com/search-console).
  2. Add your domain property and verify via Cloudflare DNS TXT record.
  3. Submit the sitemap: `https://yourdomain.edu/sitemap.xml`.
  4. In [Google Analytics 4](https://analytics.google.com/), create property "CodeSphere" and obtain Measurement ID (`G-XXXXXXXXXX`).
  5. Inject GA4 script into WordPress `<head>` via custom plugin or theme `header.php`.
* **Relevant Files/Services:** GSC Dashboard, GA4 Dashboard, Cloudflare DNS, [`header.php`](file:///e:/Projects/codeSphere/wordpress/wp-content/themes/codesphere/header.php).
* **How to Test:** Visit live site from smartphone and open GA4 Realtime dashboard to verify active user tracking. In GSC, check sitemap index status returns "Success".
* **Evidence to Capture:**
  - Screenshot of GSC Ownership Verification modal ("Ownership auto-verified").
  - Screenshot of GSC Sitemaps panel showing `sitemap.xml` with "Success" status and discovered URL count.
  - Screenshot of GA4 Realtime overview showing active sessions.

---

### Task P0-4: Generate Real Restorable UpdraftPlus Backup ZIP
* **Rubric Item:** Milestone II, Criterion 7 — *Final report, UpdraftPlus backup ZIP, and viva defense (2 Marks)*
* **Current Status:** **PARTIAL** (Documentation ready, live backup file pending)
* **Expected Outcome:** A restorable `.zip` backup package generated by UpdraftPlus stored in `data/backups/`.
* **Exact Implementation Steps:**
  1. In the live WordPress admin, install and activate the free **UpdraftPlus** plugin.
  2. Go to **Settings > UpdraftPlus Backups** and click **Backup Now**.
  3. Check: *Include database*, *Include files (plugins, themes, uploads)*.
  4. Download the resulting backup ZIP components (database, themes, plugins, uploads).
  5. Archive into `data/backups/codesphere-updraftplus-backup.zip`.
* **Relevant Files/Services:** UpdraftPlus Plugin, `data/backups/`.
* **How to Test:** Test restore on local XAMPP using UpdraftPlus "Restore" function.
* **Evidence to Capture:**
  - Screenshot of UpdraftPlus "Existing Backups" table with timestamp.
  - File path verification: `data/backups/codesphere-updraftplus-backup.zip`.

---

## 2. Priority P1 — Important Tasks (Grade Differentiation)

### Task P1-1: Populate Genuine Google Keyword Planner Volume & LSI Data
* **Rubric Item:** Milestone I, Criterion 2 — *Keyword research, LSI keywords, and search-intent mapping (4 Marks)*
* **Expected Outcome:** [`keyword-page-map.csv`](file:///e:/Projects/codeSphere/docs/seo/keyword-page-map.csv) populated with real Indian monthly search volumes and 3–5 LSI keywords per primary seed.
* **Exact Implementation Steps:**
  1. Open Google Keyword Planner (India location, English language).
  2. Enter the 10 target seeds from our plan.
  3. Download official CSV and place in `docs/seo/raw/gkp-india-export-2026.csv`.
  4. Update `keyword-page-map.csv` replacing "Pending Research" with genuine numerical volumes and LSI terms.
* **Evidence to Capture:** GKP dashboard screenshot and exported raw CSV.

---

### Task P1-2: Capture Competitor SERP Breakdown & Screenshots
* **Rubric Item:** Milestone I, Criterion 3 — *Competitor analysis and SERP breakdown (3 Marks)*
* **Expected Outcome:** Populated table in [`competitor-analysis-template.md`](file:///e:/Projects/codeSphere/docs/seo/competitor-analysis-template.md) showing top-3 ranking pages for core seeds.
* **Exact Implementation Steps:**
  1. Open an incognito browser tab.
  2. Search: `difference between sql and nosql`, `binary tree vs binary search tree`, `dynamic programming for beginners`.
  3. Note title tags, meta descriptions, word counts, and heading structure of top 3 ranking results.
  4. Take full-page SERP screenshots and save in `docs/seo/serp-screenshots/`.
* **Evidence to Capture:** 3 SERP screenshots and updated competitor comparison table.

---

### Task P1-3: Run Live Google PageSpeed Insights & Core Web Vitals Benchmark
* **Rubric Item:** Milestone II, Criterion 2 — *Speed optimization, Core Web Vitals, and caching (3 Marks)*
* **Expected Outcome:** Public PageSpeed score showing Performance $\ge 90$ on Desktop and $\ge 80$ on Mobile.
* **Exact Implementation Steps:**
  1. Visit [PageSpeed Insights](https://pagespeed.web.dev/).
  2. Enter live URL: `https://yourdomain.edu/dsa/trees/binary-trees/`.
  3. Record FCP (First Contentful Paint), LCP (Largest Contentful Paint), CLS (Cumulative Layout Shift).
* **Evidence to Capture:** Full PDF export or high-resolution screenshot of PSI result page.

---

### Task P1-4: Validate Schema.org Markup on Google Rich Results Test
* **Rubric Item:** Milestone II, Criterion 1 — *Technical/on-page SEO and schema markup (4 Marks)*
* **Expected Outcome:** Zero errors / warnings on `TechArticle` and `BreadcrumbList` schemas.
* **Exact Implementation Steps:**
  1. Visit [Google Rich Results Test](https://search.google.com/test/rich-results).
  2. Enter live article URL.
  3. Verify structured data detected: *Breadcrumbs* and *Article*.
* **Evidence to Capture:** Screenshot of "Page is eligible for rich results" status.

---

### Task P1-5: Compile Submission Reports for Milestones I & II
* **Rubric Item:** Milestone I & II — *Reports and Viva Defense (5 Marks total)*
* **Expected Outcome:** Formatted academic report PDFs summarizing research, cloud architecture, crawl results, and delta comparisons.
* **Exact Implementation Steps:**
  1. Export [`README.md`](file:///e:/Projects/codeSphere/README.md), [`academic-methodology.md`](file:///e:/Projects/codeSphere/docs/research/academic-methodology.md), and [`experiment-findings-report.md`](file:///e:/Projects/codeSphere/docs/research/experiment-findings-report.md) to clean PDF format.
  2. Prepare 10-slide PowerPoint viva presentation covering the central research question, graph topology, and 70.6% dead-end reduction.

---

## 3. Priority P2 — Optional Enhancements (Technical Polish)

| Task | Scope | Benefit | Action |
|---|---|---|---|
| **P2-1: Gephi Network Visualization High-Res Image** | Graph Visualization | Impressive visual artifact for viva slides | Open [`data/final/graph.gexf`](file:///e:/Projects/codeSphere/data/final/graph.gexf) in Gephi, apply ForceAtlas2 layout, export 300 DPI PNG. |
| **P2-2: Screaming Frog Crawl Cross-Validation** | SEO Auditing | Independent validation of Python crawler | Run free Screaming Frog (up to 500 URLs) on live domain; verify 0 orphan pages matches Python output. |
| **P2-3: Dark Mode Header Toggle** | Front-End Polish | User experience enhancement | Add lightweight JS toggle for switching between light and dark CSS tokens in `style.css`. |
