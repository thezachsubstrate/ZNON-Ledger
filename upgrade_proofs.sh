#!/bin/bash
# ZNON OpenTimestamps Proof Upgrade Script
set -e

REGISTRY_DIR="core/registry"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${CYAN}⚡ ZNON OTS PROOF UPGRADE${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo "Time: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

if ! command -v ots >/dev/null 2>&1; then
    echo -e "${YELLOW}❌ OpenTimestamps client not installed${NC}"
    exit 1
fi

if [ ! -d "$REGISTRY_DIR" ]; then
    echo -e "${YELLOW}❌ Registry directory not found${NC}"
    exit 1
fi

OTS_COUNT=$(ls "$REGISTRY_DIR"/*.ots 2>/dev/null | wc -l)

if [ "$OTS_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  No OTS files found${NC}"
    exit 1
fi

echo -e "${BLUE}📊 Found $OTS_COUNT OTS proof files${NC}"
echo ""

UPGRADED=0
PENDING=0
FAILED=0

for ots_file in "$REGISTRY_DIR"/*.ots; do
    [ ! -f "$ots_file" ] && continue
    
    basename=$(basename "$ots_file")
    echo -e "${BLUE}🔹 Processing: $basename${NC}"
    
    if ots upgrade "$ots_file" 2>&1 | grep -q "Success"; then
        echo "   ✅ Upgraded to Bitcoin anchor"
        ((UPGRADED++))
        git add "$ots_file" 2>/dev/null
        git commit -m "ZNON: Upgrade OTS proof $basename" --quiet 2>/dev/null || true
    elif ots upgrade "$ots_file" 2>&1 | grep -q "pending"; then
        echo "   ⏳ Still pending"
        ((PENDING++))
    else
        echo "   ⚠️  Upgrade failed"
        ((FAILED++))
    fi
done

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}📊 UPGRADE SUMMARY${NC}"
echo "Total: $OTS_COUNT | Upgraded: $UPGRADED | Pending: $PENDING | Failed: $FAILED"
echo ""
echo "Complete: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
