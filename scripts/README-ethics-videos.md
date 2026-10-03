# Ethics video publishing

Register a recording in `ethics-new-recordings.json` with a unique lesson slug,
source path relative to the iCloud Ethics folder, R2 key, title and related
breakdown. Keep `ready` false until processing succeeds.

Run the integrated upload workflow:

```sh
export ETHICS_CONTENT_ROOT="$PWD/.private-courses/ethics"
python3 scripts/process_ethics_uploads.py --whisper /path/to/whisper.cpp
```

It reuses existing R2 objects, uploads missing MP4 files, generates original-language Arabic/English
captions locally, checks caption timing and repeated text, generates a poster,
and builds the lesson pages, transcript data and listening controls. Caption
review failures keep the new lesson unpublished. Download cloud-only files in
Finder and rerun; completed lessons are skipped.

Paid lesson pages and captions must be generated into the private course source:

```sh
export ETHICS_CONTENT_ROOT="$PWD/.private-courses/ethics"
python3 scripts/build_ethics_video_pages.py
python3 scripts/build_ethics_study_tools.py
python3 scripts/secure_ethics_content.py --build-worker --check
```

Review the private pages and caption files, then deploy the course-access Worker.
Do not publish paid HTML, captions, or transcripts through GitHub Pages.
Register replacements with a new slug and R2 key so
captions cannot accidentally refer to the previous recording.

This is a local upload-and-caption workflow. Uploading directly in Cloudflare's
R2 dashboard does not invoke it; no cloud queue or always-running transcription
service is configured.

`build_ethics_study_tools.py` uses reviewed transcript-based chapter outlines
when available and finds topic mentions for other recordings. Future recordings
receive automatic topic markers until an outline is added to `CURATED_CHAPTERS`.
Caption/transcript wording is automatic and can still contain recognition errors.

Mixed-language recordings require transcription in the original spoken languages,
not translation. Review English passages as well as Arabic before publishing;
automatic language detection alone does not guarantee accurate code-switching.

For Arabic–English recordings, draft captions with short pause-aligned windows:

```sh
python3 scripts/transcribe_ethics_bilingual.py \
  --only introduction-to-business-ethics --output-dir /tmp/ethics-caption-review
```

This requires `mlx-whisper`, `numpy`, and `ffmpeg` on Apple Silicon. The larger
multilingual model runs locally. Validate timing, review mixed-language passages,
and copy approved drafts into the private captions directory before rebuilding.
Do not assume a language auto-detection result guarantees faithful transcription.
