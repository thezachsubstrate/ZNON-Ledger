from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
GLOSSARY_FILE = os.path.join(REPO, "core/GLOSSARY.md")

def count_glossary_terms():
    try:
        with open(GLOSSARY_FILE, 'r') as f:
            return len([l for l in f.readlines() if '|' in l]) - 2 # Subtracting headers
    except: return 0

@app.route('/')
def home():
    density = count_glossary_terms()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:20px; }
        .header { border-bottom: 2px solid #ffd700; padding-bottom:10px; margin-bottom:20px; }
        .box { border:1px solid #ffd700; padding:15px; background:#0a0a0a; border-radius:8px; margin-bottom:15px; }
        #chat { height:250px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; }
        .dot { display:inline-block; width:6px; height:6px; background:#ffd700; border-radius:50%; margin-left:3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity:0.2; } 50% { opacity:1; } }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:10px; }
        button { background:#ffd700; color:#000; padding:10px 20px; font-weight:bold; border:none; cursor:pointer; }
    </style></head>
    <body>
        <div class="header">
            <h1 style="color:#ffd700; margin:0;">ZNON ARCHITECT v1.2.6</h1>
            <div style="color:#ffd700; font-size:0.7em;">SUBSTRATE DENSITY: {{ density }} TERMS DETECTED</div>
        </div>
        <div class="box">
            <div id="chat"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in" placeholder="Query the 855+ Logic Terms..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div>YOU: ${txt}</div><div id="loading">THINKING<span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = '';
                c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById('loading').remove();
                    c.innerHTML += `<div style="color:#0f0;">ZNON: ${data.r}</div>`;
                } catch { document.getElementById('loading').innerHTML = "TIMEOUT: Engine crunching heavy glossary data..."; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, density=density)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    r = requests.post("http://localhost:11434/api/generate", json={"model":"znon-agent","prompt":p,"stream":False}, timeout=60)
    return jsonify({"r": r.json().get('response', 'Logic rejection.')})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
