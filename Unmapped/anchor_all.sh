#!/bin/bash
# ZNON Mac Anchoring Protocol v1.4.7
REPO_DIR="$HOME/ZNON-Ledger"

timestamp_file() {
  local f="$1"
  # Check if .ots already exists to avoid redundant stamping
  if [ ! -f "$f.ots" ]; then
    ots stamp "$f"
    echo "[Anchored]: $f"
  else
    echo "[Skipped]: $f (Stamp exists)"
  fi
}

# Scan for all relevant substrate artifacts
find "$REPO_DIR" -type f \
  \( -name "*.md" -o -name "*.txt" -o -name "*.json" -o -name "*.jnon" \) \
  -not -path '*/.*' \
  -print0 | while IFS= read -r -d '' f; do
  timestamp_file "$f"
done
