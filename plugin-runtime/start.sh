#!/bin/sh
# Start the LangBot Plugin Runtime.
# LANGBOT_PLUGIN_RUNTIME_CONTROL_TOKEN (32+ characters) protects the control
# WebSocket; LangBot sends the same value. GET /healthz on the control port
# answers without the token and is what Railway's health check probes.
set -e
cd /app
export TZ="${TZ:-UTC}"
exec uv run --no-sync -m langbot_plugin.cli.__init__ rt --ws-control-port "${PORT:-5400}"
