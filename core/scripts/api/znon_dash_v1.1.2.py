from flask import Flask, render_template_string, request
import os
from datetime import datetime

"""
PURPOSE: Interactive ZNON Dashboard with Live Hallucination Auditing.
SUBSTRATE_VERSION: v1.1.2
"""

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
SENSORS_FILE = os.path.join(REPO_PATH, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        lines = f.readlines()[2:]
        return [line.strip().split('|')[1:4] for line in lines if '|' in line]

def run_audit(text):
    # Logic from audit_wrapper_v1.1.1
    score = 100
    findings = []
    contradictions = ["definitely maybe", "true lie", "static change"]
    for c in contradictions:
        if c in text.lower():
            score -= 20
            findings.append(f"FAIL: Paradox detected ({c})")
    if score == 100: findings.append("PASS: Logical consistency high.")
    return score, findings

@app.route('/', methods=['GET', 'POST'])
def home():
    sensors = get_sensors()
    audit_score = None
    audit_findings = []
    
    if request.method == 'POST':
        text_to_audit = request.form.get('audit_text', '')
        audit_score, audit_findings = run_audit(text_to_audit)

    html = """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; background: #1a1a1a; color: #eee; padding: 20px; }
            .card { background: #2d2d2d; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #ffd700; }
            .audit-box { background: #333; padding: 20px; border-radius: 8px; border: 1px solid #ffd700; margin-bottom: 20px; }
            textarea { width: 100%; height: 100px; background: #222; color: #0f0; border: 1px solid #444; padding: 10px; }
            button { background: #ffd700; color: #000; border: none; padding: 10px 20px; font-weight: bold; border-radius: 4px; cursor: pointer; }
            .score { font-size: 24px; color: #ffd700; }
            h1 { color: #ffd700; }
        </style>
    </head>
    <body>
        <h1>🛡 ZNON Sovereign Dashboard v1.1.2</h1>
        
        <div class="audit-box">
            <h2>Live Hallucination Audit</h2>
            <form method="POST">
                <textarea name="audit_text" placeholder="Paste AI Output or Discovery here..."></textarea><br><br>
                <button type="submit">RUN ZNON AUDIT</button>
            </form>
            {% if audit_score is not none %}
                <div class="score">Integrity Score: {{ audit_score }}%</div>
                <ul>{% for f in audit_findings %}<li>{{ f }}</li>{% endfor %}</ul>
            {% endif %}
        </div>

        <h2>Active Sensors</h2>
        {% for sensor in sensors %}
        <div class="card">
            <strong>{{ sensor[0] }}</strong> ({{ sensor[1] }})<br>
            <small>{{ sensor[2] }}</small>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, sensors=sensors, audit_score=audit_score, audit_findings=audit_findings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
