from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "kerembot123"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Geçersiz doğrulama token'ı", 403

    elif request.method == 'POST':
        data = request.json
        print(data)  # Gelen mesajları terminalde logla
        return "OK", 200

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Varsayılan 10000, ama Render’ın sağladığı PORT varsa onu al
    app.run(host='0.0.0.0', port=port, debug=True)

