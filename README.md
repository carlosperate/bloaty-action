# Bloaty McBloatface GitHub Action

GitHub Action to run Bloaty McBloatface: a size profiler for binaries 

```yaml
- name: Run Bloaty McBloatface on an ELF file
  uses: carlosperate/bloaty-action@v0
  with:
    bloaty-args: tests/test-elf-files/example-before.elf
```


## Using the base Docker Image to run Bloaty McBloatface locally

To diff two ELF files (from the project root directory):

```
docker run --rm -v $(pwd):/home ghcr.io/carlosperate/bloaty:latest tests/test-elf-files/example-before.elf -- tests/test-elf-files/example-after.elf
```
