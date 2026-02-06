from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import os, subprocess, requests, shutil
from datetime import datetime

# --- AUTOMATIC SCRIPT ARCHIVAL (ZSS-016 COMPLIANCE) ---
def archive_self():
    src = __file__
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_dir = os.path.expanduser("~/ZNON-Ledger/.private/script_ledger")
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, f"znon_dash_v1.2.2_{timestamp}.py")
    shutil.copy2(src, dest_path)
    # Attempt to anchor the archival copy
    subprocess.run(["ots", "stamp", dest_path], capture_output=True)

archive_self() # Seal this version before serving

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")
SENSORS_FILE = os.path.join(REPO_PATH, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        lines = f.readlines()[2:]
        return [line.strip().split('|')[1:5] for line in lines if '|' in line]

@app.route('/')
def home():
    sensors = get_sensors()
    return render_template_string("""
    <!DOCTYPE html>
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root { --gold: #ffd700; --bg: #050505; --neon: #0f0; }
        body { font-family: 'Courier New', monospace; background: var(--bg); color: #e0e0e0; margin: 0; padding: 20px; }
        .shell { max-width: 900px; margin: auto; border: 1px solid #222; border-radius: 12px; background: #0a0a0a; box-shadow: 0 0 40px rgba(0,0,0,1); }
        .header { padding: 25px; border-bottom: 2px solid var(--gold); }
        .nav-tiers { display: flex; background: #111; font-size: 0.7em; }
        .tier { flex: 1; padding: 10px; text-align: center; border-right: 1px solid #222; color: #444; }
        .tier.active { color: var(--gold); border-bottom: 2px solid var(--gold); }
        
        .main-content { display: grid; grid-template-columns: 1fr 320px; gap: 1px; background: #222; }
        .panel { background: #0a0a0a; padding: 20px; }
        
        #chat-window { height: 350px; overflow-y: auto; background: #000; padding: 15px; border: 1px solid #1a1a1a; margin-bottom: 15px; }
        .msg { margin-bottom: 15px; padding: 10px; border-radius: 4px; line-height: 1.4; max-width: 90%; }
        .msg.user { background: var(--gold); color: #000; align-self: flex-end; margin-left: auto; }
        .msg.ai { background: #111; color: var(--neon); border-left: 3px solid var(--neon); }
        
        /* LOADING ANIMATION */
        .typing-dot { display: inline-block; width: 6px; height: 6px; background: var(--gold); border-radius: 50%; margin-right: 3px; animation: blink 1s infinite; }
        @keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }

        input { width: 75%; background: #000; border: 1px solid #333; color: #fff; padding: 12px; }
        button { background: var(--gold); color: #000; border: none; padding: 12px 20px; font-weight: bold; cursor: pointer; }
        
        .sensor-card { background: #0d0d0d; padding: 10px; margin-bottom: 8px; border-left: 2px solid var(--gold); font-size: 0.8em; }
    </style></head>
    <body>
        <div class="shell">
            <div class="nav-tiers">
                <div class="tier active">SOVEREIGN (L3)</div><div class="tier">CITIZEN (L2)</div><div class="tier">OBSERVER (L1)</div>
            </div>
            <div class="header">
                <span style="font-size: 0.6em; color: var(--gold); letter-spacing: 3px;">THE ZACH SUBSTRATE</span>
                <h1 style="margin:0; color:#fff;">ZNON ARCHITECT <span style="font-size:0.4em; border:1px solid var(--gold); padding:2px 5px; vertical-align:middle;">v1.2.2</span></h1>
                <div style="font-size: 0.7em; color: #666; margin-top: 5px;">The Immutable Backbone for Truth.</div>
            </div>
            <div class="main-content">
                <div class="panel">
                    <div id="chat-window"><div class="msg ai">SYSTEM READY: Laws & Glossary ingested. No onboarding required. Waiting for logical input...</div></div>
                    <div style="display:flex; gap:5px;">
                        <input type="text" id="userInput" placeholder="Execute logic audit...">
                        <button onclick="send()">RUN</button>
                    </div>
                </div>
                <div class="panel" style="background: #0d0d0d;">
                    <h4 style="color: var(--gold); font-size: 0.7em; margin-top:0;">ACTIVE SENSORS</h4>
                    {% for s in sensors %}
                    <div class="sensor-card">
                        <strong>{{ s[0] }}</strong><br><span style="color:#666;">{{ s[1] }}</span>
                    </div>
                    {% endfor %}
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
                
                const loadingId = "load-" + Date.now();
                chat.innerHTML += `<div class="msg ai" id="${loadingId}">THINKING <span class="typing-dot"></span><span class="typing-dot" style="animation-delay:0.2s"></span><span class="typing-dot" style="animation-delay:0.4s"></span></div>`;
                chat.scrollTop = chat.scrollHeight;

                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({prompt: text})
                    });
                    const data = await res.json();
                    document.getElementById(loadingId).innerHTML = data.reply;
                } catch (e) {
                    document.getElementById(loadingId).innerHTML = "ERROR: Connection timeout.";
                }
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body></html>
    """, sensors=sensors)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    try:
        res = requests.post("http://localhost:11434/api/generate", 
                            json={"model": "znon-agent", "prompt": prompt, "stream": False},
                            timeout=60)
        return jsonify({"reply": res.json().get('response', 'Logic rejection.')})
    except:
        return jsonify({"reply": "OFFLINE: Check 'ollama serve'."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
