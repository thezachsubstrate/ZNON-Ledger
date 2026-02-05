#!/bin/bash
# ZNON Master Sealer v1.4.6
# Purpose: Eliminate Stale State Drift and ensure cryptographic finality.

echo "[ZNON] Initializing Master Seal..."

# 1. Kill stale API processes
lsof -ti:5001 | xargs kill -9 2>/dev/null

# 2. Run the Anchoring Protocol
if [ -f "./anchor_all.sh" ]; then
    chmod +x ./anchor_all.sh
    ./anchor_all.sh
else
    echo "[ERROR] anchor_all.sh not found. Substrate integrity compromised."
    exit 1
fi

# 3. Git Propagation
git add .
read -p "Enter Commit Truth (Message): " msg
git commit -m "$msg"
git push origin main

echo "[ZNON] Substrate Sealed and Propagated to GitHub."
