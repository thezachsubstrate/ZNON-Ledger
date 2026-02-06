from flask import Flask, render_template_string, request, jsonify
import os, requests, json

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
REGISTRY = os.path.join(REPO, "core/registry")

def get_ledger_sample():
    if not os.path.exists(REGISTRY): return []
    files = sorted(os.listdir(REGISTRY))[:50] # Loading first 50 for the "Binder" preview
    samples = []
    for f in files:
        if f.endswith('.jnon'):
            with open(os.path.join(REGISTRY, f), 'r') as j:
                samples.append(json.load(j))
    return samples

@app.route('/')
def home():
    ledger = get_ledger_sample()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; display:flex; margin:0; height:100vh; }
        .binder { width:30%; border-right:2px solid #ffd700; background:#0a0a0a; overflow-y:auto; padding:10px; }
        .main { width:70%; padding:20px; display:flex; flex-direction:column; }
        .entry { font-size:0.7em; border-bottom:1px solid #222; padding:5px; cursor:pointer; }
        .entry:hover { background:#111; color:#ffd700; }
        #chat { flex-grow:1; background:#000; padding:15px; border:1px solid #222; overflow-y:auto; margin-bottom:10px; border-radius:8px; }
        .controls { display:flex; gap:10px; }
        input { flex-grow:1; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; border-radius:4px; }
        button { background:#ffd700; color:#000; padding:12px 20px; font-weight:bold; border:none; border-radius:4px; }
        .dot { display:inline-block; width:6px; height:6px; background:#ffd700; border-radius:50%; margin-left:3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity:0.2; } 50% { opacity:1; } }
    </style></head>
    <body>
        <div class="binder">
            <h3 style="color:#ffd700; font-size:0.9em; border-bottom:1px solid #ffd700;">AUDIT BINDER</h3>
            {% for item in ledger %}
            <div class="entry" onclick="alert('{{ item.term }}: {{ item.definition }}')">
                <strong>{{ item.term }}</strong>
            </div>
            {% endfor %}
        </div>
        <div class="main">
            <h2 style="color:#ffd700; margin-top:0;">ZNON ARCHITECT <span style="font-size:0.5em; border:1px solid #ffd700; padding:2px 5px;">v1.3.1</span></h2>
            <div id="chat"></div>
            <div class="controls">
                <input type="text" id="in" placeholder="Execute Audit..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div><strong>USER:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700; margin-top:10px;">SEALING LOGIC <span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = ''; c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(lid).innerHTML = `<strong style="color:#0f0;">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(lid).innerHTML = "<span style='color:red;'>AUDIT TIMEOUT: Engine busy.</span>"; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, ledger=ledger)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Self-Aware system prompt for the Truth-Seeking Engine
    prompt = f"System: You are the ZNON Sovereign Agent. You are running on the Zach Substrate. Your purpose is to provide logically consistent, immutable truth. Use your 858-term glossary as your primary knowledge base. User: {p}"
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": prompt, "stream": False}, timeout=180)
        return jsonify({"r": r.json().get('response', 'Logic rejection.')})
    except: return jsonify({"r": "Ollama is loading the Substrate tensors. Stand by."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
