FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ARG CHROMIUM_LIBS_A="libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2"
ARG CHROMIUM_LIBS_B="libdrm2 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6"
ARG CHROMIUM_LIBS_C="libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation"
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; mkdir -p /etc/apt/keyrings; curl -fsSL -o /tmp/nodesource.key https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key
RUN set -eux; gpg --batch --dearmor -o /etc/apt/keyrings/nodesource.gpg /tmp/nodesource.key; rm -f /tmp/nodesource.key
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs $CHROMIUM_LIBS_A $CHROMIUM_LIBS_B $CHROMIUM_LIBS_C; rm -rf /var/lib/apt/lists/*
RUN set -eux; node --version | grep -q "^v${NODE_MAJOR}[.]"
RUN set -eux; pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3" boto3==1.35.99 pyyaml==6.0.2 playwright==1.49.1
RUN set -eux; playwright install chromium
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
