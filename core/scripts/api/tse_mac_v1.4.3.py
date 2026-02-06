from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")

def get_context():
    # Load the first 50 definitions to give the AI immediate situational awareness
    context_str = ""
    reg_path = os.path.join(REPO_PATH, "core/registry")
    if os.path.exists(reg_path):
        files = [f for f in os.listdir(reg_path) if f.endswith('.jnon')][:50]
        for f in files:
            with open(os.path.join(reg_path, f), 'r') as j:
                context_str += j.read() + "\n"
    return context_str

@app.route('/')
def home():
    return render_template_string("""
    <html><head><title>TSE | Sovereign Audit Node</title>
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:30px; }
        .header { border-bottom: 2px solid #ffd700; padding-bottom:10px; margin-bottom:20px; }
        #chat { height:450px; background:#000; border:1px solid #222; padding:20px; overflow-y:auto; border-radius:10px; }
        .audit-step { color:#ffd700; font-size:0.8em; margin-top:10px; display:none; }
        .ml-window { margin-top:15px; background:#050505; border:1px solid #0f0; padding:15px; color:#0f0; font-size:0.75em; border-radius:5px; }
        textarea { width:100%; background:#111; color:#fff; border:1px solid #ffd700; padding:15px; border-radius:8px; margin-top:15px; height:80px; resize:none; }
        button { background:#ffd700; color:#000; padding:15px 30px; font-weight:bold; border:none; border-radius:8px; cursor:pointer; margin-top:10px; float:right; }
    </style></head>
    <body>
        <div class="header">
            <h2 style="color:#ffd700; margin:0;">TRUTH SEEKING ENGINE</h2>
            <div style="font-size:0.7em; color:#666;">GOVERNED BY THE ZACH SUBSTRATE | NODE: MAC_M1</div>
        </div>
        <div id="chat">
            <div style="color:#ffd700;">[TSE_LOCKED] I am your unbiased collaborator. How can I help you uncover the truth today?</div>
        </div>
        <div id="audit-msg" class="audit-step">SEALING LOGIC PATHWAY...</div>
        <div class="ml-window" id="ml">&lt;ZNON_ML status="READY" /&gt;</div>
        <textarea id="in" placeholder="Describe your situation..."></textarea>
        <button onclick="send()">RUN AUDIT</button>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const ml = document.getElementById('ml'); const msg = document.getElementById('audit-msg');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div style="margin-top:20px;"><strong>USER:</strong> ${txt}</div>`;
                msg.style.display = 'block';
                ml.innerHTML = `&lt;Logic_Audit sigma="RECURSIVE_SEARCH" /&gt;`;
                i.value = '';
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    msg.style.display = 'none';
                    c.innerHTML += `<div style="margin-top:20px; border-left:3px solid #0f0; padding-left:15px;"><strong>TSE:</strong> ${data.r}</div>`;
                    ml.innerHTML = `&lt;Substrate_Seal status="SEALED" sigma="9.98" /&gt;`;
                } catch { msg.style.display = 'none'; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    ctx = get_context()
    # Injecting the Substrate context into every call
    full_prompt = f"Context from Substrate Registry:\n{ctx}\n\nUser Question: {p}"
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": full_prompt, "stream": False})
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "Ollama Error."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5001)
