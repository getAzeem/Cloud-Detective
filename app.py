from flask import Flask, request, render_template_string
import yaml

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>K8s YAML Analyzer</title>
    <style>
        body { font-family: Arial; background:#0f172a; color:white; padding:30px; }
        textarea { width:100%; height:320px; background:#111827; color:#e5e7eb; padding:15px; border-radius:10px; }
        button { padding:12px 22px; border:0; border-radius:8px; font-weight:bold; cursor:pointer; }
        .card { background:#111827; padding:20px; border-radius:14px; margin-top:20px; border:1px solid #334155; }
        .bad { color:#f87171; }
        .good { color:#4ade80; }
    </style>
</head>
<body>
    <h1>🛡️ Kubernetes YAML Security Analyzer</h1>
    <p>Paste Deployment/Pod YAML and detect security + reliability issues.</p>

    <form method="POST">
        <textarea name="yaml_text" placeholder="Paste Kubernetes YAML here...">{{ yaml_text }}</textarea><br><br>
        <button type="submit">Analyze YAML</button>
    </form>

    {% if results %}
    <div class="card">
        <h2>Security Score: {{ score }}/100</h2>

        {% if results %}
            <h3>Issues Found</h3>
            {% for item in results %}
                <p class="bad">❌ {{ item }}</p>
            {% endfor %}
        {% else %}
            <p class="good">✅ No major issues detected.</p>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""

def analyze_yaml(text):
    issues = []
    score = 100

    try:
        docs = list(yaml.safe_load_all(text))
    except Exception:
        return 0, ["Invalid YAML format"]

    full_text = text.lower()

    if "latest" in full_text:
        issues.append("Avoid using image tag ':latest'. Use fixed version tags.")
        score -= 15

    if "resources:" not in full_text:
        issues.append("Missing CPU/memory resource requests and limits.")
        score -= 20

    if "livenessprobe" not in full_text:
        issues.append("Missing livenessProbe.")
        score -= 10

    if "readinessprobe" not in full_text:
        issues.append("Missing readinessProbe.")
        score -= 10

    if "runasnonroot" not in full_text:
        issues.append("Container should set runAsNonRoot: true.")
        score -= 15

    if "privileged: true" in full_text:
        issues.append("Privileged container detected. This is risky.")
        score -= 25

    if "allowprivilegeescalation: false" not in full_text:
        issues.append("Set allowPrivilegeEscalation: false.")
        score -= 10

    if "namespace:" not in full_text:
        issues.append("No namespace specified.")
        score -= 5

    return max(score, 0), issues

@app.route("/", methods=["GET", "POST"])
def home():
    yaml_text = ""
    results = []
    score = None

    if request.method == "POST":
        yaml_text = request.form.get("yaml_text", "")
        score, results = analyze_yaml(yaml_text)

    return render_template_string(
        HTML,
        yaml_text=yaml_text,
        results=results,
        score=score
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
