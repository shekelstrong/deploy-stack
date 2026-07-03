"""deploy_vercel: генерация vercel.json + next.config.js."""


VERCEL_TEMPLATES = {
    "nextjs": {
        "vercel_json": '''{
  "version": 2,
  "buildCommand": "next build",
  "framework": "nextjs",
  "regions": ["fra1"]
}
''',
        "next_config": '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**" },
    ],
  },
  // Для SPA-режима (export) раскомментируй:
  // output: "export",
  // trailingSlash: true,
  // images: { unoptimized: true },
};

module.exports = nextConfig;
''',
    },
    "vite": {
        "vercel_json": '''{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
''',
    },
    "remix": {
        "vercel_json": '''{
  "version": 2,
  "framework": "remix"
}
''',
    },
    "astro": {
        "vercel_json": '''{
  "version": 2,
  "framework": "astro"
}
''',
    },
}


async def run(name: str, framework: str, spa_mode: bool = False) -> dict:
    """Генерирует vercel.json + конфиг.

    Args:
        name: Имя проекта.
        framework: nextjs/vite/remix/astro.
        spa_mode: SPA-режим (client-side routing).

    Returns:
        Словарь с файлами.
    """
    template = VERCEL_TEMPLATES[framework]
    return {
        "name": name,
        "framework": framework,
        "spa_mode": spa_mode,
        "vercel_json": template["vercel_json"],
        "next_config": template.get("next_config"),
        "instructions": [
            "1. Скопируй vercel.json в корень",
            "2. Для Next.js скопируй next.config.js тоже",
            f"3. vercel --prod (или через GitHub: push → auto-deploy)",
            "4. Переменные окружения: Vercel Dashboard → Settings → Environment Variables",
        ],
    }
