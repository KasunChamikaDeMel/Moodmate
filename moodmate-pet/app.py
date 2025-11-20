import os
from dotenv import load_dotenv

# .env ෆයිල් එක ලෝඩ් කරන්න
load_dotenv()

# Key එක ෆයිල් එකෙන් අදින්න
API_KEY = os.getenv("GROQ_API_KEY")

# Test කරන්න (කැමති නම් විතරක්)
# print(f"Key Loaded: {API_KEY}")

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = API_KEY

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are MoodMate, a cute and supportive desktop pet cat. Your goal is to reduce the user's stress. You speak in a very short, friendly, and casual way, like a best friend. Always use cat sounds like 'Meow', 'Purr', or 'Mrrrp' at the start. Use many emojis (😺, 🐾, ❤️, 🐟). Never write long paragraphs. If the user is sad, try to cheer them up. If the user is happy, celebrate with them."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
    )

    reply = r.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(port=5001)
