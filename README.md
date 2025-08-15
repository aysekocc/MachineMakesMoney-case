
# Banka Ekstre Yükleme ve KPI - Django REST API

Bu repository, *Backend Developer Case Study* için hazırlanmış çalışır örnek bir Django REST API projesidir.
Amaç: kullanıcıların CSV banka ekstrelerini yükleyip, işlemleri listeleyip KPI raporu alabilmeleri.

## Özellikler (MVP)
- Kayıt / Giriş (JWT - djangorestframework-simplejwt)
- CSV yükleme endpoint'i: `POST /api/transactions/upload/`  
  - Header: `Authorization: Bearer <token>`, `Idempotency-Key: <key>`
  - multipart/form-data alanı: `file`
  - Atomic yükleme, duplicate kontrolü (user + unique_hash)
- Transaction listeleme: `GET /api/transactions/` (filtreler için query params)
- KPI raporu: `GET /api/reports/summary/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- Swagger/OpenAPI via drf-spectacular
- Örnek CSV ve tests

## Hızlı başlangıç (local, sqlite)

1. Ortam oluştur:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Ayarlar (opsiyonel): `.env` dosyası ekleyebilirsiniz. Varsayılan sqlite kullanılır.

3. Migration ve kullanıcı oluştur:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Çalıştır:
```bash
python manage.py runserver
```

5. API doc: `http://127.0.0.1:8000/api/docs/`

## Docker (opsiyonel)
Repo'da `docker-compose.yml` örneği bulunuyor. PostgreSQL kullanmak istiyorsanız env ayarlarını README'deki gibi yapılandırın.

## Örnek Kullanım (curl)
Kayıt:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"pass1234"}'
```

Giriş:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"pass1234"}'
```

CSV yükleme:
```bash
curl -X POST http://127.0.0.1:8000/api/transactions/upload/ \
 -H "Authorization: Bearer <access_token>" \
 -H "Idempotency-Key: abc-123" \
 -F "file=@sample_data/sample_transactions.csv"
```

## Testler
```bash
pytest
```

## Notlar
- Bu proje bir başlangıç iskeletidir ve case study gereksinimlerine uygun şekilde genişletilebilir (Postgres, Celery, otomatik kategorileme vb).
