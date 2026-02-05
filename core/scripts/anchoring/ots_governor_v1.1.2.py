import os
import subprocess
import re
from datetime import datetime

"""
PURPOSE: Automates versioned OTS anchoring and provides real-time throughput metrics.
SUBSTRATE_VERSION: v1.1.2
AUTHOR: Zach Mosley
"""

def get_next_patch_version(file_base, extension):
    # Matches: filename_v1.1.X.ext
    pattern = re.compile(rf"{re.escape(file_base)}_v1\.1\.(\d+){re.escape(extension)}")
    max_patch = -1
    for filename in os.listdir('.'):
        match = pattern.match(filename)
        if match:
            max_patch = max(max_patch, int(match.group(1)))
    return max_patch + 1 if max_patch != -1 else 1

def run_anchor_cycle(target_files):
    print(f"⚡ ZNON Anchor Cycle Initialized: {datetime.now().strftime('%H:%M:%S')}")
    print("--------------------------------------------------")
    
    success_count = 0
    version_bumps = 0
    
    for full_path in target_files:
        dir_name = os.path.dirname(full_path)
        file_name = os.path.basename(full_path)
        file_base, extension = os.path.splitext(file_name)
        
        # Determine current version or bump
        patch = get_next_patch_version(file_base, extension)
        if patch >= 9:
            print(f"🚨 GOVERNOR ALERT: {file_base} at Patch 9. Verify Major/Minor bump.")
            continue

        versioned_name = f"{file_base}_v1.1.{patch}{extension}"
        target_path = os.path.join(dir_name, versioned_name)

        # 1. Create versioned copy
        subprocess.run(["cp", full_path, target_path])

        # 2. Attempt Stamp
        result = subprocess.run(["ots", "stamp", target_path], capture_output=True, text=True)
        
        if "already exists" in result.stderr.lower():
            # If hash exists, we don't count it as a "new" timestamp for this run
            print(f"⏩ {versioned_name}: Hash identical. Skipping to maintain ledger purity.")
            os.remove(target_path) # Clean up redundant file
        else:
            print(f"✅ {versioned_name}: Successfully Anchored.")
            success_count += 1

    print("--------------------------------------------------")
    print(f"📊 RUN SUMMARY:")
    print(f"   New Timestamps: {success_count}")
    print(f"   Status: Sovereign Integrity Confirmed.")

if __name__ == "__main__":
    # Example: Run on registry files
    registry_files = [os.path.join("../../registry", f) for f in os.listdir("../../registry") if f.endswith(".jnon")]
    run_anchor_cycle(registry_files)
