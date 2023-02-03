# Bloaty McBloatface GitHub Action

GitHub Action to run Google's Bloaty McBloatface - a size profiler for
binaries: https://github.com/google/bloaty/

```yaml
- name: Run Bloaty McBloatface on an ELF file
  uses: carlosperate/bloaty-action@v1
  with:
    bloaty-args: <path_to_your_file_and_any_other_flags>
```

- 🧑‍💻 Additional examples, including PR comments, can be found in the
  "[Additional Action Examples](#additional-action-examples)" section.
- 🐳 A `bloaty` Docker image (`ghcr.io/carlosperate/bloaty`) is also
  provided, more info in the
  "[Using the Docker Image to run Bloaty directly](#using-the-docker-image-to-run-bloaty-directly)" section.


## Action Inputs/Outputs

Inputs:
- `bloaty-args`: **(Required)** All arguments to pass to Bloaty McBloatface.
- `output-to-summary`: *(Optional)* Add the bloaty output to the GitHub Actions
  Job Summary.

Outputs:
- `bloaty-output`: The output from Bloaty McBloatface
- `bloaty-output-encoded`: The bloaty output in a string with escaped characters (so you'll get things like `\n`). It can be easier to pass this to other action steps.


## Using the Docker image to run Bloaty directly

This repository contains two Dockerfiles and two Docker images are hosted in
the [GitHub Docker Container registry](https://github.blog/2020-09-01-introducing-github-container-registry/).

The `ghcr.io/carlosperate/bloaty` Docker image contains the bloaty application
on its own, and can be used used to run `bloaty` directly in your own
environment or applications.

For example, to diff two ELF files contained in this repo, you can run the
following command from this repository root directory:

```bash
docker run --rm -v $(pwd):/home ghcr.io/carlosperate/bloaty:latest test-elf-files/example-after.elf -- test-elf-files/example-before.elf
```
```
    FILE SIZE        VM SIZE    
 --------------  -------------- 
   +14%  +221Ki  [ = ]       0    .debug_info
   +12% +52.4Ki  [ = ]       0    .debug_line
   +13% +46.0Ki  [ = ]       0    .debug_loc
   +13% +24.5Ki  [ = ]       0    .debug_abbrev
   +18% +20.8Ki   +18% +20.8Ki    .text
  +9.8% +16.4Ki  [ = ]       0    .debug_str
   +17% +11.2Ki  [ = ]       0    .symtab
   +21% +10.9Ki  [ = ]       0    .strtab
   +11% +7.89Ki  [ = ]       0    .debug_ranges
  +9.5% +5.57Ki  [ = ]       0    .debug_frame
  +9.3% +1.71Ki  [ = ]       0    .debug_aranges
  [ = ]       0  +9.6%    +792    .bss
 -24.4%    -120 -26.5%    -120    .data
  [ = ]       0  -0.7%    -792    .heap
 -15.2% -20.7Ki  [ = ]       0    [Unmapped]
   +12%  +397Ki  +5.6% +20.7Ki    TOTAL
```

The other `ghcr.io/carlosperate/bloaty-action` Docker image is based also
includes a custom script to add additional features for integration with
the GitHub Actions CI.

## Additional Action Examples

To add a GitHub Actions Run summary simply set the `output-to-summary` input
to `true`:

```yaml
- name: Run Bloaty McBloatface on an ELF file & add output to summary
  uses: carlosperate/bloaty-action@v1
  with:
    bloaty-args: test-elf-files/example-before.elf -- test-elf-files/example-after.elf
    output-to-summary: true
```

To add a PR comment you an use the `actions/github-script` action in a step
to post a comment with the output of a the `carlosperate/bloaty-action` step:

```yaml
- name: Run Bloaty McBloatface on an ELF file
  uses: carlosperate/bloaty-action@v1
  id: bloaty-comparison
  with:
    bloaty-args: test-elf-files/example-before.elf -- test-elf-files/example-after.elf
- name: Add a PR comment with the bloaty diff
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '## Bloaty output\n```\n${{ steps.bloaty-comparison.outputs.bloaty-output-encoded }}```\n'
      })
```

| Job Summary | PR Comment |
|-------------|------------|
| ![gh-action-summary-screenshot](https://user-images.githubusercontent.com/4189262/216423832-cfad5b15-e206-47fb-a653-45a256f9f267.png)<br><br><br> | ![PR comment screenshot](https://user-images.githubusercontent.com/4189262/216636388-9fe86aa8-4d53-47bb-be99-415fec07bc88.png) |
