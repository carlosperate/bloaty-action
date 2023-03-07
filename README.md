# Bloaty McBloatface GitHub Action

GitHub Action to run Google's Bloaty McBloatface - a size profiler for
binaries: https://github.com/google/bloaty/

```yaml
- name: Run Bloaty McBloatface on an ELF file
  uses: carlosperate/bloaty-action@v1
  with:
    bloaty-args: <path_to_your_file_and_any_bloaty_flags>
```

- 🧑‍💻 Additional examples, including Job Summaries and PR comments, can be
  found in the "[Additional Action Examples](#additional-action-examples)"
  section.
- 🐳 A Bloaty Docker image (`ghcr.io/carlosperate/bloaty`) is also provided,
  more info in the
  "[Using the Docker Image to run Bloaty directly](#using-the-docker-image-to-run-bloaty-directly)" section.


## Action Inputs/Outputs

Inputs:
- `bloaty-args`: **(Required)** All arguments to pass to Bloaty McBloatface.
- `output-to-summary`: *(Optional, default `false`)* Boolean (`true` or `false`) to include
  the bloaty output in the [GitHub Actions Job Summary](https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/).
- `summary-title`: *(Optional, default `"bloaty output"`)* If
  `output-to-summary` is enabled, this is the title on top of the bloaty output.

Outputs:
- `bloaty-output`: A string with the output from Bloaty McBloatface
- `bloaty-output-encoded`: The bloaty output string with escaped characters (so you'll get things like `\n`). It can be easier to pass this to other action steps.


## Using the Docker image to run Bloaty directly

This repository contains two Dockerfiles and the two Docker images are hosted in
the [GitHub Docker Container registry](https://github.blog/2020-09-01-introducing-github-container-registry/).

The [`ghcr.io/carlosperate/bloaty`](docker-bloaty/) Docker image contains the
bloaty application on its own, and can be used used to easily run `bloaty`
directly in your own environment or applications.

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

The other [`ghcr.io/carlosperate/bloaty-action`](docker-action/) Docker image
is built on top of the base `bloaty` image to run with GitHub Actions, and
includes a custom script adding GitHub Actions specific features.

## Additional Action Examples

To better understand what arguments to use with Bloaty, the documentation is
not very long and a recommended read:
[google/bloaty/doc/using.md](https://github.com/google/bloaty/blob/52948c107c8f81045e7f9223ec02706b19cfa882/doc/using.md)

Personally, I like to use the following flags to analyse where the data/memory is going:
```
bloaty -d compileunits,symbols --domain=vm <path_to_file>
```

To add a the Bloaty output to the
[GitHub Actions Job Summary](https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/)
simply set the `output-to-summary` input to `true`:

<img width="30%" src="https://user-images.githubusercontent.com/4189262/216423832-cfad5b15-e206-47fb-a653-45a256f9f267.png" align="left" alt="GH Action Run summary screenshot">

```yaml
- name: Run Bloaty & add output to the run summary
  uses: carlosperate/bloaty-action@v1
  with:
    bloaty-args: -d compileunits,symbols test-elf-files/example-before.elf
    output-to-summary: true
    summary-title: "Size profile of `example-before.elf` largest components"
```

<br clear="left"/>

To create a PR comment, add an `id` to the `carlosperate/bloaty-action` step,
and then use its output with the the
[`actions/github-script`](https://github.com/actions/github-script/) action to
post a markdown comment to the PR:

<img width="30%" src="https://user-images.githubusercontent.com/4189262/216636388-9fe86aa8-4d53-47bb-be99-415fec07bc88.png" align="left" alt="PR comment screenshot">

```yaml
- name: Run Bloaty McBloatface on an ELF file
  uses: carlosperate/bloaty-action@v1
  id: bloaty-step
  with:
    bloaty-args: test-elf-files/example-before.elf
- name: Add a PR comment with the bloaty output
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '## Bloaty output\n```\n${{ steps.bloaty-step.outputs.bloaty-output-encoded }}```\n'
      })
```

The following example shows how to build your project before and after the
PR commits, and how to post the size diff as a PR comment:

```yml
steps:
  - name: Check out the repo with the full git history
    uses: actions/checkout@v3
    with:
      fetch-depth: '0'
  - name: Build your project (example for a standard Makefile, change as required)
    run: make
  - name: Save the built ELF/Mach-O/PE/COFF file to a different directory where it doesn't get cleaned out
    run: mv <path_to_your_elf> ../original.elf
  - name: If it's a PR checkout the base commit
    if: ${{ github.event.pull_request }}
    run: git checkout ${{ github.event.pull_request.base.sha }}
  - name: Clean the build and rebuild with the base commit
    if: ${{ github.event.pull_request }}
    run: |
      make clean
      make
  - name: Run Bloaty to compare both output files
    if: ${{ github.event.pull_request }}
    id: bloaty-comparison
    uses: carlosperate/bloaty-action@v1
    with:
      bloaty-args: ../original.elf -- <path_to_the_base_commit_elf>
      output-to-summary: true
  - name: Add a PR comment with the bloaty diff
    if: ${{ github.event.pull_request }}
    continue-on-error: true
    uses: actions/github-script@v6
    with:
      script: |
        github.rest.issues.createComment({
          issue_number: context.issue.number,
          owner: context.repo.owner,
          repo: context.repo.repo,
          body: '## PR build size diff\n```\n${{ steps.bloaty-comparison.outputs.bloaty-output-encoded }}```\n'
        })
```
