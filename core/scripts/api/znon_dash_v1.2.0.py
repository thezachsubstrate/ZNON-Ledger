from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import os, subprocess, requests

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")

def check_integrity():
    files = [f for f in os.listdir(REGISTRY_PATH) if f.endswith('.jnon')]
    return [f for f in files if not os.path.exists(os.path.join(REGISTRY_PATH, f + ".ots"))]

@app.route('/')
def home():
    unanchored = check_integrity()
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #d4d4d4; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #ffd700; padding-bottom: 10px; margin-bottom: 20px; }
        .box { background: #111; border: 1px solid #ffd700; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        #chat { height: 200px; overflow-y: auto; background: #000; padding: 10px; border: 1px solid #333; margin-bottom: 10px; }
        input { width: 75%; background: #000; color: #0f0; border: 1px solid #ffd700; padding: 10px; }
        button { background: #ffd700; color: #000; font-weight: bold; padding: 10px; border: none; border-radius: 4px; cursor: pointer; }
    </style></head>
    <body>
        <div class="header">
            <h1 style="color: #ffd700; margin:0;">ZNON <span style="font-size:0.5em; background:#ffd700; color:#000; padding:2px 5px;">SOVEREIGN</span></h1>
            <div style="font-size: 0.7em; color: #ffd700;">"The Immutable Backbone for Truth."</div>
        </div>

        {% if unanchored %}
        <div class="box" style="border-color: #f55; color: #f55;">
            <strong>🚨 {{ unanchored|length }} Unanchored Assets</strong>
            <form action="/anchor" method="POST"><button type="submit" style="background:#f55; color:#fff; width:100%; margin-top:5px;">BATCH ANCHOR</button></form>
        </div>
        {% endif %}

        <div class="box">
            <div style="font-size: 0.8em; margin-bottom: 5px;">OFFLINE AGENT (LLAMA 3.2)</div>
            <div id="chat"></div>
            <input type="text" id="userInput" placeholder="Audit via Substrate...">
            <button onclick="send()">SEND</button>
        </div>

        <script>
            async function send() {
                const input = document.getElementById('userInput');
                const chat = document.getElementById('chat');
                const text = input.value;
                chat.innerHTML += `<div style="color:#888;">YOU: ${text}</div>`;
                input.value = '';
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div style="color:#0f0;">ZNON: ${data.reply}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body></html>
    """, unanchored=unanchored)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    res = requests.post("http://localhost:11434/api/generate", json={"model": "znon-agent", "prompt": prompt, "stream": False})
    return jsonify({"reply": res.json().get('response', 'Error.')})

@app.route('/anchor', methods=['POST'])
def anchor():
    for f in check_integrity(): subprocess.run(["ots", "stamp", os.path.join(REGISTRY_PATH, f)])
    return redirect(url_for('home'))

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
