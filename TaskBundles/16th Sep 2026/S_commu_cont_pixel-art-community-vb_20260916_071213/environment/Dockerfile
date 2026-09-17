FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NODE_MAJOR=20

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates git build-essential postgresql-client \
    && curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

CMD ["sleep", "infinity"]
