from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "kerembot123"


@app.route('/webhook', methods=['GET'])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token_sent == VERIFY_TOKEN:
        return challenge  # Eğer token doğruysa challenge'ı geri döndür
    return "Invalid verification token", 403  # Yanlışsa 403 hata kodu ver


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # HOST eklendi!
