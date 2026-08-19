---
name: ultimaker-skill-discovery
description: Skills from the UltiCortex catalogue that apply to this repository, and when to load them.
trigger: always_on
---
# UltiMaker Skill Discovery & Usage

This repository has been matched against the UltiCortex skill catalogue. Loading
the relevant skill is **not optional** for the work it covers: these skills carry
the standards, idioms, and tooling knowledge that the rules in this directory
assume you already have.

```bash
# Search the catalogue
gh skill search ultimaker --owner Ultimaker

# Install a specific skill
gh skill install Ultimaker/UltiCortex <skill-name>
```

Load the skill **before** designing or implementing, not after review comments
arrive. If a skill contradicts a rule in this directory, raise the conflict
rather than silently picking one.

## Skills Matched To This Repository

### `software-architect` — always relevant

Expert software-architecture advisor: design patterns (GoF), SOLID/DRY, enterprise patterns (Fowler PoEAA), DDD/CQRS, evolutionary architecture (monolith-first, strangler fig, microservices), distributed systems, C4 diagrams, C++….

**Why it applies here:** SOLID, DRY and the design-pattern catalogue — the reference to consult when a change needs decomposition rather than more lines in an existing module.

```bash
gh skill install Ultimaker/UltiCortex software-architect
```

## Other Catalogue Skills

26 further skill(s) exist that no automatic trigger matched.
They are indexed in `.agents/rules/40-skill-discovery-index-rules.md` (a
model-decision rule, loaded only when judged relevant) rather than here,
because by construction they are the ones static detection judged irrelevant —
and this file is loaded every session.

```bash
gh skill search ultimaker --owner Ultimaker
```
