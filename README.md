[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/langbot-1?utm_medium=integration&utm_source=button&utm_campaign=langbot)

# LangBot on Railway

One-click [LangBot](https://github.com/langbot-app/LangBot) for Railway: an open-source platform for LLM-powered bots on Telegram, Discord, Slack, Lark, DingTalk, WeCom, QQ, WeChat, LINE and more.

**Version:** LangBot `v4.11.9`, official image `rockchin/langbot:v4.11.9@sha256:86c2333a7482bbb5980965852e0835bf1f970f8fd7aedbba29970db32022023a`.

## What the template deploys

| Service | Source | What it does | Volume |
|---|---|---|---|
| **LangBot** | `langbot/` in this repo | Web UI, HTTP API, webhook callbacks and IM adapters. Public domain on port 5300, health check `/healthz`. | `/app/data` (config, instance id, Chroma knowledge-base vectors, uploads) |
| **Plugin Runtime** | `plugin-runtime/` in this repo | Installs and runs LangBot plugins. Private only: LangBot connects to its control WebSocket on port 5400 with a generated token. Health check `/healthz`. | `/app/data` (installed plugins, their dependency environments and data) |
| **Postgres** | Railway's Postgres | Bots, pipelines, models, users, plugin settings and history. LangBot runs its migrations on boot. | `/var/lib/postgresql/data` |

Both app services build from this repo's Dockerfiles, which pin the official image by version and digest and add only a small start script.

## Variables

| Service | Variable | Default | Notes |
|---|---|---|---|
| LangBot | `LANGBOT_ADMIN_EMAIL` | *(you enter it)* | Email of the owner account, created on first boot. The only prompt. |
| LangBot | `LANGBOT_ADMIN_PASSWORD` | `${{secret(24)}}` | Initial owner password. Read it in the LangBot service's Variables tab; change it in the UI after you sign in. |
| LangBot | `SYSTEM__JWT__SECRET` | `${{secret(64,"abcdef0123456789")}}` | Signs login sessions. |
| LangBot | `SYSTEM__RECOVERY_KEY` | `${{secret(16,"23456789ABCDEFGHJKLMNPQRSTUVWXYZ")}}` | Key for the "Forgot password" flow on the login page. |
| LangBot | `DATABASE__POSTGRESQL__URL` | `${{Postgres.DATABASE_URL}}` | Private-network Postgres URL. |
| LangBot | `PLUGIN__RUNTIME_WS_URL` | `ws://${{Plugin Runtime.RAILWAY_PRIVATE_DOMAIN}}:5400/control/ws` | Plugin Runtime control WebSocket. |
| LangBot | `LANGBOT_PLUGIN_RUNTIME_CONTROL_TOKEN` | `${{Plugin Runtime.LANGBOT_PLUGIN_RUNTIME_CONTROL_TOKEN}}` | Same token as the runtime. |
| LangBot | `PORT` | `5300` | |
| Plugin Runtime | `LANGBOT_PLUGIN_RUNTIME_CONTROL_TOKEN` | `${{secret(48)}}` | Protects the control WebSocket. |
| Plugin Runtime | `PORT` | `5400` | |

LangBot reads any `SECTION__KEY` environment variable as an override of its `config.yaml` (for example `SPACE__DISABLE_TELEMETRY=true`). `langbot/start.sh` sets the fixed ones: `DATABASE__USE=postgresql`, `BOX__ENABLED=false`, `MCP__STDIO__ENABLED=false`, and `API__WEBHOOK_PREFIX=https://<the service's Railway domain>` unless you set it yourself (do that when you add a custom domain).

## Left out

- **Box sandbox** (`langbot_box`, an optional upstream profile): it needs the host Docker socket or nsjail namespaces, which Railway containers don't have. Shell/file agent tools and local stdio MCP servers are therefore off. Plugins, skills, knowledge bases and HTTP/SSE MCP servers work.
- **Platform reverse-connection ports** (2280-2285) and the plugin debug port (5401): Railway exposes one HTTP port per service. Bots that use webhooks or outgoing connections (Telegram, Discord, Slack, Lark, DingTalk, WeCom, LINE and others) work.

## Updates

This template builds from this repo's `main` branch. When we bump the LangBot version here, Railway shows deployers an "update available" notice and they choose when to apply it. Read [CHANGELOG.md](CHANGELOG.md) first: breaking changes are listed at the top of each entry. LangBot migrates its database on boot.

Upstream docs: [Docker deployment](https://docs.langbot.app/en/deploy/langbot/docker), [configuration](https://docs.langbot.app/en/deploy/settings), [releases](https://github.com/langbot-app/LangBot/releases).
