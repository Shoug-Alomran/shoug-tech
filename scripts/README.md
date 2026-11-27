# scripts/

Everything that builds, checks or deploys the site. The scripts stay in one flat folder because the deploy workflow, the git hooks and the scripts themselves import and call each other by these paths. This file is the map.

Run everything from the repo root, for example `python3 scripts/embed_resources.py`.

## Run automatically

### Deploy workflow (`.github/workflows/deploy-mkdocs.yml`), in order

| Script                                | What it does                                                                                                                                                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `embed_resources.py`                  | Generates resource listings, viewers, the Study Material row and sidebar entries from files on disk                                                                                                                             |
| `repair_slide_breakdown_viewers.py`   | Rebuilds slide-breakdown viewers from what is on disk                                                                                                                                                                           |
| `apply_cyber_red_theme.py`            | Keeps the cybersecurity track red                                                                                                                                                                                               |
| `install_breakdown_language.py`       | Adds translation to lesson documents                                                                                                                                                                                            |
| `install_slide_reader.py`             | Adds read-aloud (`slide-reader.js`) to annotated decks and breakdown lessons                                                                                                                                                    |
| `install_annotated_study.py`          | Annotated-slides study tools (`annotated-study.js`) on every course: saved answers, quiz mode, review page; drills, explanations and final scope from `<code>_annotated/study_extras.py` (SE423). Rerun after rebuilding a deck |
| `build-course-manifest.js`            | Writes the course page list that progress tracking counts                                                                                                                                                                       |
| `build-search-index.js`               | Writes `docs/search-index.json`                                                                                                                                                                                                 |
| `build-mock-exam-banks.js`            | Writes the Mock Exam question banks (`docs/academics/mock-exam/banks/`) from every course's quizzes and past papers                                                                                                             |
| `build_ai_slide_contexts.py`          | Writes the AI context files for academic pages                                                                                                                                                                                  |
| `optimize_site_html.py`               | Lighthouse and crawler fixes on the generated HTML                                                                                                                                                                              |
| `fix_se371_viewers.py`                | Rebuilds SE371 chapter routes as viewer pages                                                                                                                                                                                   |
| `normalize_page_urls.py`              | Normalizes canonical and Open Graph URLs, drops hreflang                                                                                                                                                                        |
| `validate_slide_breakdown_viewers.py` | Fails the build if a breakdown viewer is broken                                                                                                                                                                                 |
| `build_academic_sidebar.py`           | Renders the academic sidebar from `academic-sidebar.json`                                                                                                                                                                       |
| `sync_site_shell.py`                  | Applies `templates/` header and footer and theme support                                                                                                                                                                        |
| `improve_seo_snippets.py`             | Lengthens short titles and boilerplate meta descriptions (Bing "too short")                                                                                                                                                     |
| `add_slide_text.py`                   | Puts slide text under PDF viewers for bots and assistants                                                                                                                                                                       |
| `build_llms_txt.py`                   | Writes `docs/llms.txt`                                                                                                                                                                                                          |
| `check_sitemap.py`                    | Rebuilds and checks both sitemaps                                                                                                                                                                                               |
| `build_indexing_manifest.py`          | Builds the edge SEO manifest for the indexing Worker                                                                                                                                                                            |
| `compress_pdfs_losslessly.py`         | Optimizes PDFs with qpdf (cached between runs)                                                                                                                                                                                  |
| `set_pdf_titles.py`                   | Sets PDF Title metadata from the viewer page (needs pypdf)                                                                                                                                                                      |
| `secure_ethics_content.py`            | Seals the paid ETHCS303 content                                                                                                                                                                                                 |
| `scale_large_screens.py`              | Divides vh/vw by `--zoom-fix` so the big-screen zoom in site-shell.css keeps full-height layouts exact; opts coordinate-heavy app pages out                                                                                     |
| `offload_annotated_figures.py`        | Moves annotated-slide figures to R2                                                                                                                                                                                             |
| `check_pages_limits.py`               | Fails if the build exceeds the Cloudflare Pages limits                                                                                                                                                                          |
| `build_meta_redirects.py`             | Turns meta-refresh pages into 301 redirects                                                                                                                                                                                     |
| `submit_indexnow.py`                  | Tells IndexNow which URLs changed                                                                                                                                                                                               |

