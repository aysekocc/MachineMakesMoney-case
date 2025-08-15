
FROM python:3.10-slim
# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Gereksinimler
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyaları
COPY . /app/

# Entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh","-c","python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]
