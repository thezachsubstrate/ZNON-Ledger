#!/data/data/com.termux/files/usr/bin/bash
REPO_DIR=/data/data/com.termux/files/home/znon_repo

timestamp_file() {
  local f="$1"
  ots stamp "$f"
  echo "[Anchored]: $f"
}

find "$REPO_DIR" -type f \
  \( -name "*.md" -o -name "*.txt" -o -name "*.json" \) \
  -print0 | while IFS= read -r -d '' f; do
  timestamp_file "$f"
done

