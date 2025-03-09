import os
import json
import requests
from flask import Flask, request
from dotenv import load_dotenv  # .env dosyasını okumak için

# Çevre değişkenlerini yükle
load_dotenv()

app = Flask(__name__)

# Facebook API için Token'lar
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Webhook doğrulama tokeni
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Facebook API erişim tokeni


@app.route("/", methods=["GET"])
def home():
    return "Messenger Webhook Çalışıyor!", 200


# Webhook doğrulama
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook doğrulandı!")
        return challenge, 200
    else:
        print("❌ Webhook doğrulama başarısız!")
        return "Forbidden", 403


# Facebook'tan gelen mesajları işleyen POST isteği
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    print("📩 Gelen mesaj:", json.dumps(data, indent=2))  # Loglar

    if "entry" in data:
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if "message" in messaging_event and "text" in messaging_event["message"]:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]

                    print(f"📥 Kullanıcıdan gelen mesaj: {message_text}")

                    response_text = f"Merhaba! Sen şöyle dedin: {message_text}"
                    send_message(sender_id, response_text)

    return "OK", 200


# Facebook'a cevap gönderen fonksiyon
def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, params=params, headers=headers, json=payload)

    print("📤 Gönderilen Mesaj:", json.dumps(payload, indent=2))
    print("📥 Facebook API Cevabı:", response.json())  # API cevabını logla


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
