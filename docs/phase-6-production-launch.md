# Phase 6: Serverga birinchi yuklash (production)

Sana: 2026-09-17. Sayt: **https://yoshlar-texnoparki.uz** (admin: `/admin/`, API hujjati: `/api/docs/`).

## Bajarilgan ishlar (Completed Tasks):
1. **GitHub:** kod `Arabjonoff/Texnopark-BackEnd` va `Arabjonoff/Texnopark-FrontEnd` (public) repolariga `main` branch'ga yuklandi.
2. **Server tahlili (5.104.108.235, Ubuntu 22.04, 6 CPU, 15 GB RAM):** server boshqa loyihalar bilan umumiy — selen-crm (portlar 3000/8000), barormebel (8001), zelly, workers, mehmon.zelly, gift.yoshlar-texnoparki. Docker, Nginx, certbot oldindan o'rnatilgan.
   - Shu sababli Texnopark portlari **8010** (backend) va **3010** (frontend), faqat `127.0.0.1` da.
   - Boshqa saytlarning Nginx fayllari, konteynerlari va sertifikatlariga tegilmadi. Eski image'larni tozalash faqat `texnopark` loyihasi image'lariga qo'llanadi.
3. **Server sozlamalari:**
   - `deploy` foydalanuvchisi (docker guruhida), `/opt/texnopark/{Texnopark-Back,Texnopark-Front,data,backups}`.
   - `deploy/.env` — tasodifiy `DJANGO_SECRET_KEY`, domen, HTTPS sozlamalari (faqat serverda, `chmod 600`).
   - Nginx: `/etc/nginx/sites-available/yoshlar-texnoparki.uz`; Let's Encrypt sertifikati (`yoshlar-texnoparki.uz`, `www`), HTTP → HTTPS yo'naltirish, avtomatik yangilanadi.
4. **Tuzatish:** `package-lock.json` Docker'dagi npm 11.19 bilan mos emas edi (`npm ci` xatosi) — yetishmagan ixtiyoriy WASM paketlari qo'shildi, `node:24-alpine` ichida tekshirildi.
5. **Kontent:** `seed_data` bilan boshlang'ich kontent yuklandi.
6. **GitHub Actions uchun SSH kalit:** ochiq qismi serverdagi `deploy` foydalanuvchisiga qo'shildi va ulanish tekshirildi. Yopiq kalit kompyuterda: `Yoshlar-Texnopark/github-actions-deploy-key` (git'ga tushmaydi).
7. **Backup:** `deploy/backup.sh` — SQLite backup API orqali to'g'ri nusxa + media, `/opt/texnopark/backups`, 14 kun saqlanadi. Cron: har kuni 03:00. Birinchi backup yaratildi va ichi tekshirildi.

## Tekshiruv (internet orqali)
- `/`, `/about`, `/courses/python`, `/events/robotics-challenge`, `/news`, `/contact?course=python` — 200, API ma'lumotlari ko'rinadi; `/news/yoq` — 404.
- `/admin/login/` — 200, admin CSS (`/static/`) — 200; `/api/statistics/` — 200.
- HTTP → HTTPS (301), `www` — ishlaydi.
- Aloqa formasi production'da yuborildi → ariza bazaga yozildi (sinov arizasi o'chirildi).
- Boshqa saytlar (selen-crm, zelly, workers, gift) ishlashda davom etmoqda.

## Qo'lda bajarilishi kerak
- Admin foydalanuvchi yaratish (`createsuperuser`).
- GitHub'ning ikkala reposiga `SSH_HOST`, `SSH_USER`, `SSH_KEY` secret'larini qo'shish — shundan keyin `main` ga push avtomatik deploy qiladi.
- Server root paroli chatda ochiq yozilgan — **almashtirish** tavsiya etiladi.
