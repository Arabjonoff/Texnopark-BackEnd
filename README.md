# Andijon Yoshlar Texnoparki — Backend (REST API)

Django + Django REST Framework + SQLite. Frontend: `../Texnopark-Front/andijon-yoshlar-texnoparki` (Next.js).

## Ishga tushirish

```bash
python -m venv .venv
.venv\Scripts\activate            # Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env            # DJANGO_SECRET_KEY ni o'zgartiring
python manage.py migrate
python manage.py seed_data        # frontend mock data'sini bazaga yuklash
python manage.py createsuperuser  # admin panel uchun
python manage.py runserver
```

| Manzil | Tavsif |
| --- | --- |
| http://127.0.0.1:8000/admin/ | Admin panel (kurs va tadbirlarni boshqarish) |
| http://127.0.0.1:8000/api/docs/ | Swagger — API hujjati |
| http://127.0.0.1:8000/api/schema/ | OpenAPI sxema |

## Endpointlar

| Metod | URL | Tavsif |
| --- | --- | --- |
| GET | `/api/courses/`, `/api/courses/{slug}/` | Kurslar (`?search=`) |
| GET | `/api/events/`, `/api/events/{slug}/` | Tadbirlar (`?status=open`, `?category=`, `?search=`, `?ordering=date`) |
| GET | `/api/news/`, `/api/news/{slug}/` | Yangiliklar (kelajak sanadagilari yashirin) |
| GET | `/api/site-settings/` | Telefon, email, manzil, ijtimoiy tarmoqlar |
| GET | `/api/statistics/` | Statistika raqamlari |
| GET | `/api/features/` | "Nega aynan biz?" kartalari |
| GET | `/api/equipment/` | Laboratoriya jihozlari |
| GET | `/api/partners/` | Hamkorlar |
| GET | `/api/video-stories/` | O'quvchilar natijalari |
| POST | `/api/applications/` | Forma: kursga yozilish / tadbirga ro'yxat / xabar (10 ta/soat, IP bo'yicha) |

Formadan boshqa hamma endpoint faqat o'qish uchun. Kontent va kelgan murojaatlar admin panelda boshqariladi.

## Javob formati

- Maydon nomlari **camelCase** (`shortDesc`, `dateIso`) — frontend tiplari bilan bir xil.
- `id` — bu `slug` (`flutter`, `andijon-ideathon-2026`), frontend URL'lari shunga asoslangan.
- `theme` (`blue`, `purple`, ...) va `icon` (`smartphone`, `cpu`, ...) — kalitlar. Yangi ikonka qo'shilsa frontenddagi `components/ui/DynamicIcon.tsx` ham yangilanadi. Tailwind class'lari va lucide ikonkalari frontendda shu kalit bo'yicha tanlanadi.
- Rasmlar (`logo`, `thumbnail`, `cover`, `image`) — to'liq URL yoki `null`.
- Tadbir `date` — tayyor matn (`12 Oktabr, 2026`), `dateIso` — `2026-10-12`, `time` — `09:00 — 18:00`.

## Tuzilma

```
config/            settings, urls
apps/core/         umumiy modellar (Theme, Icon, PublishableModel), seed_data buyrug'i
apps/courses/      Course, CurriculumItem
apps/events/       Event, ScheduleItem
apps/content/      SiteSettings, Statistic, Feature, Equipment, Partner
apps/projects/     VideoStory
apps/news/         Post
apps/applications/ Application (formalardan kelgan murojaatlar)
docs/              bajarilgan ishlar bosqichma-bosqich
```

## Testlar

```bash
python manage.py test
```

## Serverga yuklash (production)

Docker Compose + Nginx + GitHub Actions — qadam-baqadam: [`docs/DEPLOY.md`](docs/DEPLOY.md).
