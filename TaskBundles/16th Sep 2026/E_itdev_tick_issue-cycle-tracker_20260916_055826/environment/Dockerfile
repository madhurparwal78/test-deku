FROM python:3.12-slim
ARG TARGETARCH
ENV DEBIAN_FRONTEND=noninteractive PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git build-essential postgresql-client fonts-liberation \
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 \
    libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y --no-install-recommends nodejs && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --break-system-packages pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 "psycopg[binary]==3.2.3" boto3==1.35.99 pyyaml==6.0.2 playwright==1.49.1
RUN playwright install chromium
ENV PYTHONPATH=/tests
RUN mkdir -p /app/.browser_screenshots /app/.downloads
WORKDIR /app
