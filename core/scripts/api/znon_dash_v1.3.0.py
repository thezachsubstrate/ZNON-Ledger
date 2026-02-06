from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
SENSORS_FILE = os.path.join(REPO, "core/sensors/SENSOR_REGISTRY.md")
REGISTRY_DIR = os.path.join(REPO, "core/registry")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        return [line.strip().split('|')[1:3] for line in f.readlines()[2:] if '|' in line]

def get_term_count():
    return len([f for f in os.listdir(REGISTRY_DIR) if f.endswith('.jnon')])

@app.route('/')
def home():
    sensors = get_sensors()
    count = get_term_count()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:15px; }
        .box { border:1px solid #ffd700; padding:15px; background:#0a0a0a; border-radius:8px; margin-bottom:15px; }
        #chat { height:250px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; }
        .dot { display:inline-block; width:6px; height:6px; background:#ffd700; border-radius:50%; margin-left:3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity:0.2; } 50% { opacity:1; } }
        input { width:65%; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; }
        button { background:#ffd700; color:#000; padding:12px; font-weight:bold; border:none; cursor:pointer; }
    </style></head>
    <body>
        <h2 style="color:#ffd700; text-align:center; margin:0;">ZNON ARCHITECT v1.3.0</h2>
        <p style="color:#ffd700; text-align:center; font-size:0.8em;">Substrate Density: {{ count }} Terms</p>
        <div class="box">
            <div id="chat"></div>
            <div style="display:flex; gap:5px;">
                <input type="text" id="in" placeholder="Audit Logic..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <div class="box">
            <h4 style="color:#ffd700; margin:0 0 10px 0;">ACTIVE SENSORS</h4>
            {% for s in sensors %}
            <div style="font-size:0.7em; border-left:2px solid #ffd700; padding-left:10px; margin-bottom:5px;">
                <strong>{{ s[0] }}</strong>: {{ s[1] }}
            </div>
            {% endfor %}
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div>YOU: ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700;">ZNON THINKING <span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = ''; c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(lid).innerHTML = `<strong style="color:#0f0;">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(lid).innerHTML = "<span style='color:red;'>TIMEOUT: Model Loading... Wait 30s.</span>"; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, sensors=sensors, count=count)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Self-Awareness logic
    prompt = f"System: You are ZNON, running on the Zach Substrate. Sell the truth. Explain why your 858 glossary terms make you more consistent than other AI. User: {p}"
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": prompt, "stream": False}, timeout=300)
        return jsonify({"r": r.json().get('response', 'Logic Rejection.')})
    except: return jsonify({"r": "Ollama is warming up. Please wait."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
