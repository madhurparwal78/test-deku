FROM python:3.12-slim-bookworm

ARG TARGETARCH
ARG CHROMIUM_LIBS_A="libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0"
ARG CHROMIUM_LIBS_B="libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 fonts-liberation"

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NODE_MAJOR=20
ENV PYTHONPATH=/tests

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git build-essential postgresql-client && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
RUN apt-get update && apt-get install -y --no-install-recommends nodejs ${CHROMIUM_LIBS_A} ${CHROMIUM_LIBS_B} && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1
RUN pip install --no-cache-dir "psycopg[binary]==3.2.3" boto3==1.35.99 pyyaml==6.0.2
RUN pip install --no-cache-dir playwright==1.49.1

RUN playwright install chromium

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

EXPOSE 4173

CMD ["sleep", "infinity"]
