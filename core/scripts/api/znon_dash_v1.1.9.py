from flask import Flask, render_template_string, request, jsonify
import os
import requests

app = Flask(__name__)

def chat_with_local_ai(prompt):
    # This calls the Ollama server running on your phone
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "znon-agent",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json().get('response', 'Connection Error.')
    except:
        return "ZNON AI is currently sleeping. Run 'ollama serve'."

@app.route('/')
def home():
    return render_template_string("""
    <html><body style="background:#0a0a0a;color:#ffd700;padding:20px;font-family:monospace;">
        <h1>🛡 ZNON OFFLINE AGENT v1.1.9</h1>
        <div id="chat" style="height:300px;overflow-y:auto;border:1px solid #ffd700;padding:10px;margin-bottom:10px;background:#111;"></div>
        <input type="text" id="userInput" style="width:80%;background:#000;color:#0f0;border:1px solid #ffd700;padding:10px;">
        <button onclick="send()" style="background:#ffd700;color:#000;padding:10px;font-weight:bold;">SEND</button>
        <script>
            async function send() {
                const input = document.getElementById('userInput');
                const chat = document.getElementById('chat');
                const text = input.value;
                chat.innerHTML += `<div><strong>YOU:</strong> ${text}</div>`;
                input.value = '';
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: text})
                });
                const data = await res.json();
                chat.innerHTML += `<div style="color:#fff;"><strong>ZNON:</strong> ${data.reply}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
        </script>
    </body></html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt')
    reply = chat_with_local_ai(prompt)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
