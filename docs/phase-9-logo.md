# Phase 9: Sayt logotipi (backend)

Frontend qismi: `Texnopark-FrontEnd/docs/phase-28-logo-and-hero-card.md`.

## Bajarilgan ishlar (Completed Tasks):
1. **`SiteSettings.logo`** — `ImageField(upload_to='logo/')`, ixtiyoriy. `help_text` da qanday rasm kerakligi yozilgan (kvadrat 1:1, shaffof fonli PNG/SVG, kamida 200x200 px) — bu matn Django admin'da ham, dashboard formasida ham ko'rinadi.
2. **Public API:** `GET /api/site-settings/` javobiga `logo` qo'shildi (to'liq URL yoki `null`).
3. **Dashboard API:** `PATCH /api/dashboard/site-settings/` orqali logo yuklanadi; `ImageClearMixin` ga `logo` qo'shilgani uchun `logoClear=true` bilan olib tashlanadi.
4. **Django admin:** "Sayt sozlamalari" ga "Logotip" bo'limi qo'shildi. Yo'l-yo'lakay **"Bosh sahifa kartasi"** (`hero_image`, `hero_video_url`) ham qo'shildi — ular Phase 8 da yaratilgan, lekin admin `fieldsets` iga kiritilmagan edi, shuning uchun Django admin'dan tahrirlab bo'lmasdi (dashboard orqali ishlagan).
5. **Migratsiya:** `content/0004_sitesettings_logo.py`.

## Tekshiruv
- 37 ta test o'tdi, `manage.py check` xatosiz.
- Jonli tekshirildi: logo yuklandi → `/api/site-settings/` da URL qaytdi va saytda ko'rindi; dashboard'da "Rasmni olib tashlash" belgilanib saqlandi → `logo: null` va saytda "YT" harflari qaytdi.
- Sinov logotipi va hero rasmi tekshiruvdan keyin bazadan va `media/` dan o'chirildi.
