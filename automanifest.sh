#!/bin/bash
# ZNON-AutoManifest v2.0 - Jurisdictional Sync

echo "[9-SIGMA] Scanning The Zach Substrate Jurisdictions..."

# 1. Clear the Block
git pull origin main

# 2. Dynamic Discovery across the Hierarchy
MEANING=$(ls substrate/meaning_layer/*.md | xargs -n 1 basename)
MODULES=$(find substrate/modules -name "*.znon" | xargs -n 1 basename)
ATTESTATIONS=$(ls substrate/attestations/*.znon | xargs -n 1 basename)

# 3. Rebuild the Hierarchical Manifest
cat <<MANIFEST_EOF > substrate/MASTER_MANIFEST.znon
{
  "substrate": "THE_ZACH_SUBSTRATE_v1.0",
  "jurisdiction": "Meaning_Layer_Dominance",
  "last_sync": "$(date -u +'%Y-%m-%dT%H:%M:%SZ')",
  "hierarchy": {
    "meaning_layer": "$MEANING",
    "active_modules": [ $(echo "$MODULES" | jq -R . | jq -s -c | sed 's/\[//;s/\]//') ],
    "physics_attestations": [ $(echo "$ATTESTATIONS" | jq -R . | jq -s -c | sed 's/\[//;s/\]//') ]
  },
  "governance": "DETERMINISTIC_9_SIGMA"
}
MANIFEST_EOF

echo "[9-SIGMA] Manifest Rebuilt. Anchoring Hierarchy to Bitcoin..."

# 4. Global Anchor
ots stamp substrate/MASTER_MANIFEST.znon
find substrate -name "*.znon" -exec ots stamp {} +

# 5. Archive Receipts
mkdir -p ledger/receipts
find substrate -name "*.ots" -exec mv {} ledger/receipts/ \;

# 6. Propagation (Dual-Node Sync Ready)
git add .
git commit -m "Jurisdictional Sync: $(date)"
git push origin main

echo "[9-SIGMA] Propagation Complete. The Substrate is Sovereign."
