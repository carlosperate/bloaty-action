# Docker image with the Bloaty action environment

This docker image is derived from `ghcr.io/carlosperate/bloaty`, which
Dockerfile is also present in this repository in the
[../Dockerfile.bloaty](../Dockerfile.bloaty) path.

This image installs Python 3 and adds the `action.py` script to process the
bloaty output and other action features.

Originally the Dockerfile was build on each Action run, but pushing the image
to the GitHub Docker registry (`ghcr.io/carlosperate/bloaty-action`)
saves around 30 seconds of build time during GitHub Action workflow runs.
