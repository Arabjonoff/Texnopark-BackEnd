#!/usr/bin/env bash
# Baza (SQLite) va yuklangan rasmlarning zaxira nusxasi. Cron har kuni ishga tushiradi:
#   0 3 * * * bash /opt/texnopark/Texnopark-Back/deploy/backup.sh >> /opt/texnopark/backups/backup.log 2>&1
set -euo pipefail

ROOT=${TEXNOPARK_ROOT:-/opt/texnopark}
KEEP_DAYS=${BACKUP_KEEP_DAYS:-14}
DEST="$ROOT/backups"
STAMP=$(date +%F_%H%M)
COMPOSE=(docker compose -f "$ROOT/Texnopark-Back/deploy/docker-compose.yml")

mkdir -p "$DEST"

# Ishlab turgan bazadan to'g'ri nusxa olish uchun SQLite backup API (oddiy fayl nusxasi yozish paytida buzilishi mumkin)
"${COMPOSE[@]}" exec -T backend python -c "
import sqlite3
src = sqlite3.connect('/app/data/db.sqlite3')
dst = sqlite3.connect('/app/data/backup.sqlite3')
src.backup(dst)
dst.close(); src.close()
"

tar czf "$DEST/texnopark-$STAMP.tar.gz" -C "$ROOT/data" db/backup.sqlite3 media
rm -f "$ROOT/data/db/backup.sqlite3"

find "$DEST" -name 'texnopark-*.tar.gz' -mtime +"$KEEP_DAYS" -delete
echo "$(date '+%F %T') backup: $DEST/texnopark-$STAMP.tar.gz ($(du -h "$DEST/texnopark-$STAMP.tar.gz" | cut -f1))"
