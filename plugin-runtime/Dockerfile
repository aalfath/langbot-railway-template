# LangBot Plugin Runtime: runs installed plugins and serves the control
# WebSocket that LangBot connects to over Railway's private network.
# Same official image as the core, pinned by version and digest.
FROM rockchin/langbot:v4.11.9@sha256:86c2333a7482bbb5980965852e0835bf1f970f8fd7aedbba29970db32022023a

COPY start.sh /railway/

CMD ["sh", "/railway/start.sh"]
