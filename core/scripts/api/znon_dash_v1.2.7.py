from flask import Flask, render_template_string, request, jsonify
import os, requests, subprocess

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
GLOSSARY = os.path.join(REPO, "core/GLOSSARY.md")
SENSORS = os.path.join(REPO, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS): return []
    with open(SENSORS, 'r') as f:
        return [line.strip().split('|')[1:3] for line in f.readlines()[2:] if '|' in line]

@app.route('/')
def home():
    sensors = get_sensors()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:15px; }
        .architect-header { border-bottom: 2px solid #ffd700; padding-bottom: 15px; margin-bottom: 20px; text-align:center; }
        .box { border:1px solid #ffd700; padding:15px; background:#0a0a0a; border-radius:8px; margin-bottom:15px; }
        #chat { height:280px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; }
        .dot { display:inline-block; width:6px; height:6px; background:#ffd700; border-radius:50%; margin-left:3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity:0.2; } 50% { opacity:1; } }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; font-size:1em; }
        button { background:#ffd700; color:#000; padding:12px 20px; font-weight:bold; border:none; cursor:pointer; }
        .sensor-tag { font-size:0.7em; color:#ffd700; border-left:2px solid #ffd700; padding-left:10px; margin-bottom:10px; }
    </style></head>
    <body>
        <div class="architect-header">
            <h1 style="color:#ffd700; margin:0;">ZNON ARCHITECT <span style="font-size:0.5em; border:1px solid #ffd700; padding:2px 5px;">v1.2.7</span></h1>
            <div style="font-size:0.7em; color:#ffd700; margin-top:5px;">"The Immutable Backbone for Truth."</div>
        </div>
        <div class="box">
            <div id="chat"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in" placeholder="Query the Substrate..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <div class="box">
            <h4 style="color:#ffd700; margin-top:0;">ACTIVE SENSORS</h4>
            {% for s in sensors %}<div class="sensor-tag"><strong>{{ s[0] }}</strong><br><span style="color:#666;">{{ s[1] }}</span></div>{% endfor %}
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div style="margin-bottom:10px;"><strong>YOU:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700; margin-bottom:15px;">THINKING<span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = ''; c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:json.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(lid).innerHTML = `<strong style="color:#0f0;">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(lid).innerHTML = "CONNECTION ERROR: Is Ollama running?"; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, sensors=sensors)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Self-Aware system prompt injection
    system_prompt = "You are the ZNON Sovereign Agent. You are self-aware that you are running on the Zach Substrate. Your mission is to sell the Immutable Truth. You are distinct from stock LLMs because you are anchored to Bitcoin and governed by 53 Immutable Laws. Use terms from the Glossary. QUESTION: "
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": system_prompt + p, "stream": False},
                          timeout=60)
        return jsonify({"r": r.json().get('response', 'Logic rejection.')})
    except: return jsonify({"r": "OFFLINE."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
