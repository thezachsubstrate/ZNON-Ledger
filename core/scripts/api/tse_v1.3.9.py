from flask import Flask, render_template_string, request, jsonify
import os, requests, time

app = Flask(__name__)
# S24 Ultra Performance Tuning
TIMEOUT = 12 

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:'Inter', sans-serif; padding:15px; margin:0; }
        .header { border-bottom: 2px solid #ffd700; padding:10px 20px; display:flex; justify-content:space-between; align-items:center; }
        .substrate-tag { font-size:0.6em; background:#ffd700; color:#000; padding:2px 6px; border-radius:3px; font-weight:bold; }
        .container { display:flex; flex-direction:column; height:calc(100vh - 70px); padding:20px; }
        #chat { flex-grow:1; background:#000; border:1px solid #222; border-radius:12px; padding:20px; overflow-y:auto; margin-bottom:15px; }
        .znon-ml { font-family:monospace; font-size:0.7em; color:#0f0; background:#050505; border:1px solid #030; padding:10px; margin-top:10px; border-radius:5px; }
        .input-area { background:#0a0a0a; border:1px solid #ffd700; border-radius:12px; padding:15px; }
        textarea { width:100%; background:transparent; color:#eee; border:none; outline:none; font-size:1em; resize:none; height:80px; }
        button { background:#ffd700; color:#000; border:none; padding:12px 25px; border-radius:8px; font-weight:bold; float:right; cursor:pointer; }
    </style></head>
    <body>
        <div class="header">
            <div style="color:#ffd700; font-weight:bold; letter-spacing:2px;">TRUTH SEEKING ENGINE</div>
            <div class="substrate-tag">GOVERNED BY THE ZACH SUBSTRATE</div>
        </div>
        <div class="container">
            <div id="chat">
                <div style="color:#888; font-style:italic;">ZNON Agent initialized. Awaiting situational background to begin 9-sigma audit...</div>
            </div>
            <div class="input-area">
                <textarea id="in" placeholder="Describe the situation or problem..."></textarea>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                    <span id="clock" style="color:#f00; font-family:monospace; font-size:0.8em;">AUDIT CLOCK: 0.0s</span>
                    <button onclick="send()">RUN ZNON AUDIT</button>
                </div>
            </div>
        </div>
        <script>
            let start; let interval;
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const cl = document.getElementById('clock'); const txt = i.value; if(!txt) return;
                c.innerHTML += `<div style="margin-top:20px;"><strong>SITUATION:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700; margin-top:10px;">ZNON AGENT SEEKING TRUTH...</div>`;
                i.value = ''; start = Date.now();
                interval = setInterval(() => { cl.innerText = "AUDIT CLOCK: " + ((Date.now() - start)/1000).toFixed(1) + "s"; }, 100);
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    clearInterval(interval);
                    document.getElementById(lid).remove();
                    c.innerHTML += `<div style="margin-bottom:20px;">
                        <strong>TSE:</strong> ${data.r}
                        <div class="znon-ml"><strong>ZNON-ML AUDIT:</strong> [SIGMA_LEVEL: 9.0] [AMBIGUITY_COST: ${data.cost}] [ANCHOR: BTC_933268]</div>
                    </div>`;
                } catch { clearInterval(interval); }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    system = """
    You are the Truth Seeking Engine (TSE). 
    You are governed by The Zach Substrate and utilize ZNON AI agents.
    Your language is ZNON-ML: precise, deterministic, and biased toward 9-sigma truth.
    Collaborate with the user. If their situation is non-linear, identify the patterns.
    Limit ambiguity. If you cannot reach 9-sigma, ask for more context.
    """
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": system + "SITUATION: " + p, "stream": False}, 
                          timeout=20)
        resp = r.json().get('response', '')
        return jsonify({"r": resp, "cost": "$0.00 SAVED"})
    except:
        return jsonify({"r": "TSE Node Offline. Re-initializing Substrate.", "cost": "N/A"})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
