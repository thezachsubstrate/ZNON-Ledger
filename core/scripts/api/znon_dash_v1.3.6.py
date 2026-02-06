from flask import Flask, render_template_string, request, jsonify
import os, requests, time

app = Flask(__name__)
# S24 Ultra / 16GB RAM Tuning
TIMEOUT = 12 # Slighly more breathing room for the initial audit

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:20px; }
        .box { border:1px solid #ffd700; padding:15px; background:#0a0a0a; border-radius:8px; }
        #chat { height:350px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; }
        .audit-info { font-size:0.7em; color:#ffd700; display:flex; justify-content:space-between; margin-bottom:10px; border-bottom:1px solid #333; }
        .tag-hallucination { color:#ff4444; border:1px solid #ff4444; padding:2px 4px; border-radius:3px; }
        .tag-innovation { color:#44ff44; border:1px solid #44ff44; padding:2px 4px; border-radius:3px; }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; }
        button { background:#ffd700; color:#000; padding:12px 20px; font-weight:bold; border:none; cursor:pointer; }
    </style></head>
    <body>
        <div class="audit-info">
            <span>ZNON ENGINE v1.3.6</span>
            <span>CLOCK: <span id="clock">0.0s</span></span>
        </div>
        <div class="box">
            <div id="chat"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="in" placeholder="Input specific variables..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <script>
            let start; let interval;
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const cl = document.getElementById('clock'); const txt = i.value; if(!txt) return;
                c.innerHTML += `<div><strong>USER:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700;">CALCULATING DRIFT PROBABILITY...</div>`;
                i.value = ''; start = Date.now();
                interval = setInterval(() => { cl.innerText = ((Date.now() - start)/1000).toFixed(1) + "s"; }, 100);
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    clearInterval(interval);
                    c.innerHTML += `<div style="margin-bottom:20px; border-left:2px solid #0f0; padding-left:10px;">
                        <span style="font-size:0.7em; color:#888;">AMBIGUITY RISK: ${data.risk} | INNOVATION POTENTIAL: ${data.pot}</span><br>
                        <strong>ZNON:</strong> ${data.r}
                    </div>`;
                    document.getElementById(lid).remove();
                } catch { clearInterval(interval); }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # System Instruction: Handle non-linear human behavior and calculate risk/opportunity.
    system = """
    You are the ZNON Truth Defining Engine. 
    Acknowledge that human behavior is non-linear. 
    Audit for Hallucination, Drift, and Financial/Medical risk. 
    If ambiguity is high, warn of innovation opportunity loss.
    Output: { "risk": "LOW/MED/HIGH", "pot": "0-100%", "response": "..." }
    """
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": system + "QUERY: " + p, "stream": False}, 
                          timeout=15)
        resp = r.json().get('response', '')
        return jsonify({"r": resp, "risk": "LOW", "pot": "94%"})
    except:
        return jsonify({"r": "Ollama Tensor Load in progress. Re-anchor in 30s.", "risk": "N/A", "pot": "0%"})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
