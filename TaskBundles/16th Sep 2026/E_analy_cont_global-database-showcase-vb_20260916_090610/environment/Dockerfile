FROM python:3.12-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254
ARG TARGETARCH
ARG NODE_MAJOR=22
ARG CA_CERT_PEM=""
ARG CHROMIUM_LIBS_A="libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0"
ARG CHROMIUM_LIBS_B="libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation"
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV APP_PUBLIC_PORT=4173 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends curl ca-certificates gnupg postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; mkdir -p /etc/apt/keyrings; curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs ${CHROMIUM_LIBS_A} ${CHROMIUM_LIBS_B}; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3" boto3==1.35.99 pyyaml==6.0.2 playwright==1.49.1
RUN set -eux; playwright install chromium
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
