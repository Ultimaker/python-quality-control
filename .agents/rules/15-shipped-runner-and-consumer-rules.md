---
name: shipped-runner-and-consumer
description: This repository is the shared CI configuration. The run_*.sh scripts are the product, not a local test suite, and the consumers are firmware and cloud repositories.
trigger: always_on
---

# The Runners Are The Product

This repository holds no application code. It holds the linting and test
configuration that other repositories mount as a git submodule named `ci`.

## 1. This repository has no test suite of its own

`git ls-files` returns no test file and no `conftest.py`. `cfg/` holds only
`.ini` and `.txt` files.

Rule `04-build-test-and-deployment-rules.md` lists two detected test commands.
Neither command tests this repository. Do not run them here.

- `pytest -x -q cfg` collects nothing and exits with "no tests ran".
- `./run_pytest.sh` fails with `FileNotFoundError` for `./ci/cfg/pytest.ini`.
  That path exists only inside a consumer, where this repository is mounted
  at `ci`.

Verify a change to a runner script in a consumer checkout, or with
`shellcheck`. State in the pull request which consumer you used.

## 2. The root scripts are the published surface

The scripts in the repository root are the artefact that consumers call. Each
one reads its configuration from `./ci/cfg/`, so it only runs from a consumer
working directory.

`references.sh` computes the changed-file list for every linter. It also reads
an optional `linting_excluded_files.txt` from the consumer root. Consumers rely
on that behaviour. Never remove it.

The scripts in `local/` are the developer-machine variants. Change a root
script and its `local/` counterpart in the same commit.

## 3. No consumer may be assumed

This repository serves firmware repositories and cloud repositories. Examples:
`opinicus`, `okuda` and `libCharon`.

1. Never add a rule, a path or a default that assumes a cloud service.
2. Never add a rule, a path or a default that assumes a printer.
3. Keep every path in a runner relative to the consumer root.

## 4. A change here lands in every consumer

Land the change in this repository first. Then move each consumer's `ci`
submodule pointer in its own commit. Name the consumers in the pull request.
A change that tightens a linter breaks every consumer that has not fixed its
code yet, so announce it before you merge it.
