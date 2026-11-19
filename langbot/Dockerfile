# LangBot core: web UI, HTTP API, webhooks and IM adapters.
# Official image, pinned by version and digest (multi-arch index).
FROM rockchin/langbot:v4.11.9@sha256:86c2333a7482bbb5980965852e0835bf1f970f8fd7aedbba29970db32022023a

COPY start.sh wait-for-db.py seed-admin.py /railway/

CMD ["sh", "/railway/start.sh"]
