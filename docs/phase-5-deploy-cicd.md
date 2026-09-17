# Phase 5: Production sozlamalari, Docker va CI/CD

## Bajarilgan ishlar (Completed Tasks):
1. **Tanlangan yo'l:** bitta Ubuntu VPS + Docker Compose + Nginx (HTTPS certbot) + GitHub Actions. Qadam-baqadam qo'llanma: `docs/DEPLOY.md`.
2. **Production sozlamalari (`config/settings.py`), hammasi `.env` orqali:**
   - `DJANGO_CSRF_TRUSTED_ORIGINS` — HTTPS domendagi admin panel uchun.
   - `PUBLIC_BASE_URL` — rasm URL'lari ochiq domen bilan qaytadi (frontend API'ga ichki `http://backend:8000` orqali murojaat qilgani uchun busiz rasmlar brauzerda ochilmas edi). Tekshirildi: `https://texnopark.uz/media/partners/a.png`.
   - `SQLITE_PATH`, `MEDIA_ROOT` — baza va rasmlar Docker volume'da.
   - `DEBUG=False` bo'lganda: `SECURE_PROXY_SSL_HEADER`, secure cookie'lar, `nosniff`; loglar konsolga.
3. **`gunicorn`** qo'shildi (`requirements.txt`).
4. **`Dockerfile`** — python 3.14-slim, root bo'lmagan foydalanuvchi; `docker/entrypoint.sh` har ishga tushishda `migrate` va `collectstatic` qiladi.
5. **`deploy/`:**
   - `docker-compose.yml` — backend (faqat `127.0.0.1:8000`, healthcheck bilan) va frontend (`127.0.0.1:3000`). Frontend build'i ishlab turgan backend'dan ma'lumot oladi (`build.network: host`), ishlash paytida esa ichki tarmoq orqali.
   - `deploy.sh backend|frontend|all` — `git reset` ga origin/main, konteynerlarni qayta build, eski image'larni tozalash.
   - `nginx/texnopark.conf` — `/` → Next.js, `/admin` va `/api` → Django, `/static` va `/media` diskdan; `X-Forwarded-For` `$remote_addr` bilan almashtiriladi (spam cheklovini aldab bo'lmaydi); 10 MB yuklash chegarasi.
   - `.env.example` — production o'zgaruvchilari namunasi.
6. **GitHub Actions (`.github/workflows/ci-cd.yml`):**
   - `test`: `makemigrations --check`, `manage.py check`, testlar (har push va PR).
   - `deploy`: faqat `main` ga push va testlar o'tsa — SSH orqali `deploy.sh backend`. Secrets: `SSH_HOST`, `SSH_USER`, `SSH_KEY`, `SSH_PORT`.
7. `.gitattributes` — `.sh` fayllar LF bilan saqlanadi (Windows'da tahrirlansa ham Linux'da ishlaydi).

## Tekshiruv
- 18 ta test o'tdi, `manage.py check` xatosiz.
- `check --deploy` (DEBUG=False): faqat HSTS/SSL redirect ogohlantirishlari (Nginx + certbot `--redirect` hal qiladi) va console email backend (sayt hozircha email yubormaydi).
- docker-compose va workflow YAML fayllari, `deploy.sh`/`entrypoint.sh` sintaksisi tekshirildi.
- **Docker image'lar lokal build qilinmadi** — ishlab chiqish kompyuterida Docker o'rnatilmagan. Birinchi haqiqiy tekshiruv serverda (`DEPLOY.md` 5-qadam) bo'ladi.

## Keyinchalik
- Trafik oshsa SQLite o'rniga PostgreSQL.
- Yangi murojaatlar uchun Telegram/email xabarnoma.
- Backup'larni avtomatik tashqi joyga ko'chirish.
