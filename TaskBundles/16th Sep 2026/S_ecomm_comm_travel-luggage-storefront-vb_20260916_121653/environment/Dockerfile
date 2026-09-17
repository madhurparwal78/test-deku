FROM python:3.12-slim-bookworm

ARG TARGETARCH
ARG NODE_MAJOR=20
ARG http_proxy=""
ARG https_proxy=""
ARG HTTP_PROXY=""
ARG HTTPS_PROXY=""
ARG no_proxy=""
ARG NO_PROXY=""
ARG CA_CERT_PATH=""
ARG CA_CERT_PEM=""
ARG CHROME_LIBS_A="libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0"
ARG CHROME_LIBS_B="libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation"

ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONPATH=/tests
ENV http_proxy=${http_proxy} https_proxy=${https_proxy} no_proxy=${no_proxy}
ENV HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY}
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV APP_PUBLIC_PORT=4173

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg postgresql-client && rm -rf /var/lib/apt/lists/*

RUN set -eux; if [ -n "${CA_CERT_PEM}" ]; then printf '%s' "${CA_CERT_PEM}" > /usr/local/share/ca-certificates/proxy-ca.crt; fi
RUN set -eux; if [ -n "${CA_CERT_PATH}" ] && [ -f "${CA_CERT_PATH}" ]; then cp "${CA_CERT_PATH}" /usr/local/share/ca-certificates/proxy-ca.crt; fi
RUN update-ca-certificates

WORKDIR /app

RUN set -eux; curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -; rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends nodejs ${CHROME_LIBS_A} ${CHROME_LIBS_B} && rm -rf /var/lib/apt/lists/*

RUN npm install -g npm@10.9.2

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 pyyaml==6.0.2
RUN pip install --no-cache-dir "psycopg[binary]==3.2.3" boto3==1.35.99 playwright==1.49.1

RUN playwright install chromium

RUN mkdir -p /app/.browser_screenshots /app/.downloads

EXPOSE 4173
CMD ["sleep", "infinity"]
