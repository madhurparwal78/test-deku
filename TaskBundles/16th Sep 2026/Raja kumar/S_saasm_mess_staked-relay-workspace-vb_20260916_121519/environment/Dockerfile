FROM mcr.microsoft.com/playwright/python:v1.49.1-noble@sha256:42e251ec3238672c931be6c3565ff279690ae072c3e22058128d0412494f6866

ARG TARGETARCH

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV APP_PUBLIC_PORT=4173

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
       | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" \
       > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      pytest==8.4.1 \
      pytest-json-ctrf==0.3.5 \
      httpx==0.28.1 \
      "psycopg[binary]==3.2.3" \
      pyyaml==6.0.2 \
      playwright==1.49.1

RUN mkdir -p /app/.browser_screenshots /app/.downloads \
    && touch /tmp/app.log

EXPOSE 4173

CMD ["sleep", "infinity"]
