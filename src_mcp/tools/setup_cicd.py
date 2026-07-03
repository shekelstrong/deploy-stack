"""setup_cicd: генерация GitHub Actions workflow."""


async def run(name: str, vps_host: str, vps_user: str = "root", vps_path: str = None, trigger_branch: str = "main") -> dict:
    """Генерирует GitHub Actions workflow.

    Args:
        name: Имя проекта.
        vps_host: IP или hostname.
        vps_user: SSH user.
        vps_path: Путь на VPS.
        trigger_branch: На какой branch реагировать.

    Returns:
        Словарь с workflow + инструкцией.
    """
    vps_path = vps_path or f"/root/Projects/{name}"

    workflow = f'''name: Deploy {name}

on:
  push:
    branches: [{trigger_branch}]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{{{ secrets.VPS_HOST }}}}
          username: ${{{{ secrets.VPS_USER }}}}
          key: ${{{{ secrets.VPS_SSH_KEY }}}}
          script: |
            cd {vps_path}
            git pull origin {trigger_branch}
            docker compose up -d --build
            docker compose logs --tail=20
'''

    setup_script = f'''#!/bin/bash
# Одноразовая настройка VPS для деплоя {name}
set -e
apt update
apt install -y docker.io docker-compose-v2 git
mkdir -p /root/Projects/{name}
cd /root/Projects/{name}
git clone git@github.com:shekelstrong/{name}.git .
cp .env.example .env
echo "⚠️  Заполни .env: nano .env"
'''

    return {
        "workflow_path": ".github/workflows/deploy.yml",
        "workflow_content": workflow,
        "vps_setup_script": setup_script,
        "github_secrets": ["VPS_HOST", "VPS_USER", "VPS_SSH_KEY"],
        "instructions": [
            f"1. Создай в GitHub: Settings → Secrets → {vps_host}/ssh-key/username",
            "2. Положи workflow в .github/workflows/deploy.yml",
            f"3. На VPS запусти setup-скрипт (один раз)",
            f"4. Заполни .env на VPS",
            f"5. Push в {trigger_branch} → автодеплой",
        ],
    }
