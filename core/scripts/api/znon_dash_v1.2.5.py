from flask import Flask, render_template_string, request, jsonify
import os, requests, json

app = Flask(__name__)
REPO = os.path.expanduser("~/ZNON-Ledger")
REGISTRY = os.path.join(REPO, "core/registry")

@app.route('/')
def home():
    # Count the total scale of the Substrate
    total_terms = 855
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family:monospace; padding:20px; }
        .box { border:1px solid #ffd700; padding:15px; margin-bottom:15px; background:#0a0a0a; border-radius:8px; }
        #chat { height:200px; overflow-y:auto; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px; }
        input { width:70%; background:#000; color:#0f0; border:1px solid #ffd700; padding:10px; }
        button { background:#ffd700; color:#000; padding:10px; font-weight:bold; border:none; cursor:pointer; }
        .stat { color:#ffd700; font-size:0.8em; margin-bottom:20px; }
    </style></head>
    <body>
        <h1 style="color:#ffd700; margin:0;">ZNON ARCHITECT v1.2.5</h1>
        <div class="stat">SUBSTRATE DENSITY: {{ total_terms }} JNON ARTIFACTS</div>
        
        <div class="box">
            <div id="chat"></div>
            <input type="text" id="in" placeholder="Query the Substrate..."><button onclick="send()">RUN</button>
        </div>

        <div class="box">
            <input type="text" id="q" placeholder="Search 855+ Terms..." onkeyup="search()">
            <div id="results" style="margin-top:10px; font-size:0.7em; color:#888;"></div>
        </div>

        <script>
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const txt = i.value; if(!txt) return;
                c.innerHTML += `<div>YOU: ${txt}</div><div id="loading">ANALYZING...</div>`;
                i.value = '';
                const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                const data = await res.json();
                document.getElementById('loading').remove();
                c.innerHTML += `<div style="color:#0f0;">ZNON: ${data.r}</div>`;
                c.scrollTop = c.scrollHeight;
            }
            // Add search logic for the 855+ terms here in next update
        </script>
    </body></html>
    """, total_terms=total_terms)

@app.route('/chat', methods=['POST'])
def chat():
    p = request.json.get('p')
    r = requests.post("http://localhost:11434/api/generate", json={"model":"znon-agent","prompt":p,"stream":False}, timeout=60)
    return jsonify({"r": r.json().get('response', 'Logic rejection.')})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
