FROM python:3.12-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254
ARG TARGETARCH
ARG NODE_MAJOR=20
ARG CA_CERT_PEM=""
ARG http_proxy=""
ARG https_proxy=""
ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""
ARG no_proxy=""
ARG NO_PROXY=""
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV http_proxy=${http_proxy} https_proxy=${https_proxy} no_proxy=${no_proxy}
ENV HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY}
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV NODE_ENV=production NPM_CONFIG_UPDATE_NOTIFIER=false
ENV APP_PUBLIC_PORT=4173 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV CHROMIUM_DEPS_A="libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0"
ENV CHROMIUM_DEPS_B="libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation"
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg git build-essential postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; if [ -n "$CA_CERT_PEM" ]; then printf '%s' "$CA_CERT_PEM" > /usr/local/share/ca-certificates/proxy-ca.crt; update-ca-certificates; fi
RUN set -eux; mkdir -p /etc/apt/keyrings; curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs ${CHROMIUM_DEPS_A} ${CHROMIUM_DEPS_B}; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3" pyyaml==6.0.2 playwright==1.49.1
RUN set -eux; playwright install chromium
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
