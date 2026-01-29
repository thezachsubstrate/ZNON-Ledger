# Automation Rules Capsule — ZNON Governance

Purpose:
To ensure every update to the ZNON-Ledger is contradiction-audited, anchored, journaled, and synchronized without drift.

Automation Requirements:
- Every new term, capsule, or artifact must be:
  - Hashed (SHA-256)
  - Timestamped
  - Anchored (OTS receipt)
  - Journaled in the appropriate sub-journal
  - Added to the Master Journal
  - Committed and pushed to GitHub
  - Contradiction-audited
  - Folder-verified
  - Ledgered

Modification Rules:
- No overwrite or deletion may occur without explicit approval from the Creator (Zach).
- All modifications generate a new version, new hash, new ledger entry, and new OTS receipt.

Sync Rules:
- After approval, automation must:
  - Run the hashing pipeline
  - Update journals
  - Update glossaries
  - Run contradiction audit
  - Commit and push to GitHub
  - Verify GitHub matches local state

Governance:
This capsule defines the constitutional automation layer for the ZNON-Ledger and must be referenced by all future automation modules.

