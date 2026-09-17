FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ARG BASE_PKGS="ca-certificates curl gnupg postgresql-client"
ARG CHROMIUM_LIBS_A="libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2"
ARG CHROMIUM_LIBS_B="libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2"
ARG CHROMIUM_LIBS_C="libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation"
ARG http_proxy=""
ARG https_proxy=""
ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""
ARG no_proxy=""
ARG NO_PROXY=""
ARG CA_CERT_PEM=""
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV http_proxy=$http_proxy https_proxy=$https_proxy no_proxy=$no_proxy
ENV HTTP_PROXY=$HTTP_PROXY HTTPS_PROXY=$HTTPS_PROXY NO_PROXY=$NO_PROXY
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV APP_PUBLIC_PORT=4173 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends $BASE_PKGS $CHROMIUM_LIBS_A $CHROMIUM_LIBS_B $CHROMIUM_LIBS_C; rm -rf /var/lib/apt/lists/*
RUN set -eux; if [ -n "$CA_CERT_PEM" ]; then printf '%s' "$CA_CERT_PEM" > /usr/local/share/ca-certificates/proxy.crt; update-ca-certificates; fi
RUN set -eux; curl -fsSL https://deb.nodesource.com/setup_$NODE_MAJOR.x -o /tmp/n; bash /tmp/n; apt-get install -y --no-install-recommends nodejs; rm -f /tmp/n; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3" pyyaml==6.0.2 playwright==1.49.1
RUN set -eux; playwright install chromium
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
