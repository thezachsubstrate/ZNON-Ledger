from flask import Flask, render_template_string, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")

def check_registry_integrity():
    files = [f for f in os.listdir(REGISTRY_PATH) if f.endswith('.jnon')]
    unanchored = [f for f in files if not os.path.exists(os.path.join(REGISTRY_PATH, f + ".ots"))]
    return unanchored

@app.route('/', methods=['GET', 'POST'])
def home():
    unanchored_files = check_registry_integrity()
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
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="background:#111;color:#eee;padding:20px;font-family:sans-serif;">
        <h1 style="color:#ffd700;">🛡 ZNON v1.1.5 Dashboard</h1>
        <div style="background:#1a1a1a;padding:15px;border-radius:8px;margin-bottom:20px;border:1px solid {{ '#f55' if unanchored_files else '#0f0' }};">
            {% if unanchored_files %}
                <h3 style="margin:0;color:#f55;">🚨 {{ unanchored_files|length }} Unanchored Artifacts</h3>
                <form action="/anchor" method="POST" style="margin-top:10px;">
                    <button type="submit" style="background:#f55;color:#fff;padding:10px;width:100%;font-weight:bold;border:none;border-radius:4px;">BATCH ANCHOR NOW (OTS)</button>
                </form>
            {% else %}
                <div style="color:#0f0;">✅ ZSS-016: Substrate Fully Anchored.</div>
            {% endif %}
        </div>
        <div style="background:#1a1a1a;padding:20px;border:2px solid #ffd700;border-radius:8px;">
            <form method="POST">
                <textarea name="audit_text" style="width:100%;height:100px;background:#000;color:#0f0;padding:10px;border:1px solid #333;" placeholder="Paste text here..."></textarea><br><br>
                <button type="submit" style="background:#ffd700;color:#000;padding:12px;width:100%;font-weight:bold;border:none;border-radius:4px;">EXECUTE AUDIT</button>
            </form>
            {% if audit_score is not none %}<h2 style="color:#ffd700;text-align:center;">INTEGRITY: {{ audit_score }}%</h2>
            <ul style="color:#f55;font-family:monospace;list-style:none;padding:0;">{% for f in audit_findings %}<li>{{ f }}</li>{% endfor %}</ul>{% endif %}
        </div>
    </body></html>
    """, unanchored_files=unanchored_files, audit_score=audit_score, audit_findings=audit_findings)

@app.route('/anchor', methods=['POST'])
def anchor():
    for f in check_registry_integrity():
        subprocess.run(["ots", "stamp", os.path.join(REGISTRY_PATH, f)])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
