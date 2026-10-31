#!/usr/bin/env bash
# Bring a rendered film's sound up to social-platform loudness (-14 LUFS, -1 dBTP), video stream copied untouched.
# usage: nyasha-ads/tools/loudness.sh <film.mp4>...
set -euo pipefail
for f in "$@"; do
  tmp="${f%.mp4}.loud.mp4"
  ffmpeg -v error -y -i "$f" -c:v copy -af loudnorm=I=-14:TP=-1:LRA=11 -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$tmp"
  mv "$tmp" "$f"
  echo "$f: $(ffmpeg -hide_banner -i "$f" -vn -af ebur128 -f null - 2>&1 | grep -A1 'Integrated loudness' | grep -o 'I: *[-0-9.]* LUFS')"
done
