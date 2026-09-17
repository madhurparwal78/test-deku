FROM python:3.12-slim-bookworm
ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV APP_PUBLIC_PORT=4173
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir Django==5.1.4 gunicorn==22.0.0 whitenoise==6.8.2 "psycopg[binary]==3.2.3"
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
