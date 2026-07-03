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
    path = vps_path or f"/root/Projects/{name}"

    script = (
        "#!/bin/bash\n"
        "# SSH-деплой для " + name + "\n"
        "# Использование: bash deploy.sh\n\n"
        "set -e\n\n"
        "VPS_HOST=\"" + vps_host + "\"\n"
        "VPS_USER=\"" + vps_user + "\"\n"
        "VPS_PATH=\"" + path + "\"\n"
        'SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_rsa}"\n\n'
        'echo "==> Deploying ' + name + ' to $VPS_HOST:$VPS_PATH"\n\n'
        'ssh -i "$SSH_KEY" "$VPS_USER@$VPS_HOST" << EOF\n'
        "    set -e\n"
        '    cd "$VPS_PATH"\n'
        '    echo "==> Pulling latest code"\n'
        "    git pull origin main\n"
        '    echo "==> Rebuilding and restarting"\n'
        "    docker compose up -d --build\n"
        '    echo "==> Tailing logs"\n'
        "    docker compose logs --tail=10\n"
        "EOF\n\n"
        'echo "==> Deploy complete: ' + name + '"\n'
    )

    return {
        "script_name": "deploy.sh",
        "script_content": script,
        "instructions": [
            "1. Сохрани как deploy.sh в корне проекта",
            "2. chmod +x deploy.sh",
            "3. Настрой SSH key: ssh-copy-id " + vps_user + "@" + vps_host,
            "4. Запуск: ./deploy.sh",
            "5. Или через cron: crontab -e → 0 * * * * cd /path && ./deploy.sh",
        ],
    }
