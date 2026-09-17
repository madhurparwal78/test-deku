FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV APP_PUBLIC_PORT=4173 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV CHROME_LIBS_A="libglib2.0-0 libdbus-1-3 libx11-6 libxext6 libnss3 libnspr4"
ENV CHROME_LIBS_B="libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0"
ENV CHROME_LIBS_C="libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1"
ENV CHROME_LIBS_D="libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0"
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg git build-essential postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; mkdir -p /etc/apt/keyrings
RUN set -eux; curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs $CHROME_LIBS_A $CHROME_LIBS_B $CHROME_LIBS_C $CHROME_LIBS_D; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3" pyyaml==6.0.2
RUN set -eux; pip install --no-cache-dir playwright==1.49.1
RUN set -eux; playwright install chromium
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
