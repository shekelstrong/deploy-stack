"""deploy_layero: генерация конфига для Layero (RU hosting)."""


async def run(name: str, build_command: str = "npm run build", output_dir: str = "dist") -> dict:
    """Генерирует конфиг для Layero.

    Args:
        name: Имя проекта.
        build_command: Команда сборки.
        output_dir: Папка после сборки.

    Returns:
        Словарь с инструкцией.
    """
    return {
        "name": name,
        "build_command": build_command,
        "output_dir": output_dir,
        "vercel_compat": '''{
  "version": 2,
  "buildCommand": "''' + build_command + '''",
  "outputDirectory": "''' + output_dir + '''"
}
''',
        "instructions": [
            "1. Собери проект локально: " + build_command,
            "2. Убедись что папка " + output_dir + " содержит index.html",
            "3. Push в GitHub: git push",
            "4. Layero → подключи репо → auto-deploy",
            "5. Домен: настрой в Layero dashboard",
        ],
        "warnings": [
            "Layero не поддерживает serverless functions (только статика)",
            "Для Next.js с SSR → используй Vercel или VPS",
            "SPA-режим (Vite) → используй BrowserRouter + fallback на /index.html",
        ],
    }
