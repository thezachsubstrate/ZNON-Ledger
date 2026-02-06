from flask import Flask, render_template_string, request, jsonify
import os, requests, subprocess

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
SENSORS_FILE = os.path.join(REPO, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        return [line.strip().split('|')[1:3] for line in f.readlines()[2:] if '|' in line]

@app.route('/')
def home():
    sensors = get_sensors()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:20px; }
        .header { text-align: center; border-bottom: 2px solid #ffd700; padding-bottom: 10px; margin-bottom: 20px; }
        .box { border:1px solid #ffd700; padding:15px; margin-bottom:15px; background:#0a0a0a; border-radius:8px; }
        #chat { height:250px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; border-radius:4px; }
        .dot { display:inline-block; width:6px; height:6px; background:#ffd700; border-radius:50%; margin-left:3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity:0.2; } 50% { opacity:1; } }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:10px; font-size: 1em; }
        button { background:#ffd700; color:#000; padding:10px 20px; font-weight:bold; border:none; cursor:pointer; border-radius:4px; }
    </style></head>
    <body>
        <div class="header">
            <h1 style="color: #ffd700; margin:0; font-size: 1.5em;">ZNON ARCHITECT <span style="font-size:0.5em; border:1px solid #ffd700; padding:2px 5px;">v1.2.4</span></h1>
            <div style="font-size: 0.7em; color: #ffd700; margin-top:5px;">"The Immutable Backbone for Truth."</div>
        </div>
        <div class="box">
            <div id="chat"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in" placeholder="Execute logic audit..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <div class="box">
            <div style="color:#ffd700; font-size:0.8em; margin-bottom:10px;">ACTIVE SENSOR REGISTRY</div>
            {% for s in sensors %}
            <div style="font-size:0.7em; margin-bottom:8px; border-left: 2px solid #ffd700; padding-left:10px;">
                <strong>{{ s[0] }}</strong><br><span style="color:#666;">{{ s[1] }}</span>
            </div>
            {% endfor %}
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div style="margin-bottom:10px;"><strong>YOU:</strong> ${txt}</div>`;
                const loadId = "load-" + Date.now();
                c.innerHTML += `<div id="${loadId}" style="color:#ffd700; margin-bottom:15px;">ANALYZING <span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = '';
                c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(loadId).innerHTML = `<strong style="color:#0f0;">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(loadId).innerHTML = "<span style='color:red;'>ERROR: Connection timeout.</span>"; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, sensors=sensors)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model":"znon-agent","prompt":p,"stream":False}, timeout=60)
        return jsonify({"r": r.json().get('response', 'Logic Rejection.')})
    except Exception as e: return jsonify({"r": f"OFFLINE: {str(e)}"})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
