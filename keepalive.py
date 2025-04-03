import requests
import time

URL = "tartes.varacron.com:10000"

while True:
    try:
        response = requests.get(URL)
        print(f"Ping attık! Status Code: {response.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    time.sleep(10)  # 10 saniyede bir çalıştır
