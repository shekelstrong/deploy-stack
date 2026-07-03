"""ssh_deploy: генерация скрипта для ручного/SSH деплоя."""


async def run(name: str, vps_host: str, vps_user: str = "root", vps_path: str = None) -> dict:
    """Генерирует bash-скрипт для SSH-деплоя.

    Args:
        name: Имя проекта.
        vps_host: IP.
        vps_user: SSH user.
        vps_path: Путь на VPS.

    Returns:
        Словарь с bash-скриптом.
    """
    vps_path = vps_path or f"/root/Projects/{name}"

    bash_script = f'''#!/bin/bash
# SSH-деплой для {name}
# Использование: bash deploy.sh

set -e

VPS_HOST="{vps_host}"
VPS_USER="{vps_user}"
VPS_PATH="{vps_path}"
SSH_KEY="${{SSH_KEY:-$HOME/.ssh/id_rsa}"

echo "==> Deploying {name} to $VPS_HOST:$VPS_PATH"

ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" << EOF
    set -e
    cd "$VPS_PATH"
    echo "==> Pulling latest code"
    git pull origin main
    echo "==> Rebuilding and restarting"
    docker compose up -d --build
    echo "==> Tailing logs"
    docker compose logs --tail=10
EOF

echo "==> Deploy complete: {name}"
'''

    return {
        "script_name": "deploy.sh",
        "script_content": bash_script,
        "instructions": [
            "1. Сохрани как deploy.sh в корне проекта",
            "2. chmod +x deploy.sh",
            "3. Настрой SSH key: ssh-copy-id " + vps_user + "@" + vps_host,
            "4. Запуск: ./deploy.sh",
            "5. Или через cron: crontab -e → 0 * * * * cd /path && ./deploy.sh",
        ],
    }
