from flask import Flask, render_template_string, request, jsonify
import os, requests

app = Flask(__name__)
# High-Value Signaling Themes
THEME = {"gold": "#ffd700", "bg": "#050505", "neon": "#0f0"}

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: {{t.bg}}; color: #eee; font-family: monospace; padding: 20px; }
        .box { border: 1px solid {{t.gold}}; padding: 15px; background: #0a0a0a; border-radius: 8px; }
        #chat { height: 300px; overflow-y: auto; background: #000; padding: 10px; border: 1px solid #222; margin-bottom: 10px; }
        .dot { display: inline-block; width: 6px; height: 6px; background: {{t.gold}}; border-radius: 50%; margin-left: 3px; animation: b 1s infinite; }
        @keyframes b { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
        input { width: 70%; background: #000; color: {{t.neon}}; border: 1px solid {{t.gold}}; padding: 12px; }
        button { background: {{t.gold}}; color: #000; padding: 12px 20px; font-weight: bold; border: none; cursor: pointer; }
    </style></head>
    <body>
        <h2 style="color: {{t.gold}};">ZNON ARCHITECT <span style="font-size: 0.5em; border: 1px solid {{t.gold}}; padding: 2px 5px;">SOVEREIGN</span></h2>
        <div class="box">
            <div id="chat"></div>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="in" placeholder="Audit via Substrate..."><button onclick="send()">RUN</button>
            </div>
        </div>
        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div>YOU: ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:{{t.gold}};">THINKING <span class="dot"></span><span class="dot" style="animation-delay:0.2s"></span><span class="dot" style="animation-delay:0.4s"></span></div>`;
                i.value = ''; c.scrollTop = c.scrollHeight;
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    document.getElementById(lid).innerHTML = `<strong style="color:{{t.neon}};">ZNON:</strong> ${data.r}`;
                } catch { document.getElementById(lid).innerHTML = "TIMEOUT: Phone is crunching the 3B model. Please wait..."; }
                c.scrollTop = c.scrollHeight;
            }
        </script>
    </body></html>
    """, t=THEME)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    # Increased timeout to 120s for mobile hardware loading
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": p, "stream": False}, 
                          timeout=120)
        return jsonify({"r": r.json().get('response', 'Logic rejection.')})
    except Exception as e:
        return jsonify({"r": f"ENGINE_BUSY: Still loading model tensors. Try again in 30s."})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
