FROM python:3.12-slim-bookworm

ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl gnupg git build-essential pkg-config \
      libpq-dev postgresql-client \
      libjpeg62-turbo-dev libpng-dev libwebp-dev libtiff-dev \
      zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev \
      libavif-dev ffmpeg fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_20.x -o /tmp/nodesource_setup.sh \
    && bash /tmp/nodesource_setup.sh \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/* /tmp/nodesource_setup.sh

RUN pip install --no-cache-dir \
      "Django==5.0.9" \
      "psycopg[binary]==3.2.3" \
      "gunicorn==23.0.0" \
      "boto3==1.35.36" \
      "Pillow==10.4.0" \
      "pillow-avif-plugin==1.4.6" \
      "python-dotenv==1.0.1"

RUN mkdir -p /app/.browser_screenshots /app/.downloads

WORKDIR /app

EXPOSE 4173

CMD ["sleep", "infinity"]
