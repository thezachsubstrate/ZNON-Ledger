from flask import Flask, render_template_string
import os

"""
PURPOSE: Mobile-responsive Dashboard for ZNON Sensors and Scripts.
SUBSTRATE_VERSION: v1.1.1
AUTHOR: Zach Mosley
"""

app = Flask(__name__)

REPO_PATH = os.path.expanduser("~/ZNON-Ledger")
SENSORS_FILE = os.path.join(REPO_PATH, "core/sensors/SENSOR_REGISTRY.md")

def get_sensors():
    if not os.path.exists(SENSORS_FILE): return []
    with open(SENSORS_FILE, 'r') as f:
        lines = f.readlines()[2:] # Skip table header
        return [line.strip().split('|')[1:4] for line in lines if '|' in line]

@app.route('/')
def home():
    sensors = get_sensors()
    html = """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: sans-serif; background: #1a1a1a; color: #eee; padding: 20px; }
            .card { background: #2d2d2d; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #ffd700; }
            h1 { color: #ffd700; border-bottom: 1px solid #444; padding-bottom: 10px; }
            .status { font-weight: bold; color: #00ff00; }
        </style>
    </head>
    <body>
        <h1>🛡 ZNON Sovereign Dashboard</h1>
        <p>Substrate Status: <span class="status">DETERMINISTIC</span></p>
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
    return render_template_string(html, sensors=sensors)

if __name__ == '__main__':
    # Runs on port 5000
    app.run(host='0.0.0.0', port=5000)
