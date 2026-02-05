from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
REGISTRY_PATH = os.path.join(REPO_PATH, "core/registry")

def check_registry_integrity():
    files = [f for f in os.listdir(REGISTRY_PATH) if f.endswith('.jnon')]
    issues = []
    for f in files:
        if not os.path.exists(os.path.join(REGISTRY_PATH, f + ".ots")):
            issues.append(f"ZSS-016 ALERT: {f} is NOT anchored to blockchain.")
    return issues

def run_audit(text):
    score, findings = 100, []
    p_weights = {"definitely maybe": 15, "true lie": 15, "static change": 10, "permanent temporary": 15}
    for p, w in p_weights.items():
        c = text.lower().count(p)
        if c > 0:
            score -= (w * c)
            findings.append(f"FAIL: '{p}' detected {c}x (-{w*c} pts)")
    return max(0, score), findings

@app.route('/', methods=['GET', 'POST'])
def home():
    audit_score, audit_findings = None, []
    integrity_issues = check_registry_integrity()
    
    if request.method == 'POST':
        audit_score, audit_findings = run_audit(request.form.get('audit_text', ''))
        
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="background:#111;color:#eee;padding:20px;font-family:sans-serif;">
        <h1 style="color:#ffd700;">🛡 ZNON v1.1.4 Dashboard</h1>
        
        {% if integrity_issues %}
            <div style="background:#422;border:2px solid #f55;padding:15px;border-radius:8px;margin-bottom:20px;">
                <h3 style="margin:0;color:#f55;">🚨 REGISTRY INTEGRITY ALERT (ZSS-016)</h3>
                <ul style="font-size:0.8em;padding-left:20px;">{% for issue in integrity_issues %}<li>{{ issue }}</li>{% endfor %}</ul>
            </div>
        {% else %}
            <div style="color:#0f0;margin-bottom:20px;">✅ ZSS-016: Registry Integrity Verified.</div>
        {% endif %}

        <div style="background:#1a1a1a;padding:20px;border:2px solid #ffd700;border-radius:8px;">
            <form method="POST">
                <textarea name="audit_text" style="width:100%;height:120px;background:#000;color:#0f0;padding:10px;border:1px solid #333;" placeholder="Paste text here..."></textarea><br><br>
                <button type="submit" style="background:#ffd700;color:#000;padding:12px;width:100%;font-weight:bold;border-radius:4px;">EXECUTE AUDIT</button>
            </form>
            {% if audit_score is not none %}
                <h2 style="color:#ffd700;text-align:center;">INTEGRITY: {{ audit_score }}%</h2>
                <ul style="color:#f55;font-family:monospace;list-style:none;padding:0;">{% for f in audit_findings %}<li>{{ f }}</li>{% endfor %}</ul>
            {% endif %}
        </div>
    </body></html>
    """, integrity_issues=integrity_issues, audit_score=audit_score, audit_findings=audit_findings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
