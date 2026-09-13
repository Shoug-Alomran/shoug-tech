# Ethics video publishing

Register a recording in `ethics-new-recordings.json` with a unique lesson slug,
source path relative to the iCloud Ethics folder, R2 key, title and related
breakdown. Keep `ready` false until processing succeeds.

Run the integrated upload workflow:

```sh
python3 scripts/process_ethics_uploads.py --whisper /path/to/whisper.cpp
```

It reuses existing R2 objects, uploads missing MP4 files, generates Arabic
captions locally, checks caption timing and repeated text, generates a poster,
and builds the lesson pages, transcript data and listening controls. Caption
review failures keep the new lesson unpublished. Download cloud-only files in
Finder and rerun; completed lessons are skipped.

Review the generated pages and caption files, then deploy through the existing
GitHub Pages workflow. Register replacements with a new slug and R2 key so
captions cannot accidentally refer to the previous recording.

This is a local upload-and-caption workflow. Uploading directly in Cloudflare's
R2 dashboard does not invoke it; no cloud queue or always-running transcription
service is configured.

`build_ethics_study_tools.py` uses reviewed transcript-based chapter outlines
when available and finds topic mentions for other recordings. Future recordings
receive automatic topic markers until an outline is added to `CURATED_CHAPTERS`.
Caption/transcript wording is automatic and can still contain recognition errors.
