import os
import subprocess
from datetime import datetime

"""
PURPOSE: Mass-minting with Version-Baked Filenames for OTS Collision Resistance.
SUBSTRATE_VERSION: v1.1.2
AUTHOR: Zach Mosley
"""

def mint_sensor(sensor_id, name, explanation, use_case, application, version="1.1.2"):
    repo_root = os.path.expanduser("~/ZNON-Ledger")
    registry_file = os.path.join(repo_root, "core/sensors/SENSOR_REGISTRY.md")
    
    # NEW PROTOCOL: Version-Baked Filename
    jnon_filename = f"sensor_{sensor_id}_v{version}.jnon"
    jnon_path = os.path.join(repo_root, f"core/registry/{jnon_filename}")
    
    jnon_content = f'{{\n  "sensor_id": "{sensor_id}",\n  "name": "{name}",\n  "explanation": "{explanation}",\n  "use_case": "{use_case}",\n  "application": "{application}",\n  "version": "{version}",\n  "sealed": "{datetime.now().isoformat()}"\n}}'
    
    with open(jnon_path, "w") as f: f.write(jnon_content)
    
    # Update Registry Table
    table_row = f"| **{name}** | `{sensor_id}` | {explanation} | {use_case} | v{version} |\n"
    with open(registry_file, "a") as f: f.write(table_row)
    
    # Stamping
    subprocess.run(["ots", "stamp", jnon_path])
    print(f"✅ Minted & Version-Baked: {jnon_filename}")

if __name__ == "__main__":
    # Test batch run for ZSS-006 to ZSS-015
    sensors = [
        ("ZSS-006", "Semantic Leakage", "Detects bias overrides", "Bias", "Law #3"),
        ("ZSS-007", "Citation Anchor", "Fact checks sources", "Fact Check", "Cross-Ref"),
        ("ZSS-008", "Recursive Logic Check", "Detects circular reasoning", "Logic", "Loop Break"),
        ("ZSS-009", "Tone Policing Sensor", "Filters manipulation", "Audit", "Neutrality"),
        ("ZSS-010", "Probability Drift", "Detects guessing", "Certainty", "Law #12"),
        ("ZSS-011", "Structural First Audit", "Identifies novelty", "Innovation", "ZNVP Filter"),
        ("ZSS-012", "Contextual Siphon v2", "Deep isolation", "Security", "Dual-Pane v2"),
        ("ZSS-013", "Ghost Path Detection", "Finds broken paths", "Debug", "Path Verify"),
        ("ZSS-014", "Hype-to-Truth Ratio", "Raw data density", "Metric", "Density Check"),
        ("ZSS-015", "Root Author Sensor", "Identity alignment", "Identity", "Law #0 Sync")
    ]
    for s_id, s_name, s_exp, s_use, s_app in sensors:
        mint_sensor(s_id, s_name, s_exp, s_use, s_app)
