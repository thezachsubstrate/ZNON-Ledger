#!/bin/bash
# ZNON Master Sealer v1.4.8
# Purpose: Auto-generate 9-sigma Commit Truths and maintain Substrate integrity.

echo "[ZNON] Initializing Smart Seal..."

# 1. Stale State Cleanup
lsof -ti:5001 | xargs kill -9 2>/dev/null

# 2. Run Mac Anchoring Protocol
if [ -f "./anchor_all.sh" ]; then
    chmod +x ./anchor_all.sh
    ./anchor_all.sh
else
    echo "[ERROR] anchor_all.sh not found."
    exit 1
fi

# 3. Intelligence Layer: Suggesting the Truth
git add .
CHANGES=$(git status -s | awk '{print $2}' | paste -sd "," - | sed 's/,/, /g')

if [ -z "$CHANGES" ]; then
    echo "[ABORT] No changes detected in the Substrate."
    exit 0
fi

SUGGESTION="Update $CHANGES"
echo -e "\033[1;33m[SUGGESTED TRUTH]:\033[0m $SUGGESTION"
read -p "Enter Commit Truth (Press Enter to use suggestion): " msg

# Use suggestion if input is empty
final_msg=${msg:-$SUGGESTION}

# 4. Finality & Propagation
git commit -m "$final_msg"
git push origin main

echo "[ZNON] Substrate Sealed: $final_msg"
