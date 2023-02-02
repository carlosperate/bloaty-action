# Dev Instructions

## Update GitHub Action git tag

```
git tag -fa v0 -m "Update v0 tag"
git push origin v0 --force
```


## Base Bloaty Docker image

Build image:
```
docker build -t "bloaty" --file Dockerfile.bloaty .
```

Run image:
```
docker run --rm bloaty --help
docker run --rm -v $(pwd):/home tests/test-elf-files/example-after.elf -d compileunits -n 30 -s vm
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

Build image, from the project root directory:
```
docker build -t "bloaty-action" docker-action
```

Run image:
```
docker run --rm bloaty-action --help
docker run --rm -v $(pwd):/home bloaty-action tests/test-elf-files/example-after.elf
```

Publish image:
```
docker login ghcr.io -u <your_username>
docker images
docker tag IMAGE_ID ghcr.io/carlosperate/bloaty-action:latest
docker tag IMAGE_ID ghcr.io/carlosperate/bloaty-action:VERSION
docker push ghcr.io/carlosperate/bloaty-action:latest
docker push ghcr.io/carlosperate/bloaty-action:VERSION
```
