from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "gaming-app-secret-key-2024")

# HTML Template (embedded for simplicity)
GAME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Number Guessing Game</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 10px; font-size: 2em; }
        .subtitle { color: #666; margin-bottom: 25px; }
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            padding: 15px;
            background: #f0f4ff;
            border-radius: 12px;
        }
        .stat-item { display: flex; flex-direction: column; }
        .stat-label { font-size: 0.85em; color: #666; }
        .stat-value { font-size: 1.5em; font-weight: bold; color: #667eea; }
        input[type="number"] {
            width: 100%;
            padding: 15px;
            font-size: 1.2em;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
        }
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button, .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 1.1em;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
        }
        button:hover, .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102,126,234,0.4);
        }
        .message {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            font-weight: 500;
        }
        .message.info { background: #e3f2fd; color: #1565c0; }
        .message.success { background: #e8f5e9; color: #2e7d32; }
        .message.error { background: #ffebee; color: #c62828; }
        .message.warning { background: #fff3e0; color: #e65100; }
        .hint { font-size: 0.9em; color: #666; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 Number Guessing Game</h1>
        <p class="subtitle">Guess a number between 1 and {{ max_num }}</p>

        <div class="stats">
            <div class="stat-item">
                <span class="stat-label">Attempts</span>
                <span class="stat-value">{{ attempts }}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Best Score</span>
                <span class="stat-value">{{ best_score if best_score else '-' }}</span>
            </div>
        </div>

        {% if message %}
            <div class="message {{ message_type }}">{{ message }}</div>
        {% endif %}

        {% if not game_over %}
            <form method="POST" action="/guess">
                <input type="number" name="guess" min="1" max="{{ max_num }}"
                       placeholder="Enter your guess..." required autofocus>
                <button type="submit">🎯 Submit Guess</button>
            </form>
            <p class="hint">💡 Tip: Try to guess in fewer attempts!</p>
        {% else %}
            <a href="/reset" class="btn">🔄 Play Again</a>
        {% endif %}
    </div>
</body>
</html>
"""

MAX_NUMBER = 100


@app.route("/")
def index():
    if "target" not in session:
        session["target"] = random.randint(1, MAX_NUMBER)
        session["attempts"] = 0
        session["game_over"] = False
        session["message"] = "Start guessing!"
        session["message_type"] = "info"

    return render_template_string(
        GAME_TEMPLATE,
        max_num=MAX_NUMBER,
        attempts=session.get("attempts", 0),
        best_score=session.get("best_score"),
        message=session.get("message"),
        message_type=session.get("message_type", "info"),
        game_over=session.get("game_over", False),
    )


@app.route("/guess", methods=["POST"])
def guess():
    try:
        user_guess = int(request.form.get("guess", 0))
    except ValueError:
        session["message"] = "❌ Please enter a valid number!"
        session["message_type"] = "error"
        return redirect(url_for("index"))

    if user_guess < 1 or user_guess > MAX_NUMBER:
        session["message"] = f"⚠️ Please enter a number between 1 and {MAX_NUMBER}."
        session["message_type"] = "warning"
        return redirect(url_for("index"))

    target = session.get("target", random.randint(1, MAX_NUMBER))
    session["attempts"] = session.get("attempts", 0) + 1

    if user_guess == target:
        attempts = session["attempts"]
        best = session.get("best_score")
        if best is None or attempts < best:
            session["best_score"] = attempts
            session["message"] = (
                f"🏆 CORRECT! You guessed it in {attempts} attempts. "
                f"New best score!"
            )
        else:
            session["message"] = (
                f"🎉 CORRECT! You guessed it in {attempts} attempts."
            )
        session["message_type"] = "success"
        session["game_over"] = True
    elif user_guess < target:
        session["message"] = f"📈 Too low! Try a higher number. (Attempt {session['attempts']})"
        session["message_type"] = "info"
    else:
        session["message"] = f"📉 Too high! Try a lower number. (Attempt {session['attempts']})"
        session["message_type"] = "info"

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.pop("target", None)
    session.pop("attempts", None)
    session.pop("game_over", None)
    session.pop("message", None)
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
