# SHOUG.TECH

**SHOUG.TECH** is my personal technical portfolio and knowledge platform, built to document and showcase my work across **software engineering, cybersecurity, academic resources, workshops, and applied projects**.

The platform serves as both a professional portfolio and a structured technical knowledge base, bringing together projects, coursework, security labs, documentation, study resources, and professional development in one place.

## About

I’m **Shoug Fawaz Alomran**, a Software Engineering and Cybersecurity student focused on building, analyzing, securing, and documenting technical systems.

My primary areas of interest include:

- **Software Engineering** — designing and developing structured, maintainable software systems
- **Cybersecurity** — developing practical skills in penetration testing, security analysis, and defensive awareness
- **Technical Documentation** — transforming complex academic and technical material into structured, accessible resources
- **Knowledge Systems** — building platforms and workflows that organize learning, projects, and technical information
- **Technical Workshops** — creating and delivering practical learning experiences around development and technology

SHOUG.TECH documents that work through real projects, academic material, technical resources, workshops, and continuously evolving documentation.

## Live Site

- [SHOUG.TECH](https://shoug-tech.com/)
- [Site map for AI assistants](https://shoug-tech.com/llms.txt)

## Tech Stack

- **Python 3**
- **HTML**
- **CSS**
- **JavaScript**
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n)
- **Firebase Authentication**
- **Firebase**
- **Firebase Hosting** (main site, since November 2026)
- **GitHub Actions**
- **GitHub Pages** (project subdomains only)
- **Cloudflare** (DNS, `www` redirect, email routing and Workers)

## Repository Structure

```text
.
├── docs/
│   ├── academics/
│   ├── projects/
│   ├── workshops/
│   ├── resources/
│   ├── assets/
│   └── *.ar.md
│
├── scripts/
│   ├── check_i18n_parity.py
│   ├── sync_arabic.py
│   └── preflight_qa.sh
│
├── .github/
│   └── workflows/
│       └── deploy-mkdocs.yml
│
├── mkdocs.yml
└── site/
```

### Key Files

- `docs/` — website content, academic resources, projects, assets, custom styling, scripts, and Arabic pages
- `mkdocs.yml` — navigation, theme configuration, plugins, extensions, and internationalization settings
- `scripts/` — validation, localization, synchronization, and pre-release QA utilities
- `.github/workflows/deploy-mkdocs.yml` — automated build and deployment workflow
- `site/` — generated MkDocs output

## Platform Sections

### Academics

Structured academic resources covering university coursework in areas including:

- Software Engineering
- Cybersecurity
- Computer Science
- Mathematics
- Supporting university courses

Course resources may include:

- Slide breakdowns
- Chapter summaries
- Mind maps
- Practice exams
- Revision material
- Study guides
- Reference resources

### Work

A professional overview of my technical work, including:

- Software projects
- Cybersecurity work
- Technical platforms
- Development experience
- Professional and academic contributions

### Workshops

Documentation and supporting resources for technical workshops I have developed or delivered.

### Resources

A curated technical directory containing tools, references, learning platforms, development resources, cybersecurity material, and other useful links.

### About

Background information, professional interests, technical focus areas, policies, and site information.

## Local Development

Clone the repository:

```bash
git clone https://github.com/Shoug-Alomran/shoug-tech.git
cd shoug-tech
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install --upgrade pip
pip install mkdocs-material mkdocs-static-i18n
```

Start the local development server:

```bash
mkdocs serve
```

The local site will typically be available at:

```text
http://127.0.0.1:8000/
```

## Bilingual Architecture

SHOUG.TECH supports both **English and Arabic** content using `mkdocs-static-i18n`.

Arabic pages follow the naming convention:

```text
page.md
page.ar.md
```

Several internal utilities help maintain synchronization between both versions.

### EN/AR Parity Check

Run:

```bash
python3 scripts/check_i18n_parity.py
```

Strict validation:

```bash
python3 scripts/check_i18n_parity.py --strict
```

Automatically create placeholders for missing Arabic pages:

```bash
python3 scripts/check_i18n_parity.py --autofix-missing-ar
```

## Arabic Synchronization Utility

`scripts/sync_arabic.py` assists with synchronizing English content into formal, Saudi-friendly Arabic while preserving Markdown structure.

Dry run:

```bash
python3 scripts/sync_arabic.py
```

Create missing Arabic files:

```bash
OPENAI_API_KEY=your_key python3 scripts/sync_arabic.py --apply
```

Update existing Arabic files when their corresponding English content changes:

```bash
OPENAI_API_KEY=your_key python3 scripts/sync_arabic.py --apply --update-existing
```

Additional options include:

```text
--backup
```

Creates a `.bak` file before overwriting existing content.

```text
--limit N
```

Processes only the first `N` files.

```text
--force
```

Ignores the translation hash cache and forces regeneration.

## Pre-Release Quality Assurance

Before deployment, the project can be validated using:

```bash
bash scripts/preflight_qa.sh
```

The QA process includes:

- English/Arabic parity validation
- Missing Arabic-page detection
- Strict MkDocs builds
- Clean build generation
- Theme asset validation
- Logo and favicon validation
- Route validation
- Internal-link validation
- Static-asset validation

## Deployment

Deployment is automated through **GitHub Actions** and published to **Firebase Hosting**.

On every push to `main`, the workflow in `.github/workflows/deploy-mkdocs.yml`:

1. Embeds new resource files and repairs generated viewer pages
2. Builds the course manifest, search index and AI page-text files
3. Optimizes the HTML and normalizes canonical URLs to each page's real address
4. Adds a text version to slide pages and writes `llms.txt`
5. Rebuilds `sitemap.xml` from the final pages
6. Validates routes, internal links, SEO metadata and the sitemap
7. Compresses PDFs and seals the paid ETHCS303 course content
8. Turns meta-refresh redirect pages into real 301 redirects in `firebase.json`
9. Deploys to the Firebase Hosting live channel and notifies IndexNow of changed URLs

The primary public domain is:

**https://shoug-tech.com/**

`www.shoug-tech.com` redirects to it through Cloudflare. The `operating-systems` and `database` subdomains are served from GitHub Pages, and `lilly-kitchen` from Vercel.

## Search Engines and AI Access

Updates made in November 2026 so that Google indexes the right pages and AI assistants (ChatGPT, Claude, Perplexity) can read the site.

### Search indexing

- **Removed hreflang tags.** A deploy step had been pointing every page's Arabic alternate at `/ar/...`, which does not exist, so Google collected thousands of 404 URLs. Arabic is applied in the browser on the same page, so the build now strips hreflang tags (`optimize_site_html.py`, `normalize_page_urls.py`), and `check_seo_metadata.py` fails the deploy if they return.
- **Cleaned the sitemap.** Removed pages are dropped and the sitemap is rebuilt from the final HTML on every deploy. Course-access sample pages that redirect are excluded.
- **Mapped old URLs.** `scripts/build_legacy_redirects.py` reads renamed and deleted pages from git history and writes about 2,000 safe old-to-new redirects to `workers/indexing/src/legacy-redirects.json`. These are served by the `shoug-indexing` Cloudflare Worker, which only runs on hostnames that go through Cloudflare. Since the move to Firebase, the main domain does not, so these redirects are not active on it yet.

### AI assistant access

- **Slide text on slide pages.** Slides live inside a PDF viewer that bots cannot read, so `scripts/add_slide_text.py` adds a collapsed "Text version" section with the text of every slide.
- **`llms.txt`.** `scripts/build_llms_txt.py` publishes a short map of the site and all courses at `/llms.txt`, the file AI tools look for first.
- **Page text as JSON.** Extracted text for academic pages is available at `/ai-context/<page path>/context.json`.
- **Real redirects.** `scripts/build_firebase_redirects.py` converts meta-refresh pages, which many bots do not follow, into 301 redirects at deploy time.
- **Cloudflare bot settings.** Bot Fight Mode and AI Labyrinth are off, so AI fetchers are not challenged. These settings now apply only to `www`.

The paid ETHCS303 course is excluded from all of the above.

### Hosting and DNS security

- The main site is served over HTTPS with HSTS by Firebase Hosting.
- The old GitHub Pages A record that Cloudflare flagged as dangling was replaced when the domain moved to Firebase.
- The GitHub Pages subdomains serve their own sites, so they cannot be taken over.
- SPF and DMARC records protect the domain's email from spoofing.

### Maintenance

After renaming or moving pages, commit and push the change, then run:

```bash
python3 scripts/build_legacy_redirects.py
python3 scripts/build_indexing_manifest.py
```

`build_legacy_redirects.py` needs full git history, so it runs by hand and never in CI. The slide text, `llms.txt` and Firebase redirects are generated automatically on every deploy.

## Project Philosophy

SHOUG.TECH is built around a simple principle:

> Build useful systems, understand how they work, secure them where possible, and document what was learned.

The platform is designed to evolve alongside my academic, technical, and professional work rather than functioning as a static portfolio.

## Copyright

Copyright © 2026 **Shoug Fawaz Alomran**. All rights reserved.

You may:

- View and reference this repository for personal and educational purposes
- Use the published material as a learning reference with appropriate attribution

You may not:

- Reproduce or redistribute substantial portions of the repository without permission
- Republish the site's original content as your own
- Use the content commercially without prior written consent

For permissions or inquiries:

**[Shoug.Alomran@Shoug-Tech.com](mailto:Shoug.Alomran@Shoug-Tech.com)**
