FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ARG DEBIAN_FRONTEND=noninteractive
ARG PROXY_CA_PEM=""
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV NO_PROXY=localhost,127.0.0.1,::1,main,postgres,mailpit no_proxy=localhost,127.0.0.1,::1,main,postgres,mailpit
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV GIT_SSL_CAINFO=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV APP_PUBLIC_PORT=4173 PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
WORKDIR /app
RUN set -eux; if [ -n "$PROXY_CA_PEM" ]; then echo "$PROXY_CA_PEM" > /usr/local/share/ca-certificates/proxy-mitm.crt; update-ca-certificates; fi
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl git gnupg openssl libpq5 postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; mkdir -p /etc/apt/keyrings; curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs; rm -rf /var/lib/apt/lists/*
RUN set -eux; apt-get install -y --no-install-recommends libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2; rm -rf /var/lib/apt/lists/*
RUN set -eux; apt-get install -y --no-install-recommends libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2; rm -rf /var/lib/apt/lists/*
RUN set -eux; apt-get install -y --no-install-recommends libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3"
RUN set -eux; pip install --no-cache-dir pyyaml==6.0.2 boto3==1.35.99 playwright==1.49.1
RUN set -eux; playwright install chromium
RUN set -eux; python --version; pip --version; node --version; npm --version; pg_isready --version
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
