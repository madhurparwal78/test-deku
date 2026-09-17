FROM node:20.18.1-bookworm-slim

ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    NPM_CONFIG_UPDATE_NOTIFIER=false \
    NPM_CONFIG_FUND=false

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates git build-essential python3 pkg-config postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g npm@10

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

EXPOSE 4173

CMD ["sleep", "infinity"]
