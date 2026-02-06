import os

# ZNON Path Audit - v1.1.0
REPO_ROOT = os.path.expanduser("~/ZNON-Ledger")
TARGET_FOLDER = "AI-Agent-Onboarding-Protocol"
REQUIRED_ARTIFACT = "AI_AGENT_ONBOARDINGv1.1.2.txt"

def run_audit():
    full_path = os.path.join(REPO_ROOT, TARGET_FOLDER)
    
    print(f"[ZNON] Commencing Path Audit for: {TARGET_FOLDER}")
    
    # 1. Physical Existence Check
    if not os.path.exists(full_path):
        print(f"❌ FAIL: Directory {TARGET_FOLDER} is missing from Substrate.")
        return

    # 2. Lineage v1.1.2 Integrity Check
    artifact_path = os.path.join(full_path, REQUIRED_ARTIFACT)
    if os.path.exists(artifact_path):
        print(f"✅ PASS: {REQUIRED_ARTIFACT} located in Protocol folder.")
        
        # 3. Cryptographic Stamp Audit
        if os.path.exists(f"{artifact_path}.ots"):
            print(f"✅ PASS: 9-Sigma OTS stamp detected for v1.1.2.")
        else:
            print(f"⚠️ WARNING: Artifact present but missing cryptographic finality (.ots).")
    else:
        print(f"❌ FAIL: {REQUIRED_ARTIFACT} not found in the designated path.")

    # 4. Archive Visibility Check
    archive_path = os.path.join(full_path, "archive")
    if os.path.exists(archive_path) and os.listdir(archive_path):
        print(f"✅ PASS: Legacy lineage archived in {TARGET_FOLDER}/archive/.")
    else:
        print(f"⚠️ WARNING: Archive subfolder is empty or missing.")

if __name__ == "__main__":
    run_audit()
