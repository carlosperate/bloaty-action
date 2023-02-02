# Bloaty McBloatface Docker Image

This directory contains the Dockerfile used to generate the
`ghcr.io/carlosperate/bloaty` Docker image.

This image only contains the `bloaty` application and can be used in your
own environment or applications.

For example, from this repository root directory you can run bloaty with:

```bash
docker run --rm -v $(pwd):/home ghcr.io/carlosperate/bloaty:latest test-elf-files/example-before.elf -d compileunits,symbols -s vm
```
