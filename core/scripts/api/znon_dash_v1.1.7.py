from flask import Flask, render_template_string, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")
SENSORS_FILE = os.path.join(REPO_PATH, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        lines = f.readlines()[2:]
        return [line.strip().split('|')[1:5] for line in lines if '|' in line]

def check_registry_integrity():
    files = [f for f in os.listdir(REGISTRY_PATH) if f.endswith('.jnon')]
    return [f for f in files if not os.path.exists(os.path.join(REGISTRY_PATH, f + ".ots"))]

@app.route('/', methods=['GET', 'POST'])
def home():
    unanchored_files = check_registry_integrity()
    sensors = get_sensors()
    audit_score, audit_findings = None, []
    
    if request.method == 'POST' and 'audit_text' in request.form:
        text = request.form.get('audit_text', '')
        score, findings = 100, []
        p_weights = {"definitely maybe": 15, "true lie": 15, "static change": 10, "permanent temporary": 15}
        for p, w in p_weights.items():
            c = text.lower().count(p)
            if c > 0:
                score -= (w * c)
                findings.append(f"FAIL: '{p}' detected {c}x (-{w*c} pts)")
        audit_score, audit_findings = max(0, score), findings

    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Courier New', Courier, monospace; background: #0a0a0a; color: #d4d4d4; padding: 20px; }
        .header { text-align: center; border-bottom: 2px solid #ffd700; padding-bottom: 20px; margin-bottom: 30px; }
        .tagline { color: #ffd700; font-style: italic; font-size: 0.8em; margin-top: 5px; }
        .substrate-tag { font-size: 0.6em; color: #888; text-transform: uppercase; letter-spacing: 2px; }
        .badge { background: #ffd700; color: #000; padding: 2px 8px; font-weight: bold; border-radius: 3px; font-size: 0.7em; }
        .card { background: #151515; padding: 15px; border-radius: 4px; margin-bottom: 10px; border-left: 5px solid #ffd700; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
        .audit-box { background: #111; padding: 20px; border: 1px solid #ffd700; border-radius: 8px; margin-bottom: 30px; }
        textarea { width: 100%; height: 100px; background: #000; color: #00ff00; border: 1px solid #333; padding: 10px; font-family: monospace; }
        button { background: #ffd700; color: #000; border: none; padding: 12px; font-weight: bold; width: 100%; border-radius: 4px; cursor: pointer; }
        .integrity-banner { background: #1a0000; border: 1px solid #ff0000; color: #ff0000; padding: 10px; border-radius: 4px; margin-bottom: 20px; font-size: 0.8em; }
    </style>
    </head>
    <body>
        <div class="header">
            <span class="substrate-tag">The Zach Substrate</span>
            <h1 style="margin: 5px 0; color: #ffd700;">ZNON <span class="badge">SOVEREIGN</span></h1>
            <div class="tagline">"The Immutable Backbone for Truth."</div>
            <div style="font-size: 0.6em; color: #555; margin-top: 10px;">World's First Truth Seeking Engine</div>
        </div>

        {% if unanchored_files %}
        <div class="integrity-banner">
            <strong>🚨 INTEGRITY BREACH:</strong> {{ unanchored_files|length }} Unanchored Files<br>
            <form action="/anchor" method="POST" style="margin-top:10px;">
                <button type="submit" style="background:#ff0000; color:#fff; font-size: 0.7em; padding: 5px;">RESOLVE & ANCHOR</button>
            </form>
        </div>
        {% endif %}

        <div class="audit-box">
            <div style="font-size: 0.7em; margin-bottom: 10px; color: #ffd700;">// HALLUCINATION_AUDIT_MODULE_V1.1.7</div>
            <form method="POST">
                <textarea name="audit_text" placeholder="Input AI output for verification..."></textarea><br><br>
                <button type="submit">EXECUTE FORENSIC AUDIT</button>
            </form>
            {% if audit_score is not none %}
                <div style="text-align:center; margin-top: 15px;">
                    <div style="font-size: 0.8em; color: #888;">INTEGRITY RATING</div>
                    <div style="font-size: 2.5em; color: #ffd700; font-weight: bold;">{{ audit_score }}%</div>
                </div>
            {% endif %}
        </div>

        <h3 style="color: #ffd700; font-size: 0.9em; border-bottom: 1px solid #333; padding-bottom: 5px;">ACTIVE SENSOR REGISTRY</h3>
        {% for sensor in sensors %}
        <div class="card">
            <strong style="color: #ffd700;">{{ sensor[0] }}</strong> <span style="font-size: 0.7em; color: #555;">({{ sensor[3] }})</span><br>
            <span style="font-size: 0.8em; color: #aaa;">{{ sensor[1] }}</span><br>
            <div style="font-size: 0.6em; color: #666; margin-top: 5px;">{{ sensor[2] }}</div>
        </div>
        {% endfor %}
        
        <div style="text-align: center; margin-top: 40px; font-size: 0.5em; color: #444;">
            Verified by Bitcoin. Audited by Truth. Integrity by Design.
        </div>
    </body></html>
    """, unanchored_files=unanchored_files, sensors=sensors, audit_score=audit_score, audit_findings=audit_findings)

@app.route('/anchor', methods=['POST'])
def anchor():
    for f in check_registry_integrity():
        subprocess.run(["ots", "stamp", os.path.join(REGISTRY_PATH, f)])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
