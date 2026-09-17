# Phase 3: REST API endpointlar, Swagger va Testlar

## Bajarilgan ishlar (Completed Tasks):
1. **Endpointlar (faqat o'qish — `ReadOnlyModelViewSet`):**
   - `GET /api/courses/` — ro'yxat (yengil: id, title, shortDesc, icon, theme, duration, level, price, seats)
   - `GET /api/courses/{slug}/` — to'liq: description, format, skills, curriculum, outcomes
   - `GET /api/events/` — ro'yxat; filtrlar: `?status=`, `?category=`, `?search=`, `?ordering=date`
   - `GET /api/events/{slug}/` — to'liq: description, prizes, schedule, requirements, organizer
   - `is_published=False` bo'lgan yozuvlar API'da ko'rinmaydi (404).
2. **Frontend bilan moslik:**
   - `id` maydoni = `slug`, shuning uchun `/courses/flutter`, `/events/andijon-ideathon-2026` URL'lari o'zgarmaydi.
   - Javoblar camelCase (`shortDesc`, `dateIso`) — frontend TypeScript tiplari bilan bir xil.
   - Tadbirda `date` — tayyor o'zbekcha matn (`12 Oktabr, 2026`), `dateIso` — saralash uchun, `time` — `09:00 — 18:00`.
   - Frontend farqi: `color`/`colorLight` o'rniga `theme`, kursda `icon` komponent o'rniga matn kaliti.
3. **Detal so'rovlarda `prefetch_related`** — dastur bandlari bitta qo'shimcha so'rov bilan olinadi (N+1 yo'q).
4. **Swagger:** `/api/docs/` (OpenAPI sxema `/api/schema/`), sxema ogohlantirishsiz validatsiyadan o'tdi.
5. **CORS:** `http://localhost:3000` dan so'rovlarga ruxsat berildi va tekshirildi.
6. **Testlar (`apps/core/tests.py`) — 7 ta, hammasi o'tdi:**
   - seed qayta ishga tushganda dublikat yo'qligi
   - camelCase va slug-id formati
   - kurs detal (curriculum, skills)
   - yashirilgan kurs 404 qaytarishi
   - tadbir sana/vaqt formati frontend bilan bir xilligi
   - status bo'yicha filtr
   - API'ga yozish (POST) taqiqlanganligi (405)
7. **Jonli tekshiruv:** `runserver` ishga tushirilib `/api/events/`, `/api/docs/` (200), `/admin/` (302 → login) tekshirildi.

## Keyingi qadamlar
- ~~Frontendni API'ga ulash~~ — bajarildi (frontend phase-20).
- ~~`news`, `projects` (video stories), `partners` ilovalari~~ — bajarildi (Phase 4).
- ~~`applications` — formalar uchun POST endpoint~~ — bajarildi (Phase 4).
- Production: `DEBUG=False`, gunicorn + nginx, PostgreSQL.

## Yangilanish
Frontend API'ga ulandi — batafsil: `Texnopark-Front/docs/phase-20-api-integration.md`. Frontend `npm run build` qilinayotganda ushbu server ishlab turishi kerak.
