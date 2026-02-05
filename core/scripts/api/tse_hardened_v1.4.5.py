from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
VERSION = "1.4.5"
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")

@app.route('/')
def home():
    return render_template_string("""
    <html><head><title>TSE | Hardened Node</title>
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:30px; }
        .audit-strip { background:#ffd700; color:#000; padding:8px 20px; font-weight:bold; font-size:0.8em; margin-bottom:20px; border-radius:4px; }
        .chat-box { height:400px; background:#000; border:1px solid #222; padding:25px; overflow-y:auto; border-radius:12px; }
        #audit-msg { color:#ffd700; font-weight:bold; display:none; margin-bottom:10px; }
        textarea { width:100%; background:#111; color:#0f0; border:1px solid #ffd700; padding:15px; border-radius:10px; height:80px; margin-top:15px; resize:none; }
        button { background:#ffd700; color:#000; border:none; padding:15px 35px; font-weight:bold; border-radius:10px; cursor:pointer; margin-top:10px; width:100%; }
        .dot { animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
    </style></head>
    <body>
        <div class="audit-strip">TRUTH SEEKING ENGINE v{{ v }} | GOVERNED BY THE ZACH SUBSTRATE</div>
        <div id="chat" class="chat-box">
            <div style="color:#ffd700;">[TSE_LOCKED] I am the Truth Seeking Engine. I use ZNON-ML to uncover 9-sigma truth. How can I collaborate with you today?</div>
        </div>
        <div id="audit-msg">ANALYZING AMBIGUITY <span class="dot">...</span></div>
        <textarea id="in" placeholder="Present your situation for audit..."></textarea>
        <button onclick="send()">RUN TSE AUDIT</button>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const msg = document.getElementById('audit-msg'); const txt = i.value; if(!txt) return;
                c.innerHTML += `<div style="margin-top:20px;"><strong>SITUATION:</strong> ${txt}</div>`;
                msg.style.display = 'block'; i.value = '';
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    msg.style.display = 'none';
                    c.innerHTML += `<div style="margin-top:20px; border-left:3px solid #0f0; padding-left:15px;"><strong>TSE:</strong> ${data.r}</div>`;
                } catch { msg.style.display = 'none'; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, v=VERSION)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Self-Awareness Prompt
    sys = "You are the Truth Seeking Engine (TSE), governed by The Zach Substrate. Use ZNON-ML. Audit for 9-sigma truth. Respond as TSE: "
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": sys + p, "stream": False})
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "Ollama Latency Error."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5001)