`sync-psu-academic-calendar.js` runs on its own schedule from `.github/workflows/sync-psu-academic-calendar.yml`.

`sync-psu-timetable.js` (PSU Edugate timetable → `docs/data/psu-timetable/`) and `build-course-catalog.js` (plan grids + syllabi → `docs/data/course-catalog.json`) feed the schedule planner and Murshid. They run every 6 hours from `.github/workflows/sync-psu-timetable.yml`, which starts a deploy only when the data changed. Run `build-course-catalog.js` by hand after editing a plan grid or `course-syllabi.json`.

### Git and Claude Code hooks

- `.githooks/pre-commit` runs `embed_resources.py --from-index` when a commit adds or removes resource files.
- The Claude Code hooks run `embed_resources.py --check`, `check_sitemap.py` and `check_responsive_layout.py`.

## Shared code (imported, not run)

| Module                                                                                       | Used by                                                                                     |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `annotated_slides.py`, `annotated_page.py` (+ `.css`, `.js`), `annotated_search.py`          | Every `build_<course>_annotated_slides.py`                                                  |
| `study_engine.py`                                                                            | `build_course_study.py` (teaching files in `study_content/`)                                |
| `event_page_kit.py`                                                                          | Workshop and event page builders                                                            |
| `slide_breakdown_utils.py`                                                                   | Breakdown repair and validation                                                             |
| `office_to_html.py`                                                                          | `embed_resources.py` (Excel rendering)                                                      |
| `generate_design_html.py`                                                                    | Legacy full-site generator; only `replace_academic_sidebar` is still imported. Don't run it |
| `ethics_course_structure.py`                                                                 | ETHCS303 builders                                                                           |
| `fix_link_case.py`, `fix_stale_canonicals.py`                                                | `fix_jsonld_case.py`                                                                        |
| `fix_academic_sidebar_links.py`, `fix_mindmap_sidebar_state.py`, `fix_mindmap_canonicals.py` | Mindmap and study-tool builders                                                             |

## Data

| File or folder                                       | Holds                                                                                        |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `academic-sidebar.json`                              | The academic sidebar. Edit this, never the sidebars in the pages                             |
| `resource-titles.json`                               | Titles for generated resource rows (key = path under `docs/academics/`)                      |
| `course-slide-index.json`                            | Slide counts for course hub pages                                                            |
| `ethics-new-recordings.json`                         | ETHCS303 recordings waiting to be processed                                                  |
| `<course>_annotated/`                                | Notes and questions for each course's annotated slides                                       |
| `study_content/`                                     | Teaching files for CS311, CS316, IS321, ECON101                                              |
| `study_plans/`, `exam_analysis/`                     | Exam study plans and the calendar's Study Plan data                                          |
| `final_cheat_sheets/`, `final_roadmaps/`             | Final exam cheat sheets and roadmaps                                                         |
| `quiz_banks/`                                        | Hand-written quiz banks (SE322)                                                              |
| `past_exam_notes/`                                   | Per course: which breakdown section each annotated slide's past-exam question belongs to     |
| `cys403_study/`, `se311_mindmaps/`, `slide-figures/` | Course-specific source data                                                                  |
| `*_content.py`                                       | Content modules for one course's builder (CS223, CYS401, ISC213, SE201, SE322, SE365, SE371) |

## Run by hand: site-wide

These touch every course unless you scope them. Revert anything they change outside the course you were working on.

