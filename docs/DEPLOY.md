# Serverga yuklash va CI/CD qo'llanmasi

## Umumiy sxema

```
GitHub (push main)
   │
   ├── GitHub Actions: test / lint / build  ──✗──> deploy to'xtaydi
   │                          │ ✓
   │                          ▼
   └── SSH ──> Server: deploy/deploy.sh ──> git pull + docker compose up --build

Server (Ubuntu VPS)
   Nginx :80/:443 (HTTPS, certbot)
     ├── /            -> Next.js  (konteyner, 127.0.0.1:3010)
     ├── /admin, /api -> Django   (konteyner, 127.0.0.1:8010)
     └── /static, /media -> /opt/texnopark/data (diskdan)
```

- **CI** (har push va PR'da): backend — testlar, migratsiya tekshiruvi; frontend — lint, TypeScript, build.
- **CD** (faqat `main` branch'ga push): testlar o'tsa, GitHub serverga SSH orqali kirib `deploy.sh` ni ishga tushiradi.
- Baza (SQLite), yuklangan rasmlar va static fayllar `/opt/texnopark/data` da — deploy'lar orasida o'chmaydi.

---

## 1. Kerakli narsalar

| Nima | Izoh |
| --- | --- |
| VPS server | Ubuntu 22.04/24.04, kamida **2 GB RAM** (Next.js build uchun), 20 GB disk |
| Domen | masalan `yoshlar-texnoparki.uz`, A-yozuvi server IP'siga yo'naltirilgan |
| GitHub akkaunt | 2 ta repo: `Texnopark-Back` va `Texnopark-Front` (private bo'lishi mumkin) |

## 2. Kodni GitHub'ga yuklash (kompyuteringizda)

GitHub'da ikkita **bo'sh** repo yarating (README qo'shmasdan), keyin:

```bash
# Backend
cd Yoshlar-Texnopark/Texnopark-Back
git add .
git commit -m "Backend: API, admin, deploy"
git branch -M main
git remote add origin git@github.com:<USERNAME>/Texnopark-Back.git
git push -u origin main

# Frontend (git repo — andijon-yoshlar-texnoparki papkasi)
cd ../Texnopark-Front/andijon-yoshlar-texnoparki
git add .
git commit -m "Frontend: API integratsiya, deploy"
git branch -M main          # hozirgi branch nomi master — main ga o'zgartiriladi
git remote add origin git@github.com:<USERNAME>/Texnopark-Front.git
git push -u origin main
```

> `.env`, `db.sqlite3`, `media/`, `node_modules` git'ga tushmaydi (`.gitignore`).
> Birinchi push'da deploy job xato beradi — server hali sozlanmagan. 3–5-qadamlardan keyin qayta ishga tushiring.

## 3. Serverni tayyorlash (bir marta)

Serverga SSH orqali kiring va:

```bash
# Docker + Nginx + certbot
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sudo sh
sudo apt install -y nginx certbot python3-certbot-nginx git

# Deploy uchun alohida foydalanuvchi
sudo adduser --disabled-password --gecos "" deploy
sudo usermod -aG docker deploy

# Loyiha papkalari (1000 — konteyner ichidagi foydalanuvchi ID'si)
sudo mkdir -p /opt/texnopark/data/{db,media,static}
sudo chown -R deploy:deploy /opt/texnopark
sudo chown -R 1000:1000 /opt/texnopark/data

# Firewall
sudo ufw allow OpenSSH && sudo ufw allow 'Nginx Full' && sudo ufw enable
```

Agar server RAM'i 2 GB dan kam bo'lsa, swap qo'shing (aks holda frontend build to'xtab qoladi):

```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 4. Repolarni serverga klonlash

Private repo bo'lsa, server GitHub'dan o'qiy olishi uchun **deploy key** kerak:

```bash
sudo -iu deploy
ssh-keygen -t ed25519 -C "texnopark-server" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
```

Chiqqan kalitni **ikkala** repoga qo'shing: GitHub → repo → Settings → Deploy keys → Add (faqat o'qish).
GitHub bitta kalitni faqat bitta repoga qo'shishga ruxsat beradi — ikkinchi repo uchun `~/.ssh/config` bilan alohida kalit ishlating yoki kalitni GitHub akkauntingizning SSH keys bo'limiga qo'shing.

```bash
cd /opt/texnopark
git clone git@github.com:<USERNAME>/Texnopark-Back.git
git clone git@github.com:<USERNAME>/Texnopark-Front.git

cp Texnopark-Back/deploy/.env.example Texnopark-Back/deploy/.env
nano Texnopark-Back/deploy/.env     # DJANGO_SECRET_KEY va domenni to'ldiring
```

## 5. Birinchi ishga tushirish

```bash
bash /opt/texnopark/Texnopark-Back/deploy/deploy.sh all

# Bazaga boshlang'ich kontent va admin foydalanuvchi
cd /opt/texnopark/Texnopark-Back
docker compose -f deploy/docker-compose.yml exec backend python manage.py seed_data
docker compose -f deploy/docker-compose.yml exec backend python manage.py createsuperuser

# Kontent yuklangandan keyin frontend'ni qayta build qilish (sahifalar to'la ma'lumot bilan tayyorlanadi)
bash deploy/deploy.sh frontend
```

Nginx:

```bash
sudo cp /opt/texnopark/Texnopark-Back/deploy/nginx/texnopark.conf /etc/nginx/sites-available/texnopark
sudo nano /etc/nginx/sites-available/texnopark        # yoshlar-texnoparki.uz -> o'z domeningiz
sudo ln -s /etc/nginx/sites-available/texnopark /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# Bepul HTTPS sertifikat (avtomatik yangilanadi)
sudo certbot --nginx -d yoshlar-texnoparki.uz -d www.yoshlar-texnoparki.uz --redirect
```

Tekshirish: `https://yoshlar-texnoparki.uz` — sayt, `https://yoshlar-texnoparki.uz/admin/` — admin panel.

## 6. GitHub Actions'ni ulash (CD)

GitHub Actions serverga kirishi uchun alohida SSH kalit (kompyuteringizda yoki serverda):

```bash
ssh-keygen -t ed25519 -C "github-actions" -f gha_key -N ""
# Ochiq kalitni serverdagi deploy foydalanuvchisiga qo'shing:
cat gha_key.pub | ssh <server> "sudo -u deploy tee -a /home/deploy/.ssh/authorized_keys"
```

**Ikkala** repoda: Settings → Secrets and variables → Actions → New repository secret:

| Secret | Qiymat |
| --- | --- |
| `SSH_HOST` | server IP yoki domen |
| `SSH_USER` | `deploy` |
| `SSH_KEY` | `gha_key` faylining **to'liq** matni (yopiq kalit) |
| `SSH_PORT` | ixtiyoriy, standart 22 |

Workflow'lar `production` environment'dan foydalanadi — Settings → Environments'da u avtomatik yaratiladi. Xohlasangiz u yerda "Required reviewers" yoqib, har deploy'ni qo'lda tasdiqlashingiz mumkin.

Endi `main` ga har push: testlar → o'tsa avtomatik deploy. Natijani repo → **Actions** bo'limida ko'rasiz. Qo'lda ishga tushirish: Actions → workflow → **Run workflow**.

## Kundalik ishlar

```bash
cd /opt/texnopark/Texnopark-Back
docker compose -f deploy/docker-compose.yml ps                 # holat
docker compose -f deploy/docker-compose.yml logs -f backend    # loglar
docker compose -f deploy/docker-compose.yml logs -f frontend
docker compose -f deploy/docker-compose.yml restart frontend
```

**Zaxira nusxa (backup)** — bazani va rasmlarni muntazam saqlang, masalan har kuni cron orqali:

```bash
# crontab -e  (deploy foydalanuvchisi)
0 3 * * * tar czf /opt/texnopark/backup-$(date +\%F).tar.gz -C /opt/texnopark data/db data/media && find /opt/texnopark -name 'backup-*.tar.gz' -mtime +14 -delete
```

Backup'larni serverdan tashqariga ham (boshqa disk, bulut) ko'chirib turing.

## Muammolar

| Belgi | Sabab va yechim |
| --- | --- |
| Deploy'da `Permission denied (publickey)` | `SSH_KEY` secret noto'g'ri yoki ochiq kalit `authorized_keys` ga qo'shilmagan |
| `git fetch` xatosi | Serverdagi deploy key repoga qo'shilmagan (4-qadam) |
| Frontend build `Killed` | RAM yetmayapti — swap qo'shing (3-qadam) |
| Admin panel CSS'siz | Nginx `/static/` yo'li yoki `data/static` ruxsatlari (`chown 1000:1000`) |
| Admin'ga kirishda `CSRF verification failed` | `deploy/.env` dagi `DJANGO_CSRF_TRUSTED_ORIGINS` da `https://domen` yo'q |
| `Bad Request (400)` | `DJANGO_ALLOWED_HOSTS` da domen yo'q |
| Rasmlar ochilmaydi | `PUBLIC_BASE_URL` noto'g'ri yoki `data/media` ruxsatlari |
