FROM ghcr.io/carlosperate/bloaty:latest

LABEL "version"="0.2.0"
LABEL org.opencontainers.image.title="Bloaty McBloatface GitHub Action"
LABEL org.opencontainers.image.description="GitHub Action using Docker to run Bloaty McBloatface: a size profiler for binaries."
LABEL org.opencontainers.image.authors="Carlos Pereira Atencio <carlosperate@embeddedlog.com>"
LABEL org.opencontainers.image.source="https://github.com/carlosperate/bloaty-action"

# Adding locale env variables to ensure shell is UTF-8 encoded
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends locales python3 && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY action.py /home/

WORKDIR /home/

ENTRYPOINT ["python3", "/home/action.py"]
