FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Root bo'lmagan foydalanuvchi; baza, media va static volume papkalari unga tegishli
RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/data /app/media /app/staticfiles \
    && chown -R app:app /app \
    && chmod +x /app/docker/entrypoint.sh
USER app

ENV SQLITE_PATH=/app/data/db.sqlite3 \
    MEDIA_ROOT=/app/media \
    DJANGO_DEBUG=False

EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-"]
