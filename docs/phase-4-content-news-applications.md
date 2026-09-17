# Phase 4: Sayt kontenti, Yangiliklar, Video stories va Murojaatlar API

## Bajarilgan ishlar (Completed Tasks):
1. **Umumiy (`apps/core`):**
   - `Icon` — barcha bo'limlar uchun yagona ikonka ro'yxati (13 ta: kurs, afzallik, laboratoriya ikonkalari). `Course.icon` ham shunga o'tkazildi.
   - `Theme` ga `orange` rangi qo'shildi.
2. **Sayt kontenti (`apps/content`):**
   - `SiteSettings` — telefon, email, manzil, ish vaqti, xarita, Instagram/Telegram/Facebook/YouTube. Faqat **bitta** yozuv (admin'da ikkinchisini qo'shib/o'chirib bo'lmaydi).
   - `Statistic` — raqam + belgi (`+`) + matn ("5+ Yil Tajriba").
   - `Feature` — "Nega aynan biz?" kartalari (sarlavha, tavsif, ikonka, rang).
   - `Equipment` — laboratoriya jihozlari (+ ixtiyoriy rasm).
   - `Partner` — hamkorlar (nom, ixtiyoriy logotip va sayt havolasi).
3. **Video stories (`apps/projects`):** `VideoStory` — o'quvchi ismi, kurs (bazadagi kursga bog'lanadi yoki matn), natija, video havolasi, muqova rasmi, rang.
4. **Yangiliklar (`apps/news`):** `Post` — slug, sarlavha, toifa, qisqa matn, to'liq matn, muqova, chop etilgan vaqt. Kelajak vaqtga qo'yilgan yangilik o'sha vaqtgacha API'da ko'rinmaydi (rejalashtirib qo'yish mumkin).
5. **Murojaatlar (`apps/applications`):** `Application` — saytdagi formadan kelgan arizalar.
   - Turlari: `contact` (xabar), `course` (kursga yozilish), `event` (tadbirga ro'yxat).
   - Holati: Yangi → Ko'rib chiqilmoqda → Yakunlangan / Rad etilgan; admin izohi.
   - Validatsiya (o'zbekcha xabarlar): ism, telefon formati, kurs/tadbir tanlanganligi, yopilgan tadbirga ro'yxat taqiqlanadi, oddiy xabarda matn majburiy.
   - **Spamga qarshi:** IP bo'yicha soatiga 10 ta (`.env` dagi `APPLICATIONS_THROTTLE_RATE` bilan o'zgartiriladi). Next.js foydalanuvchi IP'sini `X-Forwarded-For` orqali uzatadi.
   - Admin'da arizalarni faqat ko'rish va holatini o'zgartirish mumkin (saytdan kelgan ma'lumot tahrirlanmaydi).
6. **Yangi endpointlar:**
   - `GET /api/site-settings/`, `/api/statistics/`, `/api/features/`, `/api/equipment/`, `/api/partners/`, `/api/video-stories/`
   - `GET /api/news/`, `/api/news/{slug}/`
   - `POST /api/applications/` (ro'yxatni GET bilan olish taqiqlangan — 405)
7. **Seed data:** `seed_data` buyrug'i endi frontend komponentlaridagi barcha mock kontentni ham yuklaydi: sayt sozlamalari, 3 statistika, 5 afzallik, 4 jihoz, 7 hamkor, 4 video story, 1 yangilik. Qayta ishga tushirilsa dublikat yaratmaydi; sayt sozlamalari admin'da o'zgartirilgan bo'lsa ustidan yozilmaydi.
8. **Testlar:** jami 18 ta (yangi 11 ta), hammasi o'tdi — kontent ro'yxatlari, sayt sozlamalari, kelajak yangilik yashirinligi, ariza validatsiyasi, yopilgan tadbir, noma'lum kurs, IP bo'yicha cheklov (429).
9. OpenAPI sxema ogohlantirishsiz validatsiyadan o'tdi (`/api/docs/`).

## Eslatmalar
- Seed kontentidagi hamkorlar ro'yxati, statistika raqamlari, video story'dagi o'quvchilar va yagona yangilik frontend mock'idan olingan — haqiqiy ma'lumot bilan almashtirilishi kerak.
- Email: footer'da `info@texnopark.uz` ko'rsatilgan, lekin havolada `info@andijonyoshlartexnoparki.uz` edi. Seed'ga ko'rsatilgan manzil yozildi — to'g'risini admin'dagi "Sayt sozlamalari"da tekshiring.
- Yangi murojaat kelganda email/Telegram xabarnoma hali yo'q.
