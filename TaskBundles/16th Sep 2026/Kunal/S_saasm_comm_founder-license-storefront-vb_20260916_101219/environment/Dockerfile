FROM python:3.12-slim-bookworm

ARG TARGETARCH
ARG NODE_MAJOR=20

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN set -eux; apt-get update && apt-get install -y --no-install-recommends ca-certificates curl gnupg postgresql-client && rm -rf /var/lib/apt/lists/*

RUN set -eux; curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x -o /tmp/nodesource_setup.sh && bash /tmp/nodesource_setup.sh && rm -f /tmp/nodesource_setup.sh

RUN set -eux; apt-get install -y --no-install-recommends nodejs && rm -rf /var/lib/apt/lists/* && node --version && npm --version

WORKDIR /app

RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads

EXPOSE 4173

CMD ["sleep", "infinity"]
