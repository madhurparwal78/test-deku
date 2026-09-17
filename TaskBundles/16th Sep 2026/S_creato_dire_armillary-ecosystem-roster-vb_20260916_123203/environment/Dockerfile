FROM python:3.12-slim-bookworm
ARG TARGETARCH
ARG NODE_MAJOR=20
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV APP_PUBLIC_PORT=4173
WORKDIR /app
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg git postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -; apt-get install -y --no-install-recommends nodejs; rm -rf /var/lib/apt/lists/*
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads
EXPOSE 4173
CMD ["sleep", "infinity"]
