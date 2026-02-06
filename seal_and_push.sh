#!/bin/bash
# ZNON Validated Sealer v1.4.9
# Purpose: Prevent "Broken Truth" via JSON validation and Circularity checks.

echo "[ZNON] Initializing Validated Seal..."

# 1. State Cleanup
lsof -ti:5001 | xargs kill -9 2>/dev/null

# 2. Logic Validator Layer
echo "[ZNON] Performing 9-Sigma Registry Audit..."
VALID=true

for f in core/registry/*.jnon; do
    # Check JSON Syntax
    if ! python3 -c "import json; json.load(open('$f'))" 2>/dev/null; then
        echo -e "\033[1;31m[ERROR]\033[0m Syntax Error in $f"
        VALID=false
    fi
    
    # Check for Circularity (Basic check for self-reference)
    TERM_ID=$(basename "$f" .jnon)
    if grep -q "$TERM_ID" "$f" && grep -q "points_to" "$f"; then
        echo -e "\033[1;33m[WARNING]\033[0m Potential Circular Definition in $f"
    fi
done

if [ "$VALID" = false ]; then
    echo "[ABORT] Substrate integrity check failed. Fix errors to proceed."
    exit 1
fi

# 3. Anchoring Protocol
if [ -f "./anchor_all.sh" ]; then
    ./anchor_all.sh
fi

# 4. Intelligence Layer & Propagation
git add .
CHANGES=$(git status -s | awk '{print $2}' | paste -sd "," - | sed 's/,/, /g')

if [ -z "$CHANGES" ]; then
    echo "[ABORT] No changes detected."
    exit 0
fi

SUGGESTION="Validated Anchor: $CHANGES"
echo -e "\033[1;33m[SUGGESTED TRUTH]:\033[0m $SUGGESTION"
read -p "Enter Commit Truth (Press Enter to use suggestion): " msg
final_msg=${msg:-$SUGGESTION}

git commit -m "$final_msg"
git push origin main

echo "[ZNON] Substrate Sealed and Validated: $final_msg"
