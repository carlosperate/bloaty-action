###############################################################################
# Builder image
###############################################################################
FROM ubuntu:22.04 as bloaty-builder

# Bloaty McBloatface git tag to build
ARG BLOATY_VERSION=v1.1

# Install dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && \
    apt-get install -y git && \
    apt-get install -y --no-install-recommends build-essential cmake ninja-build && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Clone, build and install Bloaty McBloatface
RUN mkdir /git && \
    git clone https://github.com/google/bloaty.git /git/bloaty && \
    cd /git/bloaty && \
    git checkout tags/$BLOATY_VERSION && \
    git submodule update --init --recursive && \
    cmake -B build -G Ninja -S . && \
    cmake --build build && \
    cmake --build build --target install

###############################################################################
# Image to ship
###############################################################################
FROM ubuntu:22.04

# The versioning system used for this image: <bloaty_version>-<docker_img_version>
LABEL "version"="v1.1-2"
LABEL org.opencontainers.image.title="Bloaty McBloatface Docker Image"
LABEL org.opencontainers.image.description="Docker image to run Bloaty McBloatface: a size profiler for binaries."
LABEL org.opencontainers.image.authors="Carlos Pereira Atencio <carlosperate@embeddedlog.com>"
LABEL org.opencontainers.image.source="https://github.com/carlosperate/bloaty-action"

# Copy the binaries into this image
COPY --from=bloaty-builder /usr/local/bin /usr/local/bin

WORKDIR /home

ENTRYPOINT ["bloaty"]
