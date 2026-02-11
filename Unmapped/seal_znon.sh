#!/bin/bash
# ZNON 858-Term Sovereign Seal Protocol for Termux
set -e

GLOSSARY_FILE="core/GLOSSARY.md"
REGISTRY_DIR="core/registry"
REPO_URL="git@github.com:thezachsubstrate/ZNON-Ledger.git"

echo "⚡ ZNON Sovereign Seal Protocol"
echo "Location: $(pwd)"
echo "Time: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

# Create registry if missing
mkdir -p "$REGISTRY_DIR"

# Check if GLOSSARY exists, if not create from stdin/paste
if [ ! -f "$GLOSSARY_FILE" ]; then
    echo "❌ GLOSSARY.md not found. Create it first with the 858 terms."
    exit 1
fi

# Count terms in glossary
TOTAL_TERMS=$(grep -cE '^[0-9]+\. \*\*' "$GLOSSARY_FILE" 2>/dev/null || echo "0")
echo "📊 Detected $TOTAL_TERMS terms in glossary"

if [ "$TOTAL_TERMS" -ne 855 ]; then
    echo "⚠️ Warning: Expected 858 terms, found $TOTAL_TERMS"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Process each term
grep -E '^[0-9]+\. \*\*' "$GLOSSARY_FILE" | while IFS= read -r line; do
    if [[ "$line" =~ ^([0-9]+)\.\ \*\*(.+)\*\*:\ (.*)$ ]]; then
        num_raw="${BASH_REMATCH[1]}"
        term="${BASH_REMATCH[2]}"
        def="${BASH_REMATCH[3]}"
        
        num=$(printf "%03d" "$num_raw")
        safe_name=$(echo "$term" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '_' | sed 's/_$//' | cut -c1-50)
        filename="${num}_${safe_name}.md"
        filepath="$REGISTRY_DIR/$filename"
        
        echo "🔹 Term $num_raw: $term"
        
        # Skip if exists and has OTS
        if [ -f "$filepath" ] && [ -f "$filepath.ots" ]; then
            echo "   ⏭️ Already sealed"
            continue
        fi
        
        # Generate artifact
        cat > "$filepath" << EOF
# ZNON Registry Entry: Term $num_raw

**Term ID:** $num_raw
**Canonical Name:** $term
**Definition:** $def
**Status:** Logic-Locked
**Sealed:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Source:** [\`$GLOSSARY_FILE\`](../../$GLOSSARY_FILE)

## Sovereign Metadata
- **Root Author:** Zach Mosley
- **Repository:** $REPO_URL
- **Verification:** SHA-256:$(sha256sum "$filepath" 2>/dev/null | awk '{print $1}' || echo "pending")

*OTS Proof: $filepath.ots*
EOF
        
        # OTS Stamp (Termux-friendly)
        if [ ! -f "$filepath.ots" ]; then
            if command -v ots >/dev/null 2>&1; then
                ots stamp "$filepath" 2>/dev/null && echo "   ⏳ Stamped" || echo "   ⚠️ Stamp pending"
            else
                echo "   ⚠️ OTS not available"
            fi
        fi
        
        # Git commit per term (atomic)
        git add "$filepath" "$filepath.ots" 2>/dev/null
        git commit -m "ZNON-Registry[$num_raw]: Seal $term" --quiet 2>/dev/null || true
    fi
done

echo ""
echo "✅ Registry seal cycle complete"
echo "Next: Run './upgrade_proofs.sh' after 1 hour for Bitcoin anchoring"
