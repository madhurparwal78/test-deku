FROM python:3.12-slim-bookworm

ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git build-essential libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

EXPOSE 4173

CMD ["sleep", "infinity"]
