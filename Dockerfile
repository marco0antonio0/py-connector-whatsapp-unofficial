FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    NON_INTERACTIVE=1 \
    BOT_API_PORT=3000 \
    CONFIG_FILE=/app/state/config.json \
    EULA_FILE=/app/state/eula.txt

WORKDIR /app

# Dependências mínimas para Chromium/Selenium
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/state

EXPOSE 3000

CMD ["python3", "main.py"]