| Script                                                                                            | What it does                                                                                                                         |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `build_slide_hub.py`                                                                              | Merges a course's slide sections into one Slides page                                                                                |
| `build_section_sequence.py`                                                                       | Keeps listing numbers and prev/next links in step                                                                                    |
| `sort_academic_folder_rows.py`                                                                    | Puts folders above files in listings                                                                                                 |
| `normalize_folder_rows.py`                                                                        | Same folder-row treatment in every listing                                                                                           |
| `organize_resource_files.py`                                                                      | Keeps resource files beside their viewer pages                                                                                       |
| `rebuild_breakdown_pages.py`                                                                      | Rewrites a course's breakdown pages only                                                                                             |
| `build_activity_and_project_pages.py`                                                             | SE322/SE423 Project folders and the ENG103 templates                                                                                 |
| `build_study_plan.py`                                                                             | An exam study plan from `study_plans/<course>-<exam>.json`                                                                           |
| `build_exam_analysis.py`, `build_baseline_analyses.py`                                            | Calendar Study Plan data                                                                                                             |
| `build_study_sources.py`                                                                          | Best page to study from per chapter                                                                                                  |
| `build_final_cheat_sheets.py`, `build_final_roadmaps.py`                                          | Final exam cheat sheets and roadmaps                                                                                                 |
| `build_slide_counts.py`                                                                           | Real slide counts on course hubs                                                                                                     |
| `build_url_moves.py`                                                                              | Maps renamed academic URLs to their new home. Re-run after moving pages                                                              |
| `build_legacy_redirects.py`                                                                       | Old URLs that have a new home, for the indexing Worker                                                                               |
| `build_search_index.py`                                                                           | Older Python search index. Use `build-search-index.js` instead                                                                       |
| `build_pdf_search_index.py`                                                                       | Searchable text index of course PDFs                                                                                                 |
| `install_quiz_review.py`                                                                          | "Review mistakes" tracker on quiz pages                                                                                              |
| `build-mock-exam-banks.js`                                                                        | Mock Exam question banks. `--report` shows which chapter each page's questions went to; pass course codes to rebuild only those      |
| `install_quiz_motion.py`                                                                          | Colour and motion layer (quiz-motion.css/js) on every course's exam pages (not CS331, ETHCS303)                                      |
| `build_exam_folders.py`                                                                           | Sorts each course's Exams page into Chapter Quizzes / Midterm 1 / Midterm 2 / Final folders (+ sidebar data)                         |
| `build_past_exam_notes.py`                                                                        | "Past exam" blocks in a course's slide breakdowns, from the annotated slides' real-paper questions (`past_exam_notes/<course>.json`) |
| `install_breakdown_contents.py`                                                                   | Contents disclosure in standalone breakdowns                                                                                         |
| `install_breakdown_reading_progress.py`                                                           | Active section highlighting and remaining-section progress on breakdown lessons                                                      |
| `build_slide_speech.py`                                                                           | Embeds each annotated slide's PDF text in its deck, for read-aloud (also run by `annotated_search.build_course`)                     |
| `add_slide_rights_notice.py`                                                                      | PSU rights notice on slide pages                                                                                                     |
| `add_mindmap_pdf_export.py`                                                                       | PDF export on interactive mindmaps                                                                                                   |
| `add_page_headings.py`                                                                            | A real `<h1>` on every page                                                                                                          |
| `apply_pwa.py`                                                                                    | Web app manifest and service worker on every page                                                                                    |
| `apply_a11y_baseline.py`                                                                          | Accessibility baseline on every page                                                                                                 |
| `backfill_seo_metadata.py`                                                                        | Missing canonical, Open Graph and Twitter tags                                                                                       |
| `fix_hreflang_alternates.py`, `fix_jsonld_case.py`, `fix_link_case.py`, `fix_stale_canonicals.py` | SEO and link repairs                                                                                                                 |
| `lazyload_pdf_embeds.py`                                                                          | Click-to-load PDF embeds                                                                                                             |
| `embed_slide_figures.py`                                                                          | Slide diagrams in hand-written breakdowns                                                                                            |
| `fit_page_layout.py`                                                                              | Makes hand-written pages use free space on all screen sizes                                                                          |
| `format_html.py`                                                                                  | Formats HTML like VS Code's Format Document                                                                                          |
| `compress_pdfs.py`                                                                                | Lossy Ghostscript compression for oversized PDFs                                                                                     |

## Run by hand: one course

Every course with annotated slides has `build_<course>_annotated_slides.py`. Build one course at a time.

