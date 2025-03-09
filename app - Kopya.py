from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Messenger Webhook Çalışıyor!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Facebook webhook doğrulama isteği için
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == "kerembot123":
            print("Webhook doğrulandı!")
            return challenge, 200
        else:
            return "Doğrulama başarısız", 403

    elif request.method == "POST":
        # Facebook mesajları buradan alacak
        data = request.json
        print("Gelen mesaj:", data)
        return "Mesaj alındı", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render’ın atadığı portu al
    app.run(host="0.0.0.0", port=port)
