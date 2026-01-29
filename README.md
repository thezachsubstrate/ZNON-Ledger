# ZNON-Ledger

This repository contains blockchain-anchored governance artifacts for the ZNON specification system.

Each artifact is:
- Timestamped via OpenTimestamps
- Anchored in the Bitcoin blockchain
- Recorded with SHA-256 hash and attestation block
- Ready for institutional verification and contract reference

## Structure

- `/ledger/anchoring/` — Immutable timestamp entries for each ZNON spec version
- `/specs/` — The actual specification files
- `/receipts/` — OpenTimestamps `.ots` receipts for each artifact

## Verification

Artifacts in this ledger can be independently verified using the OpenTimestamps client:
```bash
ots verify <filename>.ots
```

## Governance Use

This ledger supports:
- Contractual reference clauses
- Institutional timestamp verification
- Public auditability of governance artifacts
🔗 Anchoring Log

- **ZNON-Spec-v1.1** — SHA-256 hash `6d4a8f4f...077d`, anchored in Bitcoin block **934137** on **2026-01-28 EST**
