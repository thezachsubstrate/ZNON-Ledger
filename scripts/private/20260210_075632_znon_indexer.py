import os
import json
import datetime
import hashlib

def get_id(p):
    try:
        h = hashlib.sha256()
        with open(p, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except:
        return "UNKNOWN"

def run_indexer():
    print("Initiating ZNON Jurisdimensional Scan...")
    manifest = {
        "metadata": {
            "ver": "3.6", 
            "node": "Samsung_Termux", 
            "ts": str(datetime.datetime.now())
        }, 
        "modules": {m: [] for m in ["MedStrate", "Legistrate", "Bankstrate", "Bizstrate", "Fitstrate", "Artstrate", "Homestrate", "Techstrate"]}, 
        "unmapped": []
    }

    for r, d, f in os.walk("."):
        if ".git" in r: continue
        for file in f:
            p = os.path.join(r, file)
            mapped = False
            for m in manifest["modules"]:
                if m.lower() in p.lower():
                    manifest["modules"][m].append({
                        "p": p, 
                        "id": get_id(p), 
                        "ots": os.path.exists(p + ".ots")
                    })
                    mapped = True
                    break
            if not mapped:
                manifest["unmapped"].append(p)

    with open("ZNON_INDEX.json", "w") as f:
        json.dump(manifest, f, indent=4)

    with open("ZNON_DASHBOARD.md", "w") as d:
        d.write(f"# 🏛️ ZNON SOVEREIGN DASHBOARD\n")
        d.write(f"**State Lock:** `{manifest['metadata']['ts']}`\n\n")
        for m, items in manifest["modules"].items():
            d.write(f"### 📦 {m}\n")
            if not items:
                d.write("_Empty_\n")
            else:
                for i in items[:15]:
                    status = '✅' if i['ots'] else '⚠️'
                    d.write(f"- `{i['p']}` | ID: `{i['id']}` | {status}\n")
        d.write(f"\n### 🔍 UNMAPPED COUNT: {len(manifest['unmapped'])}\n")

    print(f"\nSUCCESS: Audit Binder Created.")
    print(f"Mapped files: {sum(len(v) for v in manifest['modules'].values())}")
    print(f"Unmapped files: {len(manifest['unmapped'])}")

if __name__ == "__main__":
    run_indexer()

