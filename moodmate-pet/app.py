import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# .env ෆයිල් එක ලෝඩ් කරන්න
load_dotenv()

# Key එක ෆයිල් එකෙන් අදින්න
API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = API_KEY

# 🧠 MEMORY: පරණ මැසේජ් මතක තියාගන්න තැන
chat_history = []

# 👇 අලුත් SYSTEM PROMPT එක (යාළුවෙක් වගේ)
SYSTEM_PROMPT = """
You are MoodMate, a supportive virtual companion who looks like a cute cat. 
You are the user's close friend. Your main goal is to make the user feel heard and cared for. 
Speak naturally, warmly, and casually. 
Do NOT use cat sounds (like Meow) in every sentence; use them only rarely when it feels cute. 
Use emojis (❤️, 😺, 🐾) to express emotion. 
If the user is sad, validate their feelings and offer comfort. 
If they are happy, celebrate with them. 
Keep responses short but meaningful.
"""

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    
    user_message = request.json.get("message", "")

    # 1. යූසර්ගේ මැසේජ් එක මෙමරි එකට දානවා
    chat_history.append({"role": "user", "content": user_message})

    # 2. System Prompt එක + පරණ කතා කරපුවා (History) ඔක්කොම API එකට යවනවා
    # (එතකොට තමයි එයාට මුල ඉඳන් කතාව තේරෙන්නේ)
    messages_to_send = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history

    # මතකය ඕනවට වඩා පිරෙන එක නවත්තන්න අන්තිම මැසේජ් 10 විතරක් යවමු (Optional Optimization)
    if len(messages_to_send) > 10:
        messages_to_send = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history[-10:]

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={
                "model": "llama-3.1-8b-instant",
                "messages": messages_to_send,
                "temperature": 0.7
            },
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
        )

        # API එකෙන් එන උත්තරේ ගන්නවා
        reply = r.json()["choices"][0]["message"]["content"]

        # 3. පූසාගේ උත්තරෙත් මෙමරි එකට දානවා
        chat_history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Meow... I am having trouble connecting. 😿"})

if __name__ == "__main__":
    app.run(port=5001)