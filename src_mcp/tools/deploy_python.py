"""deploy_python: генерация Dockerfile + compose для Python-сервиса."""


DOCKERFILE_TEMPLATES = {
    "fastapi": '''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:{port}/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
''',
    "aiogram": '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\
    CMD python -c "import os; assert os.path.exists('/tmp/healthy')" || exit 1

CMD ["python", "bot.py"]
''',
    "django": '''FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:{port}/ || exit 1

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:{port}"]
''',
    "flask": '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:{port}/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "app:app"]
''',
    "raw": '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
''',
}


async def run(name: str, framework: str, port: int = 8080) -> dict:
    """Генерирует Dockerfile + compose.

    Args:
        name: Имя сервиса.
        framework: fastapi/aiogram/django/flask/raw.
        port: Порт.

    Returns:
        Словарь с Dockerfile, compose, requirements_template.
    """
    dockerfile = DOCKERFILE_TEMPLATES[framework].format(port=port)
    compose = COMPOSE_TEMPLATE.format(name=name, port=port)
    req = REQUIREMENTS_BY_FRAMEWORK[framework]

    return {
        "name": name,
        "framework": framework,
        "port": port,
        "dockerfile": dockerfile,
        "compose": compose,
        "requirements_example": req,
        "instructions": [
            f"1. Скопируй Dockerfile и docker-compose.yml в корень проекта",
            f"2. Создай requirements.txt по шаблону",
            f"3. Создай .env с переменными окружения",
            f"4. На VPS: cd /root/Projects/{name} && git pull && docker compose up -d --build",
        ],
    }


COMPOSE_TEMPLATE = '''services:
  {name}:
    build: .
    container_name: {name}
    restart: unless-stopped
    env_file: .env
    ports:
      - "{port}:{port}"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  # Опционально: postgres
  # postgres:
  #   image: postgres:16-alpine
  #   restart: unless-stopped
  #   environment:
  #     POSTGRES_DB: {name}
  #     POSTGRES_USER: postgres
  #     POSTGRES_PASSWORD: changeme
  #   volumes:
  #     - pgdata:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

# volumes:
#   pgdata:
'''


REQUIREMENTS_BY_FRAMEWORK = {
    "fastapi": "fastapi==0.115.0\nuvicorn[standard]==0.32.0\npydantic==2.9.0\n",
    "aiogram": "aiogram>=3.13.0\npydantic-settings>=2.0.0\naiohttp>=3.9.0\n",
    "django": "django>=5.1\ngunicorn>=23.0\npsycopg2-binary>=2.9\n",
    "flask": "flask>=3.0\ngunicorn>=23.0\n",
    "raw": "requests>=2.32.0\n",
}
