import os
import random
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API securely from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


# -------------------------------
# Helper Functions
# -------------------------------

def life_path_number(dob):
    digits = [int(c) for c in dob if c.isdigit()]
    total = sum(digits)
    if total in [11, 22, 33]:
        return total
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total


def detect_problem_category(message):
    message = message.lower()
    categories = {
        "study": ["study", "exam", "college", "assignment", "homework", "marks"],
        "career": ["career", "job", "work", "office", "promotion", "salary"],
        "love": ["love", "relationship", "crush", "breakup", "boyfriend", "girlfriend"],
        "stress": ["stress", "tension", "anxiety", "sad", "tired", "pressure"]
    }

    for cat, keywords in categories.items():
        if any(k in message for k in keywords):
            return cat
    return "general"


# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    category = detect_problem_category(user_input)

    prompt = f"""
You are Buddy 🤖 — a warm, funny, and kind life advisor AI friend for college students.
The user said: "{user_input}"

Based on their message, the mood category is: {category}.
Give a short, motivating, or comforting response — like a real friend — with emojis and positivity.
If relevant, suggest a motivational movie, song, or food.
    """

    try:
        response = model.generate_content(prompt)
        bot_reply = response.text.strip()
    except Exception:
        bot_reply = "Oops 😅 I'm having trouble connecting to my thoughts right now. Try again later!"

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
