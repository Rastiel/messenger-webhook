# keepalive.py
import requests
import time

# URL'yi kendi sunucu adresinle güncelle
URL = "http://localhost:10000/webhook"

while True:
    try:
        response = requests.get(URL)
        print(f"Ping attık! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    time.sleep(10)
