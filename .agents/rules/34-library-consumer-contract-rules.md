---
name: library-consumer-contract
description: This repository's public surface (runner scripts, linter configs in cfg/, CI workflows) is mounted into 14+ consumer repositories — any change is a cross-repository contract.
trigger: glob
glob: "*.sh"
paths:
  - "*.sh"
  - "cfg/*"
  - "local/*"
  - ".github/**/*"
  - "**/*.py"
---
# Library Consumer Contract

This repository is consumed by downstream repositories rather than run on its own.
Sibling checkouts across firmware and cloud pin this repository as a submodule at `ci`:
`okuda`, `opinicus`, `dbus-interface-lib`, `libLogger`, `libCharon`, `print-process-reporting`,
`misp-service`, `ultiLib`, `libSmeagol`, `mqttHandler`, `ebpf-io-logger`, `UMBusService`, etc.

A service is bounded by its own process: rename an internal function and nothing outside notices.
This repository has no such boundary. Its public surface is mounted directly into downstream builds and CI pipelines.

## Published Surface & What Constitutes a Breaking Change

Within the published surface, all of the following are contract changes, not isolated refactors:

1. **Tightening Linter Configuration (`cfg/`)**:
   - Adding new linter error codes or strict checks in `cfg/.flake8`, `cfg/mypy.ini`, `cfg/pylintrc`, or `cfg/pycodestyle.ini` will immediately fail CI runs across downstream repositories if their code does not comply.
2. **Modifying Runner Scripts (`run_*.sh`, `references.sh`)**:
   - Renaming runner scripts, altering command-line arguments, or changing environment variable contracts (such as `PARENT_BRANCH` in `references.sh`) affects all consumers calling `./ci/run_*.sh`.
3. **Altering Submodule Layout**:
   - Moving or renaming directories (`cfg/`, `local/`) breaks consumers whose scripts rely on paths like `./ci/cfg/pytest.ini`.

## How to Make Contract Changes

1. **Name Affected Consumers in the PR**:
   - Identify which downstream repositories are affected (e.g. `opinicus`, `okuda`, `dbus-interface-lib`, `libLogger`, `libCharon`).
2. **Land Changes Here First, Then Update Consumer Pointers**:
   - Merge the quality control repository changes to `master`.
   - Update the `ci` submodule pointer in each consumer repository in a dedicated commit referencing the Jira ticket.
3. **Additive & Coordinated Updates**:
   - When introducing stricter linter rules, test against active consumer branches and coordinate PRs to clean up lint in consumers before or alongside submodule bumps.
4. **Transparent Commit Messages**:
   - Detail the changes and migration steps in the commit message so downstream developers and agents understand rule adjustments.
