FROM python:3.12-slim-bookworm

ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NODE_MAJOR=20

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates git build-essential postgresql-client \
    && curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      "uvicorn[standard]==0.34.0" \
      "fastapi==0.115.6" \
      "psycopg[binary]==3.2.3" \
      "pydantic==2.10.4" \
      "python-jose[cryptography]==3.3.0" \
      "passlib[bcrypt]==1.7.4" \
      "httpx==0.28.1"

RUN npm install -g npm@10

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

EXPOSE 4173

CMD ["sleep", "infinity"]
