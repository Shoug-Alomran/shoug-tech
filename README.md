# Shoug Fawaz Alomran - Digital Garden & Interactive CV

This repository powers my digital garden: a bilingual (English/Arabic) MkDocs site that combines course notes, cybersecurity content, projects, workshops, and career pages.

## About
I’m **Shoug Fawaz Alomran**, passionate about:
- **Penetration Testing**: exploring systems ethically to make them safer
- **Software Development**: building useful tools and apps for everyday life
- **Cybersecurity Awareness**: helping others protect themselves online

This digital garden is both an interactive CV and a long-term learning archive covering academics, projects, labs, volunteering, and career development.

## Live Site
- [Primary domain](https://shoug-tech.com/)
- [GitHub Pages deployment](https://shoug-alomran.github.io/My-Garden/)

## Tech Stack
- Python 3
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n)
- GitHub Actions + GitHub Pages

## Repository Layout
- `docs/`: site content, assets, custom styles/scripts, and Arabic `*.ar.md` pages
- `mkdocs.yml`: full navigation, theme, plugins, and i18n config
- `scripts/`: bilingual parity checks, Arabic sync utility, preflight QA
- `.github/workflows/deploy-mkdocs.yml`: CI build and deploy pipeline
- `site/`: generated output (build artifact only)

## Site Sections
- `Home`: overview and introduction
- `Start Here`: onboarding guide for navigating the garden
- `Learn`: academic notes, chapters, quizzes, and study resources
- `Career Development`: profile, projects, services, CV, and workshop materials
- `Resources`: curated links and references
- `About`: copyright and policy pages

## Local Development
```bash
git clone https://github.com/Shoug-Alomran/My-Garden.git
cd My-Garden

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install mkdocs-material mkdocs-static-i18n

mkdocs serve
```

## Bilingual Workflow
### 1) EN/AR parity check
```bash
python3 scripts/check_i18n_parity.py
```

Strict mode:
```bash
python3 scripts/check_i18n_parity.py --strict
```

Auto-create missing Arabic placeholders:
```bash
python3 scripts/check_i18n_parity.py --autofix-missing-ar
```

### 2) Arabic sync utility
`scripts/sync_arabic.py` translates English markdown into Saudi-friendly formal Arabic while preserving markdown structure.

```bash
# Dry-run
python3 scripts/sync_arabic.py

# Create missing Arabic files
OPENAI_API_KEY=your_key python3 scripts/sync_arabic.py --apply

# Update existing Arabic files when English changes
OPENAI_API_KEY=your_key python3 scripts/sync_arabic.py --apply --update-existing
```

Optional:
- `--backup` create `.bak` before overwriting
- `--limit N` process only first N files
- `--force` ignore hash cache and retranslate

## Pre-Release QA
Run:
```bash
bash scripts/preflight_qa.sh
```

It performs:
- strict EN/AR parity check with autofix for missing Arabic files
- clean `mkdocs build --clean`
- favicon validation (`docs/favicon.ico`)

## Deployment
On every push to `main`, GitHub Actions:
1. installs dependencies
2. runs strict EN/AR parity checks
3. builds the MkDocs site
4. deploys to GitHub Pages

Workflow file: `.github/workflows/deploy-mkdocs.yml`

## Copyright
Copyright (c) 2026 Shoug Fawaz Alomran. All rights reserved.

You may:
- View and reference this project for personal and educational use

You may not:
- Reproduce, redistribute, or publish substantial portions without explicit permission
- Use the content commercially without prior consent

Contact: **Shoug.Alomran@Shoug-Tech.com**
