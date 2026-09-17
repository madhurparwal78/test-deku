FROM node:20-bookworm-slim

ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    NODE_ENV=production \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git openssl postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

EXPOSE 4173

CMD ["sleep", "infinity"]
