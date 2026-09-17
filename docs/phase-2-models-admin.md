# Phase 2: Modellar, Admin panel va Seed data

## Bajarilgan ishlar (Completed Tasks):
1. **Umumiy modellar (`apps/core/models.py`):**
   - `Theme` — rang kaliti (`blue`, `cyan`, `purple`, `yellow`, `red`, `emerald`). Bazada Tailwind class'i emas, faqat kalit saqlanadi; frontend uni class'ga aylantiradi.
   - `PublishableModel` — `is_published` (saytda ko'rsatish/yashirish), `order` (tartib), `created_at`, `updated_at`.
2. **Kurslar (`apps/courses`):**
   - `Course` — frontenddagi `lib/data/courses.ts` tipiga mos: `slug`, `title`, `short_desc`, `description`, `icon`, `theme`, `duration`, `level`, `format`, `price`, `seats`, `skills` (JSON ro'yxat), `outcomes` (JSON ro'yxat).
   - `CurriculumItem` — o'quv dasturi bandlari (`week`, `topic`, `order`).
3. **Tadbirlar (`apps/events`):**
   - `Event` — `lib/data/events.ts` ga mos. Sana matn emas, haqiqiy `DateField`; vaqt `start_time`/`end_time` (`TimeField`) — filtrlash va saralash to'g'ri ishlashi uchun. `status`: `upcoming` / `open` / `closed`.
   - `ScheduleItem` — tadbir dasturi (`time`, `activity`).
4. **Admin panel:**
   - Kurs ichida o'quv dasturini, tadbir ichida dasturni jadval ko'rinishida (inline) tahrirlash.
   - Ro'yxatda `order`, `is_published`, `status` ni to'g'ridan-to'g'ri o'zgartirish; qidiruv, filtrlar, sana bo'yicha navigatsiya.
   - `slug` nomdan avtomatik to'ldiriladi. Sarlavha: "Andijon Yoshlar Texnoparki".
5. **Seed data:** `python manage.py seed_data`
   - Frontend mock data'si (`courses.ts`, `events.ts`) JSON'ga o'girilib `apps/core/seed/initial_data.json` ga saqlandi.
   - Buyruq `bg-blue-500` → `blue`, `"12 Oktabr, 2026"` → `2026-10-12`, `"09:00 — 18:00"` → start/end vaqtga aylantiradi.
   - Qayta ishga tushirilsa dublikat yaratmaydi (slug bo'yicha yangilaydi). `--reset` — avval hammasini o'chiradi.
   - Natija: 5 ta kurs, 3 ta tadbir yuklandi.

**Eslatma:** seed data'dagi ba'zi ma'lumotlar (grant summalari, "IT Park Uzbekistan" tashkilotchi, kurs narxlari) frontend mock'idan olingan va rasmiy emas — admin panel orqali haqiqiy ma'lumotga almashtirilishi kerak.

Keyingi bosqich: API endpointlar (Phase 3).
