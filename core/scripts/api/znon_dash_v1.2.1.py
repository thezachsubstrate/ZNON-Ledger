from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import os, subprocess, requests

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")
SENSORS_FILE = os.path.join(REPO_PATH, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        lines = f.readlines()[2:]
        return [line.strip().split('|')[1:5] for line in lines if '|' in line]

def check_integrity():
    files = [f for f in os.listdir(REGISTRY_PATH) if f.endswith('.jnon')]
    return [f for f in files if not os.path.exists(os.path.join(REGISTRY_PATH, f + ".ots"))]

@app.route('/')
def home():
    unanchored = check_integrity()
    sensors = get_sensors()
    return render_template_string("""
    <!DOCTYPE html>
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root { --gold: #ffd700; --bg: #050505; --glass: rgba(255, 215, 0, 0.05); }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: #e0e0e0; margin: 0; padding: 20px; }
        .architect-shell { max-width: 800px; margin: auto; border: 1px solid #222; border-radius: 12px; overflow: hidden; background: #0a0a0a; box-shadow: 0 0 30px rgba(0,0,0,1); }
        .nav-tiers { display: flex; background: #111; border-bottom: 1px solid #222; }
        .tier { flex: 1; padding: 12px; text-align: center; font-size: 0.7em; color: #555; border-right: 1px solid #222; cursor: not-allowed; }
        .tier.active { color: var(--gold); border-bottom: 2px solid var(--gold); background: var(--glass); cursor: default; }
        
        .header { padding: 30px; text-align: left; background: linear-gradient(135deg, #0a0a0a 0%, #151515 100%); border-bottom: 1px solid #222; }
        .substrate-label { font-size: 0.6em; letter-spacing: 4px; color: var(--gold); opacity: 0.6; text-transform: uppercase; }
        
        .content-grid { display: grid; grid-template-columns: 1fr 300px; gap: 1px; background: #222; }
        @media (max-width: 600px) { .content-grid { grid-template-columns: 1fr; } }
        
        .main-panel { background: #0a0a0a; padding: 20px; }
        .side-panel { background: #0d0d0d; padding: 20px; font-size: 0.8em; }
        
        #chat-window { height: 350px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding: 10px; background: #050505; border: 1px solid #1a1a1a; margin-bottom: 15px; border-radius: 4px; }
        .msg { padding: 8px 12px; border-radius: 4px; max-width: 85%; line-height: 1.4; }
        .msg.user { align-self: flex-end; background: var(--gold); color: #000; font-weight: bold; }
        .msg.ai { align-self: flex-start; background: #1a1a1a; border: 1px solid #333; color: #0f0; font-family: 'Courier New', monospace; }
        
        .input-area { display: flex; gap: 5px; }
        input { flex: 1; background: #000; border: 1px solid #333; color: #fff; padding: 12px; border-radius: 4px; }
        input:focus { border-color: var(--gold); outline: none; }
        button.send-btn { background: var(--gold); color: #000; border: none; padding: 0 20px; font-weight: bold; border-radius: 4px; cursor: pointer; }
        
        .sensor-card { background: #111; padding: 10px; border-radius: 4px; margin-bottom: 8px; border-left: 2px solid var(--gold); }
        .status-dot { height: 6px; width: 6px; background: #0f0; border-radius: 50%; display: inline-block; margin-right: 5px; }
    </style></head>
    <body>
        <div class="architect-shell">
            <div class="nav-tiers">
                <div class="tier active">SOVEREIGN (L3)</div>
                <div class="tier">CITIZEN (L2)</div>
                <div class="tier">OBSERVER (L1)</div>
            </div>
            
            <div class="header">
                <div class="substrate-label">The Zach Substrate</div>
                <h1 style="margin: 5px 0 0 0; color: #fff; font-weight: 200;">ZNON ARCHITECT <span style="font-size:0.4em; border: 1px solid var(--gold); color: var(--gold); padding: 2px 5px; vertical-align: middle; margin-left: 10px;">v1.2.1</span></h1>
            </div>

            <div class="content-grid">
                <div class="main-panel">
                    <div id="chat-window">
                        <div class="msg ai">SYSTEM READY: Laws & Glossary ingested. No onboarding required. Waiting for logical input...</div>
                    </div>
                    <div class="input-area">
                        <input type="text" id="userInput" placeholder="Execute logic audit...">
                        <button class="send-btn" onclick="send()">RUN</button>
                    </div>
                </div>

                <div class="side-panel">
                    <div style="color: var(--gold); font-size: 0.7em; margin-bottom: 15px; letter-spacing: 1px;">ACTIVE SENSORS</div>
                    {% for s in sensors %}
                    <div class="sensor-card">
                        <div style="font-size: 0.9em;"><span class="status-dot"></span>{{ s[0] }}</div>
                        <div style="font-size: 0.7em; color: #666; margin-top: 3px;">{{ s[1] }}</div>
                    </div>
                    {% endfor %}
                    
                    {% if unanchored %}
                    <div style="margin-top: 20px; padding: 10px; border: 1px solid #f55; background: rgba(245, 85, 85, 0.1); border-radius: 4px;">
                        <div style="color: #f55; font-size: 0.7em; font-weight: bold;">INTEGRITY GAP</div>
                        <div style="font-size: 1.2em; color: #fff;">{{ unanchored|length }}</div>
                        <form action="/anchor" method="POST"><button type="submit" style="background:#f55; color:#fff; border:none; width:100%; margin-top:8px; font-size:0.7em; padding:5px;">REPAIR SUBSTRATE</button></form>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <script>
            async function send() {
                const input = document.getElementById('userInput');
                const chat = document.getElementById('chat-window');
                const text = input.value;
                if(!text) return;

                chat.innerHTML += `<div class="msg user">${text}</div>`;
                input.value = '';
                chat.scrollTop = chat.scrollHeight;

                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({prompt: text})
                    });
                    const data = await res.json();
                    chat.innerHTML += `<div class="msg ai">${data.reply}</div>`;
                } catch (e) {
                    chat.innerHTML += `<div class="msg ai" style="color: #f55;">ERROR: Engine timeout. Ensure 'ollama serve' is active.</div>`;
                }
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body></html>
    """, unanchored=unanchored, sensors=sensors)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    try:
        # Increased timeout to 60s for local mobile processing
        res = requests.post("http://localhost:11434/api/generate", 
                            json={"model": "znon-agent", "prompt": prompt, "stream": False},
                            timeout=60)
        return jsonify({"reply": res.json().get('response', 'Logic rejection: Engine returned empty.')})
    except Exception as e:
        return jsonify({"reply": f"CONNECTION_REFUSED: {str(e)}"})

@app.route('/anchor', methods=['POST'])
def anchor():
    for f in check_integrity(): subprocess.run(["ots", "stamp", os.path.join(REGISTRY_PATH, f)])
    return redirect(url_for('home'))

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
