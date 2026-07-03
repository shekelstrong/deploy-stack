---
name: deploy-stack
description: Деплой Python-сервисов, Telegram-ботов, фронтендов. VPS (Docker + GitHub Actions), Vercel, Layero. Готовые Dockerfile, docker-compose, vercel.json, GitHub Actions workflows.
---

# Deploy Stack

MCP-сервер для деплоя всего стека: Python, боты, фронты.

## Когда использовать

- Запускаешь Python-сервис / Telegram-бота на VPS
- Деплоишь Next.js / Vite на Vercel или Layero
- Настраиваешь CI/CD через GitHub Actions
- Нужен bash-скрипт для ручного/SSH-деплоя
- Хочешь единый инструмент вместо копипасты шаблонов

## 6 tools

```
сервис → deploy_python/telegram → Dockerfile + compose
       → deploy_vercel/layero → vercel.json + конфиг
       → setup_cicd → GitHub Actions workflow
       → ssh_deploy → bash-скрипт
```

## Алгоритм

### 1. deploy_python
5 фреймворков с готовыми Dockerfile:
- **fastapi** — uvicorn + healthcheck
- **aiogram** — polling/webhook
- **django** — gunicorn + collectstatic
- **flask** — gunicorn
- **raw** — минимальный Python

Все с multi-stage pip install, slim образ, healthcheck.

### 2. deploy_telegram
Полный шаблон для aiogram 3:
- Dockerfile
- docker-compose.yml (без exposed портов — webhook опционально)
- requirements.txt
- .env.example (BOT_TOKEN, ADMIN_IDS, OPENROUTER_API_KEY)

### 3. deploy_vercel
4 фреймворка: nextjs / vite / remix / astro.
- vercel.json с regions=["fra1"] (ближе к РФ)
- next.config.js (для Next.js)
- rewrites для SPA (Vite)

### 4. deploy_layero
Конфиг для RU hosting:
- vercel.json совместимый формат
- Только статика (без serverless)

### 5. setup_cicd
GitHub Actions workflow:
- appleboy/ssh-action
- Auto-deploy на push в main
- Нужны 3 секрета: VPS_HOST, VPS_USER, VPS_SSH_KEY

### 6. ssh_deploy
Bash-скрипт:
- ssh-pull + docker compose restart
- Tail logs
- Можно в cron

## Pitfalls

| Ошибка | Последствие | Как избежать |
|---|---|---|
| Секреты в коде | Утечка | Только через .env, GitHub Secrets |
| Docker без healthcheck | Не знаешь упал ли | Включён во все шаблоны |
| Layero для SSR | Не запустится | Layero только статика, SSR → Vercel |
| Без restart: unless-stopped | Падение = downtime | В compose по умолчанию |
| GitHub Actions без secrets | Auth fail | Добавь VPS_SSH_KEY |
| Прямой push в main без CI | Баги в проде | setup_cicd + branch protection |
| Запуск от root в Docker | Security risk | USER node в production |

## Матрица

| Что | VPS + Docker | Vercel | Layero |
|---|---|---|---|
| Python API | ✅ | ❌ | ❌ |
| Python бот | ✅ | ❌ | ❌ |
| Next.js SSR | ⚠️ Node | ✅ | ❌ |
| Next.js static | ✅ | ✅ | ✅ |
| Vite SPA | ❌ | ✅ | ✅ |
| Astro | ✅ | ✅ | ✅ |

## Источники

8 скиллов: python-vps-deployment, telegram-bot-docker-deploy, vps-deploy-via-github-actions, buildo-deployment-architecture, vercel-frontend-deployment, vps-deployment-topology, personal-tg-bot-deploy, layero-development.
