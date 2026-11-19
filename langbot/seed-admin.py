"""Create LangBot's owner account on first boot.

LangBot lets the first visitor of a new instance create the owner account.
This script claims it for LANGBOT_ADMIN_EMAIL with LANGBOT_ADMIN_PASSWORD
through LangBot's own /api/v1/user/init endpoint on loopback, before Railway
routes public traffic to the deploy (that happens only after /healthz passes).
Once any account exists it does nothing, so changing the password in the UI
is safe.
"""
import json
import os
import sys
import time
import urllib.request

TAG = "[seed-admin]"
email = os.environ.get("LANGBOT_ADMIN_EMAIL", "").strip()
password = os.environ.get("LANGBOT_ADMIN_PASSWORD", "")
url = "http://127.0.0.1:%s/api/v1/user/init" % os.environ.get("API__PORT", "5300")

if not email or not password:
    print(TAG, "WARNING: LANGBOT_ADMIN_EMAIL or LANGBOT_ADMIN_PASSWORD is empty; "
          "the first visitor of the URL can create the owner account", flush=True)
    sys.exit(0)

deadline = time.time() + 900
while time.time() < deadline:
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            state = json.load(r)
    except Exception:
        time.sleep(0.5)
        continue
    if (state.get("data") or {}).get("initialized"):
        print(TAG, "owner account already exists; nothing to do", flush=True)
        sys.exit(0)
    body = json.dumps({"user": email, "password": password}).encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.load(r)
    except Exception as exc:
        print(TAG, "init request failed (%s); retrying" % exc.__class__.__name__, flush=True)
        time.sleep(2)
        continue
    if res.get("code") == 0:
        print(TAG, "created owner account", email, flush=True)
    else:
        print(TAG, "init refused: code=%s msg=%s" % (res.get("code"), res.get("msg")), flush=True)
    sys.exit(0)
print(TAG, "ERROR: LangBot API did not answer on loopback within 15 minutes", flush=True)
sys.exit(1)
