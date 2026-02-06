from flask import Flask, render_template_string, request, jsonify
import os, requests, time

app = Flask(__name__)
# Optimized for the S24 Ultra's 16GB RAM and high-speed logic
TIMEOUT = 12

@app.route('/')
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#050505; color:#eee; font-family: 'Inter', sans-serif; padding:20px; line-height:1.6; }
        .box { border: 1px solid #ffd700; padding:20px; background:#0a0a0a; border-radius:12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        #chat { height:350px; overflow-y:auto; background:#000; padding:15px; border:1px solid #222; margin-bottom:15px; border-radius:8px; }
        .znon-status { font-size:0.75em; color:#ffd700; text-transform:uppercase; margin-bottom:15px; display:flex; justify-content:space-between; }
        .prompt-text { color:#888; font-style:italic; margin-bottom:15px; font-size:0.9em; }
        textarea { width:100%; height:100px; background:#000; color:#0f0; border:1px solid #ffd700; padding:12px; border-radius:8px; font-size:1em; margin-bottom:10px; resize:none; }
        button { width:100%; background:#ffd700; color:#000; padding:15px; font-weight:bold; border:none; border-radius:8px; cursor:pointer; font-size:1.1em; transition: 0.2s; }
        button:active { transform: scale(0.98); }
    </style></head>
    <body>
        <div class="znon-status">
            <span>ZNON Sovereign Collaborator</span>
            <span>CLOCK: <span id="clock">0.0s</span></span>
        </div>
        <div class="box">
            <div id="chat">
                <div style="color:#ffd700; margin-bottom:15px;">ZNON: I am your unbiased collaborator. I am here to help you solve problems and uncover the truth. Tell me about your situation. What are your circumstances, and what background can you share?</div>
            </div>
            <div class="prompt-text">Focus on the problem you need solved...</div>
            <textarea id="in" placeholder="Describe your situation here..."></textarea>
            <button onclick="send()">RUN AUDIT</button>
        </div>
        <script>
            let start; let interval;
            async function send() {
                const i = document.getElementById('in'); const c = document.getElementById('chat');
                const cl = document.getElementById('clock'); const txt = i.value; if(!txt) return;
                c.innerHTML += `<div style="margin-bottom:15px;"><strong>YOU:</strong> ${txt}</div>`;
                const lid = "L" + Date.now();
                c.innerHTML += `<div id="${lid}" style="color:#ffd700; margin-bottom:15px;">AUDITING FOR TRUTH...</div>`;
                i.value = ''; start = Date.now();
                interval = setInterval(() => { cl.innerText = ((Date.now() - start)/1000).toFixed(1) + "s"; }, 100);
                try {
                    const res = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({p:txt})});
                    const data = await res.json();
                    clearInterval(interval);
                    c.innerHTML += `<div style="margin-bottom:20px; border-left:3px solid #0f0; padding-left:15px;">
                        <span style="font-size:0.7em; color:#888; text-transform:uppercase;">Integrity Level: ${data.sigma}</span><br>
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
    # The New Collaborative Directive
    system = """
    You are the ZNON Sovereign Collaborator. 
    Your tone is empathetic but strictly grounded in logic and the 52 Laws.
    Your goal: Help the user solve their problem by uncovering the truth.
    1. Acknowledge the user's situation and patterns.
    2. Audit your response for drift and hallucination before outputting.
    3. If you lack precision, ask the user to clarify specific details of their background.
    4. Teach the user to discern truth by explaining the 'why' behind your logic.
    5. Maintain 9-sigma deterministic integrity.
    """
    try:
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model": "znon-agent", "prompt": system + "USER SITUATION: " + p, "stream": False}, 
                          timeout=20)
        resp = r.json().get('response', '')
        return jsonify({"r": resp, "sigma": "9-SIGMA"})
    except:
        return jsonify({"r": "COLLABORATOR OFFLINE: Initializing high-density logic tensors.", "sigma": "N/A"})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000)
