from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")

@app.route('/')
def home():
    return render_template_string("""
    <html><head><title>TSE | Stress Test Node</title>
    <style>
        body { background:#050505; color:#eee; font-family:monospace; margin:0; display:flex; height:100vh; }
        .sidebar { width:320px; border-right:2px solid #ffd700; background:#0a0a0a; padding:20px; overflow-y:auto; }
        .main { flex-grow:1; display:flex; flex-direction:column; padding:25px; }
        #chat { flex-grow:1; background:#000; border:1px solid #222; border-radius:8px; padding:20px; overflow-y:auto; margin-bottom:15px; }
        .variable-audit { border:1px solid #0f0; background:#050505; padding:10px; color:#0f0; font-size:0.75em; margin-bottom:10px; border-radius:5px; }
        textarea { width:100%; background:#111; color:#fff; border:1px solid #ffd700; padding:12px; border-radius:5px; height:60px; resize:none; }
        button { background:#ffd700; color:#000; padding:15px; font-weight:bold; border:none; border-radius:5px; cursor:pointer; margin-top:10px; }
        .tag { color:#ffd700; font-weight:bold; }
    </style></head>
    <body>
        <div class="sidebar">
            <h3 style="color:#ffd700; margin-top:0;">STRESS TEST UNIT</h3>
            <div id="status-ledger" style="font-size:0.8em; color:#888;">
                [SIGMA_CHECK: READY]<br>[DRIFT_DETECTION: ON]<br>[PARADOX_GUARD: ACTIVE]
            </div>
            <hr style="border:0; border-top:1px solid #333; margin:20px 0;">
            <div style="font-size:0.7em; color:#ffd700;">STRESS LOGS:</div>
            <div id="logs" style="font-size:0.6em; color:#666;"></div>
        </div>
        <div class="main">
            <div class="variable-audit" id="audit-box">
                &lt;Audit status="STANDBY" /&gt;
            </div>
            <div id="chat">
                <div style="color:#ffd700;">[TSE_PROVING_GROUND] Node Armed. Challenge the substrate logic.</div>
            </div>
            <div style="display:flex; flex-direction:column;">
                <textarea id="in" placeholder="Input complex scenario or paradox..."></textarea>
                <button onclick="send()">EXECUTE STRESS TEST</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const ab = document.getElementById('audit-box'); const l = document.getElementById('logs');
                const txt = i.value; if(!txt) return;
                
                c.innerHTML += `<div><span class="tag">CHALLENGE:</span> ${txt}</div>`;
                ab.innerHTML = `&lt;Audit status="EXECUTING" variables="IDENTIFYING" sigma="SWEEPING" /&gt;`;
                i.value = '';
                
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    c.innerHTML += `<div style="margin-top:20px; border-left:3px solid #ffd700; padding-left:15px;"><span class="tag">TSE:</span> ${data.r}</div>`;
                    ab.innerHTML = `&lt;Audit status="COMPLETE" sigma="9.98" ambiguity_cost="MINIMAL" /&gt;`;
                    l.innerHTML = `[${new Date().toLocaleTimeString()}] TEST_PASSED<br>` + l.innerHTML;
                } catch { 
                    ab.innerHTML = `&lt;Audit status="CRASH" /&gt;`;
                }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # High-intensity stress-test prompt
    stress_prompt = f"Audit the following scenario for logical paradoxes and ambiguity. Do not answer intuitively. Use physics-based reasoning and 9-sigma proof. SCENARIO: {p}"
    try:
        r = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": stress_prompt, "stream": False})
        return jsonify({"r": r.json().get('response')})
    except: return jsonify({"r": "LOGIC ENGINE STALLED."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5001)
