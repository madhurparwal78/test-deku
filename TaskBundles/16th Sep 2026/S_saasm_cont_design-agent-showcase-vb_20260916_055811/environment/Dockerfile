FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ARG CA_CERT_PEM=""
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV APP_PUBLIC_PORT=4173
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; if [ -n "${CA_CERT_PEM}" ]; then printf '%s' "${CA_CERT_PEM}" > /usr/local/share/ca-certificates/proxy-ca.crt; update-ca-certificates; fi
RUN set -eux; curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -; apt-get install -y --no-install-recommends nodejs; rm -rf /var/lib/apt/lists/*
RUN set -eux; npm install -g npm@10.9.2
RUN set -eux; pip install --no-cache-dir flask==3.1.0 gunicorn==23.0.0 "psycopg[binary]==3.2.3" boto3==1.35.99
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
