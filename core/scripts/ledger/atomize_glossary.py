import os, json, re

REPO = os.path.expanduser("~/ZNON-Ledger")
GLOSSARY = os.path.join(REPO, "core/GLOSSARY.md")
REGISTRY = os.path.join(REPO, "core/registry")
os.makedirs(REGISTRY, exist_ok=True)

def atomize():
    if not os.path.exists(GLOSSARY):
        print("❌ Glossary not found.")
        return

    with open(GLOSSARY, 'r') as f:
        content = f.read()

    # Regex to find "Term: Definition" or "| Term | Definition |"
    # Adjusting for your specific V1.1.1 format
    terms = re.findall(r'\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|', content)
    
    count = 0
    for term, definition in terms:
        if "Term" in term or "---" in term: continue # Skip headers
        
        clean_term = term.strip().replace(" ", "_").upper()
        data = {
            "term": term.strip(),
            "definition": definition.strip(),
            "substrate_index": "GLOSSARY_V1.1.1",
            "integrity_sealed": False
        }
        
        with open(os.path.join(REGISTRY, f"{clean_term}.jnon"), 'w') as jf:
            json.dump(data, jf, indent=4)
        count += 1
    
    print(f"✅ Atomized {count} terms into JNON artifacts.")

if __name__ == "__main__":
    atomize()
