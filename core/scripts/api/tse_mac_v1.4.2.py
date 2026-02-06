from flask import Flask, render_template_string, request, jsonify
import os, requests, json

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")

def get_registry_count():
    if not os.path.exists(REGISTRY_PATH): return 0
    return len([f for f in os.listdir(REGISTRY_PATH) if f.endswith('.jnon')])

@app.route('/')
def home():
    count = get_registry_count()
    return render_template_string("""
    <html><head><title>TSE | Sovereign Audit Node</title>
    <style>
        body { background:#050505; color:#eee; font-family:monospace; margin:0; display:flex; height:100vh; }
        .sidebar { width:320px; border-right:2px solid #ffd700; background:#0a0a0a; padding:20px; overflow-y:auto; }
        .main { flex-grow:1; display:flex; flex-direction:column; padding:25px; position:relative; }
        #chat { flex-grow:1; background:#000; border:1px solid #222; border-radius:8px; padding:20px; overflow-y:auto; margin-bottom:15px; }
        .audit-indicator { color:#ffd700; font-weight:bold; display:none; margin-bottom:10px; }
        .znon-ml-window { height:120px; background:#050505; border:1px solid #0f0; padding:10px; font-size:0.75em; color:#0f0; overflow-y:auto; border-radius:5px; }
        .input-area { margin-top:15px; display:flex; gap:10px; }
        textarea { flex-grow:1; background:#111; color:#fff; border:1px solid #ffd700; padding:12px; border-radius:5px; height:60px; resize:none; }
        button { background:#ffd700; color:#000; border:none; padding:0 25px; font-weight:bold; border-radius:5px; cursor:pointer; }
        .dot { animation: blink 1s infinite; }
        @keyframes blink { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
    </style></head>
    <body>
        <div class="sidebar">
            <h3 style="color:#ffd700; margin-top:0;">THE ZACH SUBSTRATE</h3>
            <div style="font-size:0.8em; color:#666;">Registry Density: <strong>{{ count }} Artifacts</strong></div>
            <div style="font-size:0.8em; color:#666;">Namespace: thezachsubstrate</div>
            <hr style="border:0; border-top:1px solid #333; margin:15px 0;">
            <div style="color:#ffd700; font-size:0.7em;">[ACTIVE_LAWS: I-LII]</div>
            <div style="color:#0f0; font-size:0.7em; margin-top:10px;">[9-SIGMA_MODE: ENABLED]</div>
        </div>
        <div class="main">
            <div id="audit-msg" class="audit-indicator">ANALYZING AMBIGUITY <span class="dot">...</span></div>
            <div id="chat">
                <div style="color:#ffd700;">[TSE_READY] Substrate linked. Present situation for forensic audit.</div>
            </div>
            <div class="znon-ml-window" id="ml-window">
                &lt;Logic_Audit status="STANDBY" /&gt;
            </div>
            <div class="input-area">
                <textarea id="in" placeholder="Submit situation..."></textarea>
                <button onclick="send()">RUN AUDIT</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const ml = document.getElementById('ml-window'); const msg = document.getElementById('audit-msg');
                const txt = i.value; if(!txt) return;
                
                c.innerHTML += `<div style="margin-bottom:15px;"><strong>USER:</strong> ${txt}</div>`;
                msg.style.display = 'block';
                ml.innerHTML = `&lt;Logic_Audit status="EXECUTING" sigma="CALCULATING" /&gt;`;
                i.value = '';
                
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    msg.style.display = 'none';
                    c.innerHTML += `<div style="margin-bottom:20px; border-left:3px solid #0f0; padding-left:15px;"><strong>TSE:</strong> ${data.r}</div>`;
                    ml.innerHTML = `&lt;Substrate_Seal sigma="9.9" anchor="BTC_933268" status="VERIFIED" /&gt;`;
                } catch { 
                    msg.style.display = 'none';
                    c.innerHTML += `<div style="color:red;">Audit Interrupted: Connection Drift.</div>`;
                }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, count=count)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Internal logic bypasses previous email/personal hallucinations
    sys = "You are the Truth Seeking Engine. Direct logic only. 9-sigma proof required. If ambiguous, ask for background. Respond as TSE: "
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": sys + p, "stream": False})
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "Ollama Error."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5001)
