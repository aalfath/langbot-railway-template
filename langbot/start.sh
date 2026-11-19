#!/bin/sh
# Start LangBot on Railway.
# LangBot reads any SECTION__KEY environment variable as an override of
# data/config.yaml (for example DATABASE__USE -> database.use), so the fixed
# settings live here and the template keeps only references, secrets and the
# owner email.
set -e
cd /app

export TZ="${TZ:-UTC}"
# Listen on Railway's PORT (5300 in the template).
export API__PORT="${PORT:-5300}"
# Bots, pipelines, models, plugins and history go to the Postgres service.
export DATABASE__USE="${DATABASE__USE:-postgresql}"
# The Box sandbox needs the host Docker socket or nsjail namespaces, which
# Railway doesn't give containers. Local stdio MCP servers run commands and
# need Box too. HTTP/SSE MCP servers, skills and plugins still work.
export BOX__ENABLED="${BOX__ENABLED:-false}"
export MCP__STDIO__ENABLED="${MCP__STDIO__ENABLED:-false}"
# Webhook callback URLs shown in the UI use the service's Railway domain
# unless you set API__WEBHOOK_PREFIX yourself (for a custom domain).
if [ -z "${API__WEBHOOK_PREFIX:-}" ] && [ -n "${RAILWAY_PUBLIC_DOMAIN:-}" ]; then
  export API__WEBHOOK_PREFIX="https://${RAILWAY_PUBLIC_DOMAIN}"
fi

# Wait for Postgres so a fresh deploy doesn't crash while the database is
# still starting (Railway doesn't order service startup).
python /railway/wait-for-db.py

# Create the owner account from LANGBOT_ADMIN_EMAIL / LANGBOT_ADMIN_PASSWORD
# as soon as the API answers on loopback, so nobody else can claim the
# instance. It does nothing once an account exists.
python /railway/seed-admin.py &

exec uv run --no-sync main.py
