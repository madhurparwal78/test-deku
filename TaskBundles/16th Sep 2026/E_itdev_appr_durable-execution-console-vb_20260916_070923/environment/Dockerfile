FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ARG CA_CERT_PATH=""
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
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV NODE_ENV=production APP_PUBLIC_PORT=4173
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg git postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; if [ -n "$CA_CERT_PEM" ]; then printf '%s' "$CA_CERT_PEM" > /usr/local/share/ca-certificates/proxy-ca.crt; update-ca-certificates; fi
RUN set -eux; mkdir -p /etc/apt/keyrings; curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs; rm -rf /var/lib/apt/lists/*
RUN set -eux; pip install --no-cache-dir "fastapi==0.115.6" "uvicorn[standard]==0.34.0" "psycopg[binary]==3.2.3" "pydantic==2.10.4" "python-jose[cryptography]==3.3.0" "httpx==0.28.1"
RUN set -eux; npm install -g --no-fund --no-audit vite@6.0.7
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
