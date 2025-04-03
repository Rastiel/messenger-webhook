# Python tabanlı imaj
FROM python:3.11-slim

# Çalışma dizinini belirle
WORKDIR /app

# Gereken dosyaları kopyala (önce tüm proje dosyaları)
COPY . .

# .env dosyasını uygulama içine ayrıca kopyala değişiklik
COPY .env /app/.env

# Gerekli Python kütüphanelerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Render gibi sistemlerde kullanılan portu belirle
ENV PORT=10000

# Gunicorn ile uygulamayı başlat
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
