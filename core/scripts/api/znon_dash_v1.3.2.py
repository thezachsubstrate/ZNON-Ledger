from flask import Flask, render_template_string, request, jsonify
import os, requests, json

app = Flask(__name__)
# 300 second timeout for deep logic audits
TIMEOUT = 300 

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:20px; }
        .box { border:1px solid #ffd700; padding:15px; background:#0a0a0a; border-radius:8px; }
        #chat { height:350px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; }
        .status-bar { color:#ffd700; font-size:0.8em; margin-bottom:10px; border-bottom:1px solid #333; }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; }
        button { background:#ffd700; color:#000; padding:12px 20px; font-weight:bold; border:none; }
    </style></head>
    <body>
        <div class="status-bar">S24-ULTRA / 16GB-RAM / ZNON-SUBSTRATE-V1</div>
        <div class="box">
            <div id="chat"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in" placeholder="Query Sovereign Agent..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div><strong>USER:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700;">AUDITING SUBSTRATE...</div>`;
                i.value = ''; c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(lid).innerHTML = `<strong style="color:#0f0;">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(lid).innerHTML = "CONNECTION STALLED: Check Termux logs."; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": p, "stream": False}, 
                          timeout=300)
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "The Substrate is still initializing. Check Termux for 'Llama runner' status."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
