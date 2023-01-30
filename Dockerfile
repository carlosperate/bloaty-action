FROM ghcr.io/carlosperate/bloaty:latest

LABEL "version"="0.1.0"
LABEL org.opencontainers.image.title="Bloaty McBloatface GitHub Action"
LABEL org.opencontainers.image.description="GitHub Action using Docker to run Bloaty McBloatface: a size profiler for binaries."
LABEL org.opencontainers.image.authors="Carlos Pereira Atencio <carlosperate@embeddedlog.com>"
LABEL org.opencontainers.image.source="https://github.com/carlosperate/bloaty-action"

ENTRYPOINT ["bloaty"]
