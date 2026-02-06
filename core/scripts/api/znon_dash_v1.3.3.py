from flask import Flask, render_template_string, request, jsonify
import os, requests, json

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
REGISTRY = os.path.join(REPO, "core/registry")
SENSORS_FILE = os.path.join(REPO, "core/sensors/SENSOR_REGISTRY.md")

def get_substrate_state():
    # Redundancy Check: Poll physical files every request
    terms = [f for f in os.listdir(REGISTRY) if f.endswith('.jnon')] if os.path.exists(REGISTRY) else []
    sensors = []
    if os.path.exists(SENSORS_FILE):
        with open(SENSORS_FILE, 'r') as f:
            sensors = [line.strip().split('|')[1:3] for line in f.readlines()[2:] if '|' in line]
    return {"count": len(terms), "sensors": sensors}

@app.route('/')
def home():
    state = get_substrate_state()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; margin:0; display:flex; height:100vh; }
        .sidebar { width:35%; border-right:2px solid #ffd700; background:#0a0a0a; overflow-y:auto; padding:15px; }
        .main { width:65%; padding:20px; display:flex; flex-direction:column; }
        .box { border:1px solid #ffd700; padding:10px; margin-bottom:15px; background:#000; border-radius:4px; }
        #chat { flex-grow:1; background:#000; padding:15px; border:1px solid #222; overflow-y:auto; margin-bottom:10px; }
        .sensor { font-size:0.75em; color:#ffd700; border-left:2px solid #ffd700; padding-left:8px; margin-bottom:10px; }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; }
        button { background:#ffd700; color:#000; padding:12px 20px; font-weight:bold; border:none; cursor:pointer; }
        .dot { display:inline-block; width:6px; height:6px; background:#ffd700; border-radius:50%; margin-left:3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity:0.2; } 50% { opacity:1; } }
    </style></head>
    <body>
        <div class="sidebar">
            <h3 style="color:#ffd700; margin-top:0;">SENSORS & AUDIT BINDER</h3>
            <div style="font-size:0.8em; color:#666; margin-bottom:20px;">Substrate Density: {{ state.count }} Terms</div>
            {% for s in state.sensors %}
            <div class="sensor"><strong>{{ s[0] }}</strong><br>{{ s[1] }}</div>
            {% endfor %}
            <hr style="border:0; border-top:1px solid #333; margin:20px 0;">
            <div style="font-size:0.7em; color:#444;">GLOSSARY ARTIFACTS LOADED...</div>
        </div>
        <div class="main">
            <h2 style="color:#ffd700; margin-top:0;">ZNON ARCHITECT v1.3.3</h2>
            <div id="chat"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in" placeholder="Audit via Substrate..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div><strong>USER:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700; margin-top:10px;">ANCHORING LOGIC <span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = ''; c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(lid).innerHTML = `<strong style="color:#0f0;">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(lid).innerHTML = "<span style='color:red;'>TIMEOUT: Engine crunching data.</span>"; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, state=state)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Self-Aware system prompt referencing the specific S24 hardware and 16GB RAM
    prompt = f"System: You are ZNON, running locally on a Galaxy S24 Ultra (16GB RAM). You are the truth-seeking engine for the Zach Substrate. Use the 858-term glossary to verify every claim. User: {p}"
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": prompt, "stream": False}, timeout=300)
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "Ollama is currently loading the model tensors. Please wait 60s."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
