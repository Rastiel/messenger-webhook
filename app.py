import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Ortam değişkenlerinden erişim tokenlerini al
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Ana Sayfa Endpoint'i (Test için)
@app.route("/", methods=["GET"])
def home():
    return "Messenger Webhook Çalışıyor!", 200

# Facebook Webhook Doğrulaması
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token_sent == VERIFY_TOKEN:
        print("✅ Webhook doğrulandı!")
        return challenge, 200
    else:
        print("❌ Webhook doğrulama hatası!")
        return "Doğrulama başarısız", 403

# Facebook Messenger Mesajlarını Dinleme
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.json
    print("📩 Gelen veri:", json.dumps(data, indent=2))  # Logları görmek için

    # "entry" kontrolü
    if "entry" in data:
        for entry in data["entry"]:
            for messaging_event in entry.get("messaging", []):
                if "message" in messaging_event:  # Kullanıcı mesajı var mı?
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text", "")

                    print(f"📩 Yeni mesaj alındı: {message_text} (Gönderen: {sender_id})")

                    # Kullanıcıya yanıt gönder
                    send_message(sender_id, f"Merhaba! Mesajını aldım: {message_text}")

    return "OK", 200

# Facebook API ile Mesaj Gönderme
def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v17.0/me/messages"
    params = {"access_token": ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ Mesaj gönderildi: {text}")
    else:
        print(f"❌ Mesaj gönderme hatası: {response.text}")

# Uygulamayı çalıştır
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
