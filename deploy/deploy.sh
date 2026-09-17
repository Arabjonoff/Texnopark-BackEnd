#!/usr/bin/env bash
# Serverda yangi versiyani ishga tushiradi. GitHub Actions SSH orqali chaqiradi, qo'lda ham ishlatsa bo'ladi:
#   bash /opt/texnopark/Texnopark-Back/deploy/deploy.sh backend
#   bash /opt/texnopark/Texnopark-Back/deploy/deploy.sh frontend
#   bash /opt/texnopark/Texnopark-Back/deploy/deploy.sh all
set -euo pipefail

ROOT=${TEXNOPARK_ROOT:-/opt/texnopark}
BRANCH=${DEPLOY_BRANCH:-main}
TARGET=${1:-all}
COMPOSE=(docker compose -f "$ROOT/Texnopark-Back/deploy/docker-compose.yml")

update_repo() {
  echo "==> $1: $BRANCH yangilanmoqda"
  git -C "$ROOT/$1" fetch --prune origin "$BRANCH"
  git -C "$ROOT/$1" reset --hard "origin/$BRANCH"
}

case "$TARGET" in
  backend)
    update_repo Texnopark-Back
    "${COMPOSE[@]}" up -d --build --wait backend
    ;;
  frontend)
    update_repo Texnopark-Front
    # Frontend build'i ishlab turgan backend'ga bog'liq
    "${COMPOSE[@]}" up -d --wait backend
    "${COMPOSE[@]}" up -d --build frontend
    ;;
  all)
    update_repo Texnopark-Back
    update_repo Texnopark-Front
    "${COMPOSE[@]}" up -d --build --wait backend
    "${COMPOSE[@]}" up -d --build frontend
    ;;
  *)
    echo "Foydalanish: $0 [backend|frontend|all]" >&2
    exit 1
    ;;
esac

# Eski (osilib qolgan) image'lar faqat shu loyihaniki tozalanadi — serverdagi boshqa loyihalarga tegilmaydi
docker image prune -f --filter label=com.docker.compose.project=texnopark >/dev/null

"${COMPOSE[@]}" ps
echo "==> Deploy tugadi: $TARGET"
