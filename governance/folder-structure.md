# Folder Governance Capsule — Audit Binder Structure

Purpose:
To define the canonical folder structure of the ZNON-Ledger and prevent structural drift.

Canonical Structure:

/glossary/master/        (Creator-Level Only)
/glossary/znon/          (Tier-Filtered)
/glossary/medstrate/     (Medstrate-Tier)
/glossary/mpaa/          (User-Visible)
/glossary/mplex/         (Creator-Level)

/journals/master/        (Innovation Log)
/journals/znon/          (Language Layer Log)
/journals/medstrate/     (Healthcare/Forensic Log)
/journals/mpaa/          (Audit Layer Log)

/specs/                  (Identity, Capsule, and Protocol Specs)
/receipts/               (OTS Receipts)
/ledger/                 (Anchored Ledger Entries)

Rules:
- No folder may be renamed, removed, or relocated without explicit Creator approval.
- All new files must be placed in the correct folder according to category.
- Automation must verify folder placement before anchoring.
- Any drift triggers an immediate halt and alert.

Governance:
This capsule defines the constitutional folder layout for the ZNON-Ledger and must be referenced by all future automation modules.

