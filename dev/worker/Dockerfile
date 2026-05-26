FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app --home-dir /app --shell /usr/sbin/nologin app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY debug_worker.py ./debug_worker.py
COPY src ./src

RUN chown -R app:app /app

USER app

CMD ["celery", "-A", "debug_worker.celery_app", "worker", "--loglevel=info"]
