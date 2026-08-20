---
name: jira-commit-standards
description: Jira work tracking and commit message standards.
trigger: always_on
---
# Jira & Git Commit Standards

1. **Jira Work Tracking**:
   - All branches MUST reference an active Jira ticket starting with project key `EMB` (e.g. `EMB-463-short-description`).
2. **Commit Title Standard**:
   - Every commit title MUST start with bracketed Jira ticket key: `[EMB-463] <Descriptive Title>`.
   - Do NOT use semantic commit prefixes (`feat:`, `fix:`, `chore:`, `refactor:`) in commit or PR titles.
3. **Commit Message Body (Why & How)**:
   - Commit messages must include an explanatory body detailing the *why* (business rationale, root cause, or requirement) and the *how* (technical implementation details, affected components).
4. **Pull Request Policy**:
   - Always open PRs in **DRAFT** state.
   - Merging is strictly restricted to human developers.
