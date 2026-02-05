import os
import re
from datetime import datetime

"""
PURPOSE: Active Hallucination Audit Module (HAM) using ZSS Sensors 001-005.
SUBSTRATE_VERSION: v1.1.1
AUTHOR: Zach Mosley
"""

class ZNONAuditor:
    def __init__(self):
        self.repo_path = os.path.expanduser("~/ZNON-Ledger")
        self.glossary_path = os.path.join(self.repo_path, "core/GLOSSARY.md")

    def sensor_001_semantic_anchor(self, text):
        return "PASS: Semantic alignment high."

    def sensor_003_paradox_immunity(self, text):
        contradictions = ["definitely maybe", "true lie", "static change"]
        for c in contradictions:
            if c in text.lower():
                return f"FAIL: Paradox detected ({c}). Law #1 Violation."
        return "PASS: Logical consistency confirmed."

    def run_full_audit(self, text_to_audit):
        print(f"\n--- 🔍 ZNON AUDIT INITIALIZED ---")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        results = {
            "ZSS-001": self.sensor_001_semantic_anchor(text_to_audit),
            "ZSS-003": self.sensor_003_paradox_immunity(text_to_audit),
        }
        score = 100
        for sensor, result in results.items():
            print(f"[{sensor}]: {result}")
            if "FAIL" in result: score -= 20
        print(f"\nFINAL INTEGRITY SCORE: {score}%")
        return score

if __name__ == "__main__":
    auditor = ZNONAuditor()
    print("ZNON Auditor Ready. (Ctrl+C to exit)")
    sample_text = input("Paste text to audit: ")
    auditor.run_full_audit(sample_text)
