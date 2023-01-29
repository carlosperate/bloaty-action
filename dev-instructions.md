# Dev Instructions

## Building the base Docker image

```
docker build -t "bloaty" --file Dockerfile.base .
```

```
docker run --rm bloaty --help
```

## Publish image

```
docker login ghcr.io -u <your_username>
docker images
docker tag IMAGE_ID ghcr.io/carlosperate/bloaty:VERSION
docker tag IMAGE_ID ghcr.io/carlosperate/bloaty:latest
docker push ghcr.io/carlosperate/bloaty:VERSION
docker push ghcr.io/carlosperate/bloaty:latest
```
