import os
import subprocess
from datetime import datetime

"""
PURPOSE: Mass-minting of Sovereign Sensors with absolute timestamping.
SUBSTRATE_VERSION: v1.1.1
"""

def mint_sensor(sensor_id, name, explanation, use_case, application):
    repo_root = os.path.expanduser("~/ZNON-Ledger")
    registry_file = os.path.join(repo_root, "core/sensors/SENSOR_REGISTRY.md")
    jnon_path = os.path.join(repo_root, f"core/registry/sensor_{sensor_id}.jnon")
    
    # Create JNON
    jnon_content = f'{{\n  "sensor_id": "{sensor_id}",\n  "name": "{name}",\n  "explanation": "{explanation}",\n  "use_case": "{use_case}",\n  "application": "{application}",\n  "sealed": "{datetime.now().isoformat()}"\n}}'
    with open(jnon_path, "w") as f: f.write(jnon_content)
    
    # Update Markdown Table
    table_row = f"| **{name}** | `{sensor_id}` | {explanation} | {use_case} | {application} |\n"
    with open(registry_file, "a") as f: f.write(table_row)
    
    # Lunatic Stamping
    subprocess.run(["ots", "stamp", jnon_path])
    subprocess.run(["ots", "stamp", registry_file])
    print(f"✅ Sensor {sensor_id} ({name}) Minted and Anchored.")

if __name__ == "__main__":
    # BATCH RUN: The First 5 Sensors
    sensors = [
        ("ZSS-001", "Semantic Anchor", "Ensures terms stay within Glossary bounds", "Audit Parity", "Check via Term #858"),
        ("ZSS-002", "Temporal Drift", "Detects outdated/hallucinated timelines", "Fact Checking", "Anchor Sync"),
        ("ZSS-003", "Paradox Immunity", "Identifies logical contradictions", "Logic Auditing", "Law #1 Apply"),
        ("ZSS-004", "Contextual Siphon", "Detects info leakage between domains", "Security", "Dual-Pane Isolation"),
        ("ZSS-005", "Vibe-Check Sensor", "Detects conversational 'fluff' vs data", "Accuracy", "JNON Structure Check")
    ]
    for s_id, s_name, s_exp, s_use, s_app in sensors:
        mint_sensor(s_id, s_name, s_exp, s_use, s_app)
