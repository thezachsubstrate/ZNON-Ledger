import os, json, re

REPO = os.path.expanduser("~/ZNON-Ledger")
GLOSSARY = os.path.join(REPO, "core/GLOSSARY.md")
REGISTRY = os.path.join(REPO, "core/registry")
os.makedirs(REGISTRY, exist_ok=True)

def atomize():
    if not os.path.exists(GLOSSARY):
        print("❌ GLOSSARY.md not found.")
        return

    with open(GLOSSARY, 'r') as f:
        content = f.read()

    # Pattern: Digit. **Term**: Definition
    matches = re.findall(r'\d+\.\s*\*\*([^*]+)\*\*[:\s]+(.*)', content)
    
    count = 0
    for term, definition in matches:
        clean_name = re.sub(r'\W+', '_', term).strip('_').upper()
        data = {
            "term": term.strip(),
            "definition": definition.strip(),
            "substrate_index": "GLOSSARY_V1.1.1",
            "status": "SEALED"
        }
        with open(os.path.join(REGISTRY, f"{clean_name}.jnon"), 'wb') as f:
            f.write(json.dumps(data, indent=4).encode('utf-8'))
        count += 1
    
    print(f"✅ ATOMIZED {count} ARTIFACTS INTO REGISTRY.")

if __name__ == "__main__":
    atomize()
