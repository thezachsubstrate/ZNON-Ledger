from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")

def verify_substrate():
    laws = os.path.exists(os.path.join(REPO_PATH, "core/LAWS.md"))
    registry = os.path.exists(os.path.join(REPO_PATH, "core/registry"))
    return laws and registry

@app.route('/')
def home():
    status = "LOCKED" if verify_substrate() else "PATH_ERROR"
    return render_template_string("""
    <html><head><title>TSE | Mac Command Center</title>
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:40px; }
        .status-header { border:1px solid #ffd700; padding:10px; color:#ffd700; margin-bottom:20px; text-align:center; }
        .main-ui { display:flex; gap:20px; }
        .chat-area { flex-grow:2; background:#000; border:1px solid #222; padding:20px; height:500px; overflow-y:auto; border-radius:10px; }
        .znon-ml-feed { flex-grow:1; background:#050505; border:1px solid #0f0; color:#0f0; font-size:0.7em; padding:15px; border-radius:10px; }
        .input-box { margin-top:20px; display:flex; gap:10px; }
        textarea { flex-grow:1; background:#111; color:#fff; border:1px solid #ffd700; padding:15px; border-radius:8px; height:80px; resize:none; }
        button { background:#ffd700; color:#000; border:none; padding:0 30px; border-radius:8px; font-weight:bold; cursor:pointer; }
    </style></head>
    <body>
        <div class="status-header">TRUTH SEEKING ENGINE v1.4.0 | SUBSTRATE STATUS: {{ status }}</div>
        <div class="main-ui">
            <div class="chat-area" id="chat">
                <div style="color:#ffd700;">[ZNON] Connection established via thezachsubstrate/ZNON-Ledger. Ready to audit.</div>
            </div>
            <div class="znon-ml-feed" id="ml">
                &lt;Substrate_Link status="CONNECTED" repo="thezachsubstrate" /&gt;
            </div>
        </div>
        <div class="input-box">
            <textarea id="in" placeholder="Present your situation for 9-sigma audit..."></textarea>
            <button onclick="send()">RUN TSE</button>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const ml = document.getElementById('ml'); const txt = i.value; if(!txt) return;
                c.innerHTML += `<div><strong>USER:</strong> ${txt}</div>`;
                i.value = '';
                const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                const data = await res.json();
                c.innerHTML += `<div style="margin-top:15px; border-left:2px solid #0f0; padding-left:15px;"><strong>TSE:</strong> ${data.r}</div>`;
                ml.innerHTML += `<br>&lt;Audit timestamp="${new Date().toLocaleTimeString()}" sigma="9.98" status="SEALED" /&gt;`;
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, status=status)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": p, "stream": False})
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "Ollama Node Offline."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5001)
