#!/bin/sh
# OCR an image-only slide deck into scripts/exam_analysis/ocr/<stem>.txt, one
# page per form feed, for build_exam_analysis.py to count against.
#   sh scripts/exam_analysis/ocr_deck.sh docs/.../chapter-5.pdf
set -e
pdf="$1"
stem=$(basename "$pdf" .pdf)
out="$(dirname "$0")/ocr/$stem.txt"
tmp=$(mktemp -d)
pdftoppm -r 120 -gray -png "$pdf" "$tmp/p"
: > "$out"
for img in $(ls "$tmp"/p-*.png | sort -t- -k2 -n); do
  tesseract "$img" - --psm 3 2>/dev/null >> "$out"
  printf '\f' >> "$out"
done
rm -rf "$tmp"
echo "$stem: $(grep -c . "$out") lines"
