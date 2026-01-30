#!/bin/bash
# ZNON v1.0 Automation Script - Zach Substrate Jurisdiction

FILE=$1

if [ -z "$FILE" ]; then
    echo "Usage: ./anchor.sh <filename>"
    exit 1
fi

echo "--- Initializing ZNON Anchoring Protocol ---"

# 1. Generate SHA-256 Hash
echo "[1/4] Generating Canonical SHA-256..."
HASH=$(sha256sum "$FILE" | awk '{print $1}')
echo "Hash: $HASH"

# 2. OpenTimestamps Stamping
echo "[2/4] Anchoring to Bitcoin via OTS..."
ots stamp "$FILE"

# 3. Verification Check
echo "[3/4] Verifying OTS Proof..."
ots verify "$FILE.ots"

# 4. Git Propagation (Dual-Node Sync)
echo "[4/4] Propagating to Nodes (Mac/Samsung)..."
git add .
git commit -m "ZNON Artifact: $FILE | Hash: $HASH"
git push

echo "--- Protocol Complete. ZNON is Anchored. ---"

