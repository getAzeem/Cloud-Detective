from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Checker</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding: 60px;
        }
        .box {
            background: #111827;
            max-width: 500px;
            margin: auto;
            padding: 30px;
            border-radius: 16px;
        }
        input {
            width: 90%;
            padding: 14px;
            border-radius: 8px;
            border: none;
            margin: 15px;
        }
        button {
            padding: 12px 22px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            font-size: 22px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔐 Password Strength Checker</h1>
        <p>Check how strong your password is.</p>

        <form method="POST">
            <input type="password" name="password" placeholder="Enter password">
            <br>
            <button type="submit">Check Strength</button>
        </form>

        {% if result %}
            <div class="result">{{ result }}</div>
            <p>{{ tips }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

def check_password(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1

    if score <= 2:
        return "Weak ❌", "Use uppercase, lowercase, numbers, symbols, and at least 8 characters."
    elif score == 3 or score == 4:
        return "Medium ⚠️", "Good, but add more length or special characters."
    else:
        return "Strong ✅", "Great password structure."

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    tips = None

    if request.method == "POST":
        password = request.form.get("password", "")
        result, tips = check_password(password)

    return render_template_string(HTML, result=result, tips=tips)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
