"""Wait until the Postgres host in DATABASE__POSTGRESQL__URL accepts TCP."""
import os
import socket
import sys
import time
from urllib.parse import urlsplit

TAG = "[wait-for-db]"
url = os.environ.get("DATABASE__POSTGRESQL__URL", "")
if os.environ.get("DATABASE__USE", "postgresql") != "postgresql" or not url:
    sys.exit(0)

parts = urlsplit(url)
host, port = parts.hostname, parts.port or 5432
deadline = time.time() + 300
while time.time() < deadline:
    try:
        with socket.create_connection((host, port), timeout=3):
            print(TAG, "Postgres is reachable", flush=True)
            sys.exit(0)
    except OSError:
        time.sleep(2)
print(TAG, "Postgres did not answer within 5 minutes; starting anyway", flush=True)
