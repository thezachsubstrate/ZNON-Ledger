#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./znon-add-spec.sh /path/to/spec-file.txt"
  exit 1
fi

INPUT_PATH="$1"
BASENAME="$(basename "$INPUT_PATH")"
NAME_NO_EXT="${BASENAME%.*}"
SPEC_DIR="specs"
RECEIPTS_DIR="receipts"
LEDGER_DIR="ledger/anchoring"

mkdir -p "$SPEC_DIR" "$RECEIPTS_DIR" "$LEDGER_DIR"

# 1) Copy spec into specs/
cp "$INPUT_PATH" "$SPEC_DIR/$BASENAME"

# 2) Hash
HASH=$(shasum -a 256 "$SPEC_DIR/$BASENAME" | awk '{print $1}')
echo "SHA-256: $HASH"

# 3) Timestamp with OTS
ots stamp "$SPEC_DIR/$BASENAME"

# OTS creates .ots next to the file
OTS_FILE="$SPEC_DIR/$BASENAME.ots"
if [ ! -f "$OTS_FILE" ]; then
  OTS_FILE="$SPEC_DIR/$BASENAME.ots"
fi

# Move receipt into receipts/
mv "$OTS_FILE" "$RECEIPTS_DIR/$BASENAME.ots"

# 4) Create ledger entry
LEDGER_FILE="$LEDGER_DIR/${NAME_NO_EXT}-ledger.md"
NOW_HUMAN="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat > "$LEDGER_FILE" <<EOF
# ${NAME_NO_EXT} Ledger Entry

## Artifact Details
- **Artifact:** $BASENAME  
- **SHA-256 Hash:** $HASH  
- **OTS Receipt:** $BASENAME.ots  

## Blockchain Attestation
- **Blockchain:** Bitcoin (mainnet)  
- **Attestation Block:** _to be filled after ots upgrade_  
- **Attested Existence As Of:** $NOW_HUMAN  

## Governance Meaning
This entry records the cryptographic fingerprint and timestamp of the artifact. Any modification to the file invalidates the proof, making this entry the immutable temporal boundary for this version.

## Contract Reference Clause
> This agreement references the specification file $BASENAME, cryptographically anchored via OpenTimestamps. The SHA-256 hash of the referenced artifact is $HASH. Any modification to the specification must be accompanied by a new blockchain attestation.
EOF

# 5) Git commit + push
git add "$SPEC_DIR/$BASENAME" "$RECEIPTS_DIR/$BASENAME.ots" "$LEDGER_FILE"
git commit -m "Add $NAME_NO_EXT spec, receipt, and ledger entry"
git push origin main

echo "Done. Added $BASENAME, stamped, ledgered, and pushed."

