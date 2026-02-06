import os, json, re

REPO = os.path.expanduser("~/ZNON-Ledger")
# Target the specific V1.1.1 file you mentioned
GLOSSARY = os.path.join(REPO, "core/GLOSSARY.md") 
REGISTRY = os.path.join(REPO, "core/registry")
os.makedirs(REGISTRY, exist_ok=True)

def atomize():
    if not os.path.exists(GLOSSARY):
        print(f"❌ File not found: {GLOSSARY}")
        return

    with open(GLOSSARY, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    count = 0
    # Logic: Look for lines with pipes | indicating table rows
    for line in lines:
        if '|' in line and '---' not in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                term = parts[0]
                definition = parts[1]
                
                # Skip the Header row
                if term.lower() == "term": continue
                
                clean_filename = re.sub(r'\W+', '_', term).upper() + ".jnon"
                data = {
                    "term": term,
                    "definition": definition,
                    "source": "GLOSSARY_V1.1.1",
                    "status": "SEALED"
                }
                
                with open(os.path.join(REGISTRY, clean_filename), 'w') as jf:
                    json.dump(data, jf, indent=4)
                count += 1
    
    print(f"✅ SUCCESS: {count} terms atomized into {REGISTRY}")

if __name__ == "__main__":
    atomize()
