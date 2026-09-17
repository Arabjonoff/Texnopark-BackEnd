# Phase 8: Jamoa bo'limi (backend)

Frontend qismi: `Texnopark-FrontEnd/docs/phase-25-team-section.md`.

## Bajarilgan ishlar (Completed Tasks):
1. **`TeamMember` modeli (`apps/content`):** ism-familiya, lavozim, rasm (`team/`), qisqacha (300 belgigacha), Telegram va LinkedIn havolalari, tartib raqami, saytda ko'rsatish.
2. **Public API:** `GET /api/team/` — faqat chop etilganlar, admin'dagi tartibda.
3. **Dashboard API:** `/api/dashboard/team/` — to'liq CRUD, rasm yuklash va `photoClear` bilan olib tashlash, qidiruv (ism, lavozim).
4. **Django admin:** "Jamoa" bo'limi (ro'yxatda tartib va holatni o'zgartirish).
5. **Testlar:** jami 35 ta (yangi 3 ta) — public ro'yxatda faqat chop etilganlar, dashboard'da yaratish/tahrirlash/o'chirish, ism va lavozim majburiyligi.
6. **Swagger sxemasi tozalandi:** dashboard serializer'lariga alohida komponent nomlari berildi (`DashboardCourse` va h.k.), auth va statistika endpointlari hujjatlandi, `status` enum nomlari aniqlashtirildi. Endi `spectacular --validate --fail-on-warn` ogohlantirishsiz o'tadi (bu muammo Phase 7 dan qolgan edi).

## Eslatma
Jamoa a'zolari ma'lumoti to'qib chiqarilmadi — bo'lim bo'sh. Haqiqiy ma'lumotlar dashboard orqali kiritiladi; bo'sh bo'lsa bo'lim saytda umuman ko'rinmaydi.
