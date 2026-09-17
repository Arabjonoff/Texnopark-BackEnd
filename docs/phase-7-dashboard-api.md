# Phase 7: Dashboard API (boshqaruv paneli uchun)

Django admin o'rniga Next.js'da alohida boshqaruv paneli qilindi. Bu bosqich — uning backend qismi. Frontend: `Texnopark-FrontEnd/docs` (phase-24).

## Bajarilgan ishlar (Completed Tasks):
1. **Yangi ilova `apps/dashboard`** — barcha endpointlar `/api/dashboard/` ostida.
2. **Autentifikatsiya:**
   - `POST /api/dashboard/auth/login/` — login/parol → token (+ amal qilish muddati, foydalanuvchi ma'lumoti). Faqat **staff** (`is_staff`) foydalanuvchilar kira oladi.
   - Har kirishda yangi token, eskilari bekor bo'ladi. `POST auth/logout/` tokenni o'chiradi, `GET auth/me/` — joriy foydalanuvchi.
   - `ExpiringTokenAuthentication` — token muddati `DASHBOARD_TOKEN_TTL_HOURS` (standart 72 soat); muddati o'tgan token o'chiriladi.
   - Login'ga parol tanlab topishga qarshi cheklov: daqiqasiga 5 ta (`LOGIN_THROTTLE_RATE`).
   - Barcha boshqa endpointlar `IsAdminUser` bilan yopiq (tokensiz — 401).
3. **Statistika — `GET /api/dashboard/stats/`:** arizalar (jami, yangi, 30 kun va oldingi 30 kun, tur va holat bo'yicha, 30 kunlik kunlik qator), kurslar, tadbirlar (yaqin, ro'yxati ochiq), yangiliklar, so'nggi 6 ta ariza, yaqin 4 ta tadbir.
4. **CRUD (sahifalash `?page=&page_size=`, qidiruv `?search=`, filtrlar, `?ordering=`):**
   - `courses/` — o'quv dasturi bilan birga yoziladi (qatorlar to'liq almashtiriladi), `applicationsCount`.
   - `events/` — dastur (jadval) bilan; tugash vaqti boshlanishdan keyin bo'lishi tekshiriladi.
   - `news/` — muqova rasmi (multipart), `coverClear=true` bilan rasmni olib tashlash.
   - `statistics/`, `features/`, `equipment/` (rasm), `partners/` (logotip), `video-stories/` (muqova, kursga bog'lash yoki matn).
   - `applications/` — ko'rish, filtrlash (holat, tur, kurs, tadbir), faqat **holat va ichki izohni** o'zgartirish, o'chirish. Saytdan kelgan ma'lumot tahrirlanmaydi; yangi ariza yaratish taqiqlangan.
   - `site-settings/` — GET / PUT / PATCH (bitta yozuv).
5. **Slug:** bo'sh qoldirilsa sarlavhadan avtomatik yaratiladi ("Sun'iy intellekt" → `suniy-intellekt`), band bo'lsa `-2` qo'shiladi; qo'lda band slug kiritilsa o'zbekcha xato.
6. **Testlar:** jami 32 ta (yangi 14 ta) — login/noto'g'ri parol/staff bo'lmagan, 401, muddati o'tgan token, logout, statistika, kurs + dastur yaratish/yangilash, band slug, tadbir vaqt validatsiyasi, ariza faqat holat, rasm yuklash va olib tashlash, video story kurs nomi, sayt sozlamalari, sahifalash va qidiruv.

## Muhit o'zgaruvchilari (ixtiyoriy)
| O'zgaruvchi | Standart | Izoh |
| --- | --- | --- |
| `DASHBOARD_TOKEN_TTL_HOURS` | `72` | Dashboard sessiyasi muddati |
| `LOGIN_THROTTLE_RATE` | `5/minute` | Login urinishlari cheklovi |

## Kirish uchun foydalanuvchi
Dashboard'ga faqat staff foydalanuvchi kiradi:
```bash
docker compose -f deploy/docker-compose.yml exec backend python manage.py createsuperuser
```
