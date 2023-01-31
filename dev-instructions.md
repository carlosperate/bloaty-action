# Dev Instructions

## Base Bloaty Docker image

Build image:
```
docker build -t "bloaty" --file Dockerfile.bloaty .
```

Run image:
```
docker run --rm bloaty --help
```

Publish image:
```
docker login ghcr.io -u <your_username>
docker images
docker tag IMAGE_ID ghcr.io/carlosperate/bloaty:latest
docker tag IMAGE_ID ghcr.io/carlosperate/bloaty:VERSION
docker push ghcr.io/carlosperate/bloaty:latest
docker push ghcr.io/carlosperate/bloaty:VERSION
```

### Git tag for the bloaty image

```
git tag -a docker_bloaty_v<version> -m "v<version> release of the bloaty Docker image"
git push origin --tags
```

## Action Docker image

Build image:
```
docker build -t "bloaty-action" .
```

Run image:
```
docker run --rm bloaty-action --help
```

## Update GitHub Action git tag

```
git tag -fa v0 -m "Update v0 tag"
git push origin v0 --force
```
