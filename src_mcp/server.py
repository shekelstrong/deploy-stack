"""Deploy Stack MCP Server."""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src_mcp.tools import deploy_python, deploy_telegram, deploy_vercel, deploy_layero, setup_cicd, ssh_deploy


app = Server("deploy-stack")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="deploy_python",
            description="Генерация Dockerfile + docker-compose для Python-сервиса (FastAPI, aiogram и т.д.) на VPS.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "framework": {"type": "string", "enum": ["fastapi", "aiogram", "django", "flask", "raw"]},
                    "port": {"type": "integer", "default": 8080},
                },
                "required": ["name", "framework"],
            },
        ),
        Tool(
            name="deploy_telegram",
            description="Полный шаблон для деплоя Telegram-бота: Dockerfile + compose + .env.example + healthcheck.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "aiogram_version": {"type": "string", "default": "3.13"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="deploy_vercel",
            description="Генерация vercel.json + next.config.js для Next.js-проекта на Vercel.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "framework": {"type": "string", "enum": ["nextjs", "vite", "remix", "astro"]},
                    "spa_mode": {"type": "boolean", "default": False},
                },
                "required": ["name", "framework"],
            },
        ),
        Tool(
            name="deploy_layero",
            description="Генерация конфига для Layero (RU hosting) — статический сайт или Vite SPA.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "build_command": {"type": "string", "default": "npm run build"},
                    "output_dir": {"type": "string", "default": "dist"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="setup_cicd",
            description="Генерация GitHub Actions workflow для автодеплоя через SSH на VPS.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "vps_host": {"type": "string"},
                    "vps_user": {"type": "string", "default": "root"},
                    "vps_path": {"type": "string"},
                    "trigger_branch": {"type": "string", "default": "main"},
                },
                "required": ["name", "vps_host"],
            },
        ),
        Tool(
            name="ssh_deploy",
            description="Генерация скрипта для SSH-деплоя без GitHub Actions (для cron/ручного).",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "vps_host": {"type": "string"},
                    "vps_user": {"type": "string", "default": "root"},
                    "vps_path": {"type": "string"},
                },
                "required": ["name", "vps_host"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    import json
    tools_map = {
        "deploy_python": deploy_python,
        "deploy_telegram": deploy_telegram,
        "deploy_vercel": deploy_vercel,
        "deploy_layero": deploy_layero,
        "setup_cicd": setup_cicd,
        "ssh_deploy": ssh_deploy,
    }
    try:
        result = await tools_map[name].run(**arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {type(e).__name__}: {e}")]


async def main():
    async with stdio_server() as (rs, ws):
        await app.run(rs, ws, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
