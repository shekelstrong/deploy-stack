"""deploy_telegram: полный шаблон для деплоя Telegram-бота."""


async def run(name: str, aiogram_version: str = "3.13") -> dict:
    """Генерирует Docker + compose + .env для Telegram-бота.

    Args:
        name: Имя бота.
        aiogram_version: Версия aiogram.

    Returns:
        Словарь с файлами.
    """
    return {
        "name": name,
        "dockerfile": f'''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\
    CMD python -c "import os; assert os.path.exists('/tmp/healthy')" || exit 1

CMD ["python", "bot.py"]
''',
        "compose": f'''services:
  {name}:
    build: .
    container_name: {name}
    restart: unless-stopped
    env_file: .env
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
''',
        "requirements": f"aiogram>={aiogram_version}\npydantic-settings>=2.0.0\naiohttp>=3.9.0\n",
        "env_example": '''# Telegram
BOT_TOKEN=*** from @BotFather
ADMIN_IDS=123456789

# Optional: LLM
OPENROUTER_API_KEY=sk-or-...

# Optional: Webhook (vs polling)
# WEBHOOK_DOMAIN=https://your.domain.com
# WEBHOOK_PATH=/webhook

# Database
DATABASE_URL=sqlite+aiosqlite:///bot.db
''',
        "instructions": [
            "1. Скопируй Dockerfile, docker-compose.yml, .env в корень",
            "2. Заполни .env (BOT_TOKEN обязателен)",
            f"3. VPS: cd /root/Projects/{name} && docker compose up -d --build",
            "4. Логи: docker compose logs -f",
            "5. Healthcheck: docker inspect --format='{{.State.Health.Status}}' " + name,
        ],
    }
