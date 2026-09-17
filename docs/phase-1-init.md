# Phase 1: Backend loyihasini ochish

## Bajarilgan ishlar (Completed Tasks):
1. **Texnologiya tanlandi:** TZ (§31) talabiga ko'ra `Next.js → REST API → Django → SQLite` arxitekturasi. Python 3.14, Django 6.1, Django REST Framework 3.18.
2. **Papka:** `Yoshlar-Texnopark/Texnopark-Back` — frontend papkasi yonida alohida loyiha.
3. **Virtual muhit:** `.venv` yaratildi, barcha paketlar `requirements.txt` ga yozildi:
   - `djangorestframework` — REST API
   - `django-cors-headers` — Next.js (`localhost:3000`) so'rovlariga ruxsat
   - `django-filter` — `?status=open` kabi filtrlar
   - `drf-spectacular` — Swagger hujjat (`/api/docs/`)
   - `djangorestframework-camel-case` — javoblar frontend kabi camelCase formatda
   - `Pillow` (keyinchalik rasmlar uchun), `python-dotenv` (`.env` sozlamalari)
4. **Sozlamalar (`config/settings.py`):**
   - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` — `.env` dan o'qiladi (`.env.example` namuna).
   - Til `uz`, vaqt zonasi `Asia/Tashkent`.
   - `MEDIA_ROOT`/`STATIC_ROOT` sozlandi.
5. **Ilovalar (apps):** `apps/core` (umumiy), `apps/courses`, `apps/events`.
6. **`.gitignore`:** `.venv`, `.env`, `db.sqlite3`, `media/` git'ga tushmaydi.

Keyingi bosqich: modellar va admin panel (Phase 2).
