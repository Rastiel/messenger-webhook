from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Facebook doğrulama token'ı
VERIFY_TOKEN = "kerembot123"
ACCESS_TOKEN = "EAAcMzA5v2OIBO9Ja99OmglYhTE91lNM0CL3y3g2uPIF44gJKkMH6eVZAMIpC0PpAmuKrLF1GqmNzOdZACQtiz0IELCd7fGtMyPRjp8aY1OBoZADvEYuNHG2j7Hd11YyxZAAJcJhBZB5uOYj44SlVB1N8EW0vxXYmWlR3ed4POIjoNdNrCXaZCS0CtiIz5KHDA57QkIIKXTVgZDZD"  # Sayfa erişim token'ını ekle

@app.route("/", methods=["GET"])
def home():
    return "Messenger Webhook Çalışıyor!", 200

@app.route("/webhook", methods=["GET"])
def verify():
    """ Facebook webhook doğrulama """
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    verify_token = request.args.get("hub.verify_token")

    if mode == "subscribe" and verify_token == VERIFY_TOKEN:
        print("✅ Webhook doğrulandı!")
        return challenge, 200
    else:
        return "❌ Doğrulama başarısız", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    """ Messenger'dan gelen mesajları alır ve yanıtlar """
    data = request.json
    print("📩 Gelen mesaj:", json.dumps(data, indent=2))  # Logları görmek için ekledik

    if "entry" in data:
        for entry in data["entry"]:
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                if "message" in messaging_event:
                    message_text = messaging_event["message"]["text"]
                    print(f"📩 {sender_id} kişisinden mesaj: {message_text}")

                    # Otomatik cevap gönderme
                    send_message(sender_id, f"Merhaba! Mesajını aldım: {message_text}")

    return "OK", 200

def send_message(recipient_id, text):
    """ Kullanıcıya mesaj gönderme fonksiyonu """
    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE",
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"📤 Mesaj gönderildi: {response.status_code}, {response.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
