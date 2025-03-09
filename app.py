from flask import Flask, request
import requests

app = Flask(__name__)

# Facebook sayfanın erişim tokeni (Facebook Developer Console'dan al)
PAGE_ACCESS_TOKEN = "EAAcMzA5v2OIBO9Ja99OmglYhTE91lNM0CL3y3g2uPIF44gJKkMH6eVZAMIpC0PpAmuKrLF1GqmNzOdZACQtiz0IELCd7fGtMyPRjp8aY1OBoZADvEYuNHG2j7Hd11YyxZAAJcJhBZB5uOYj44SlVB1N8EW0vxXYmWlR3ed4POIjoNdNrCXaZCS0CtiIz5KHDA57QkIIKXTVgZDZD"  # Bunu kendi sayfanın tokeni ile değiştir

# Webhook doğrulama tokeni
VERIFY_TOKEN = "kerembot123"

@app.route('/', methods=['GET'])
def home():
    return "Messenger Webhook Çalışıyor!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':  # Webhook doğrulama isteği
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Forbidden", 403

    elif request.method == 'POST':  # Gelen mesajları al
        data = request.get_json()
        print("Gelen mesaj:", data)  # Gelen veriyi loglara yaz

        if data["object"] == "page":
            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:
                    if "message" in messaging_event:  # Gelen mesaj var mı?
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]

                        print(f"Gelen mesaj: {message_text} - Gönderen ID: {sender_id}")

                        # Gelen mesaja yanıt gönder
                        send_message(sender_id, "Merhaba! Ben bir botum. Nasıl yardımcı olabilirim?")

        return "OK", 200

def send_message(recipient_id, message_text):
    """Facebook Messenger API üzerinden mesaj gönderir."""
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post("https://graph.facebook.com/v12.0/me/messages",
                             params=params, headers=headers, json=data)
    print("Yanıt Gönderildi:", response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
