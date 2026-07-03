# deploy-stack

> MCP-сервер для деплоя Python-сервисов, Telegram-ботов, фронтендов на VPS (Docker + GitHub Actions), Vercel, Layero.

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-compatible-purple.svg)](https://modelcontextprotocol.io)

## 🎯 Что это

MCP-сервер с 6 инструментами для деплоя:

- 🐍 **deploy_python** — Dockerfile + compose (FastAPI/aiogram/Django/Flask)
- 🤖 **deploy_telegram** — полный шаблон для Telegram-бота
- ▲ **deploy_vercel** — vercel.json + next.config.js
- 🇷🇺 **deploy_layero** — конфиг для Layero (RU hosting)
- 🔄 **setup_cicd** — GitHub Actions workflow
- 🔐 **ssh_deploy** — bash-скрипт для ручного деплоя

## 📦 Установка

```bash
git clone https://github.com/shekelstrong/deploy-stack.git
cd deploy-stack
pip install -r requirements.txt
```

## 🛠 MCP Tools

### deploy_python
```python
result = await deploy_python.run("my-api", "fastapi", port=8080)
# → {dockerfile, compose, requirements_example, instructions}
```

5 фреймворков: fastapi / aiogram / django / flask / raw.

### deploy_telegram
```python
result = await deploy_telegram.run("my-bot")
# → {dockerfile, compose, requirements, env_example, instructions}
```

Полный набор для aiogram 3 бота.

### deploy_vercel
```python
result = await deploy_vercel.run("my-site", "nextjs")
# → {vercel_json, next_config, instructions}
```

4 фреймворка: nextjs / vite / remix / astro.

### deploy_layero
```python
result = await deploy_layero.run("my-site", "npm run build", "dist")
# → {vercel_compat, instructions, warnings}
```

### setup_cicd
```python
result = await setup_cicd.run("my-bot", "108.165.164.85", "root", "/root/Projects/my-bot")
# → {workflow_content, github_secrets, vps_setup_script}
```

GitHub Actions через appleboy/ssh-action.

### ssh_deploy
```python
result = await ssh_deploy.run("my-bot", "108.165.164.85")
# → {script_content, instructions}
```

Bash-скрипт для cron / ручного деплоя.

## 📁 Структура

```
deploy-stack/
├── README.md
├── LICENSE
├── SKILL.md
├── requirements.txt
├── src_mcp/
│   ├── server.py
│   └── tools/
│       ├── deploy_python.py
│       ├── deploy_telegram.py
│       ├── deploy_vercel.py
│       ├── deploy_layero.py
│       ├── setup_cicd.py
│       └── ssh_deploy.py
└── .github/workflows/ci.yml
```

## 🗺 Матрица "что куда"

| Что | VPS + Docker | Vercel | Layero |
|---|---|---|---|
| Python API (FastAPI) | ✅ | ❌ | ❌ |
| Python бот (aiogram) | ✅ | ❌ | ❌ |
| Next.js (SSR) | ⚠️ Node | ✅ | ❌ |
| Next.js (static export) | ✅ | ✅ | ✅ |
| Vite SPA | ❌ | ✅ | ✅ |
| Astro static | ✅ | ✅ | ✅ |

## 📄 License

MIT © Vasiliy Nedopekin (shekelstrong)
