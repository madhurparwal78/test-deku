FROM python:3.12-slim-bookworm

ARG TARGETARCH
ARG NODE_MAJOR=20
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN set -eux; apt-get update; apt-get install -y --no-install-recommends ca-certificates curl gnupg postgresql-client; rm -rf /var/lib/apt/lists/*
RUN set -eux; install -m 0755 -d /etc/apt/keyrings
RUN set -eux; curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key -o /tmp/node.key
RUN set -eux; gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg /tmp/node.key; rm -f /tmp/node.key
RUN set -eux; echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
RUN set -eux; apt-get update; apt-get install -y --no-install-recommends nodejs; apt-get purge -y gnupg; apt-get autoremove -y; rm -rf /var/lib/apt/lists/*
RUN set -eux; mkdir -p /app/.browser_screenshots /app/.downloads

EXPOSE 4173

CMD ["sleep", "infinity"]