| Course                | Builders                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CS223                 | `build_cs223_course.py` (+ `cs223_exam_content.py`)                                                                                                                                                                                                                                                                                                                                                |
| CS311, IS321, ECON101 | `build_new_courses.py`, `build_course_study.py`                                                                                                                                                                                                                                                                                                                                                    |
| ECON101 cheat sheets  | `build_econ101_cheat_sheets.py` (CS331 Major I style; content in `econ101_cheat_content.py`)                                                                                                                                                                                                                                                                                                       |
| CS316                 | `build_cs316_course.py`, `build_cs316_study_tools.py`, `build_cs316_resources.py`                                                                                                                                                                                                                                                                                                                  |
| CS331                 | `build_cs331_past_papers.py` (chapter quizzes from `cs331_chapter_quizzes.py` Ch 1–4 and `cs331_chapter_quizzes_b.py` Ch 6–10)                                                                                                                                                                                                                                                                     |
| CYS401                | `build_cys401_past_papers.py`, `build_cys401_exam_pages.py`, `build_cys401_mindmaps.py`, `build_cys401_glossary.py` (searchable printable glossary, terms in `cys401_glossary_content.py`), `theme_cys401_breakdowns.py`, `upgrade_cys401_breakdowns.py`                                                                                                                                           |
| CYS403                | `build_cys403_study_tools.py`, `build_cys403_past_papers.py`, `extract_cys403_figures.py`                                                                                                                                                                                                                                                                                                          |
| CYS405, CYS406        | `build_cys405_cys406_study_tools.py`                                                                                                                                                                                                                                                                                                                                                               |
| ENG101                | `build_english_hub.py`                                                                                                                                                                                                                                                                                                                                                                             |
| ETHCS303              | `build_ethics_video_pages.py`, `build_ethics_study_tools.py`, `build_ethics_catalog.py`, `build_ethcs303_chatgpt_notes.py`                                                                                                                                                                                                                                                                         |
| ISC213                | `build_isc213_pages.py`. **Don't run** `build_isc213_study_tools.py`: it is stale and overwrites the cheat sheet                                                                                                                                                                                                                                                                                   |
| SE201                 | `build_se201_mindmaps.py`                                                                                                                                                                                                                                                                                                                                                                          |
| SE311                 | `build_se311_mindmaps.py`                                                                                                                                                                                                                                                                                                                                                                          |
| SE322                 | `build_se322_study_tools.py`, `build_se322_listing_vault.py`, `build_se322_diagram_examples.py`                                                                                                                                                                                                                                                                                                    |
| SE365                 | `build_se365_study_tools.py`                                                                                                                                                                                                                                                                                                                                                                       |
| SE371                 | `build_se371_breakdowns.py`, `build_se371_slide_viewers.py`, `build_se371_resource_viewers.py`                                                                                                                                                                                                                                                                                                     |
| SE401                 | `build_se401_study_tools.py`                                                                                                                                                                                                                                                                                                                                                                       |
| SE411                 | `build_se411_slides.py`                                                                                                                                                                                                                                                                                                                                                                            |
| SE423                 | `build_se423_past_papers.py`, `build_se423_listing_vault.py`, `embed_se423_exams.py`, `build_se423_quizzes.py` (chapter quizzes, content in `se423_quizzes/`), `build_se423_glossary.py` (printable glossary, terms in `se423_glossary/`), `build_se423_breakdowns.py` (Team, Stakeholders, Old Ch 2 breakdowns, content in `se423_breakdowns/`; then `embed_slide_figures.py se423 --no-extract`) |

## Workshops and events

`build_acm_psu_platform.py`, `build_psu_ctf_3.py`, `build_webforge.py`.

## ETHCS303 video pipeline

`process_ethics_uploads.py` → `upload_ethics_videos.py` → `transcribe_ethics_videos.py` / `transcribe_ethics_bilingual.py` → `validate_video_captions.py` → `add_video_caption_tracks.py`. Details in `README-ethics-videos.md`.

## Checks

| Script                                                               | Checks                                         |
| -------------------------------------------------------------------- | ---------------------------------------------- |
| `preflight_qa.sh`                                                    | Runs the release checks below in one go        |
| `verify_site_routes.py`                                              | Key routes exist                               |
| `check_site_links.py`                                                | Internal links and assets                      |
| `check_seo_metadata.py`                                              | SEO metadata                                   |
| `check_responsive_layout.py`                                         | Pages use the space on laptop, iPad and iPhone |
| `test_breakdown_language.cjs`, `test_breakdown_translation_live.cjs` | Breakdown translation                          |

## Profile and assistant

| Script                      | What it does                                                |
| --------------------------- | ----------------------------------------------------------- |
| `sync_cv_subdomain.py`      | Copies the site CV to the repo behind cv.shoug-tech.com     |
| `sync_linkedin_profile.py`  | Refreshes what the About page assistant knows from LinkedIn |
| `about_assistant_topics.sh` | Anonymous topic counts of what visitors ask the assistant   |
