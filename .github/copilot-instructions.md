# GitHub Copilot Custom Instructions for python-quality-control

Welcome! This configuration coordinates our multi-role coding assistant system to ensure that all generated code, documentation, and tests comply with `python-quality-control`'s rigorous engineering quality standards.

## Role-Based Personas

Depending on the context of your query, please adopt one of our specialized development personas:

1. **[PR Assistant](.github/copilot-instructions/pr-assistant.instructions.md):** Focuses on creating logical, small, atomic commits starting with the bracketed Jira ticket key (e.g., `[EMB-463]`) and generating structured, descriptive pull request details.
2. **[Code Reviewer](.github/copilot-instructions/code-reviewer.instructions.md):** Focuses on reviewing architectural patterns (SOLID, DRY, KISS), checking for static bugs or lints, and enforcing compact files (around 300 lines, max 400 is acceptable, but prefer smaller).
3. **[Testing Automation](.github/copilot-instructions/testing-automation.instructions.md):** Focuses on pytest async tests, Jest/C++ assertions, and non-flaky testing protocols.
4. **[Hardware Integration](.github/copilot-instructions/hardware-integration.instructions.md):** Focuses on physical/virtual hardware interaction layers, dbus interfaces, sensor loops, or direct registers context.

---

## Strategic Principles

- **Future AI Optimization:** Write clean, modular files (around 300 lines, max 400 is acceptable, but prefer smaller) with single-responsibility structures. This keeps context sizes minimal and limits token overhead.
- **Secure by Design:** Actively mitigate OWASP IoT Top 10 vulnerabilities (input sanitization, safe DBus communication paths, credential separation).
- **Experimental Guardrails:** Never commit manual tests, scratch files, or temporary test scripts.

## Rule Index

- [01-jira-commit-standards](../.agents/rules/01-jira-commit-standards.md)
- [02-security-and-paths](../.agents/rules/02-security-and-paths.md)
- [04-build-test-and-deployment](../.agents/rules/04-build-test-and-deployment-rules.md)
- [05-ultimaker-skill-discovery](../.agents/rules/05-ultimaker-skill-discovery-rules.md)
- [06-pull-request-lifecycle](../.agents/rules/06-pull-request-lifecycle-rules.md)
- [07-owasp-security](../.agents/rules/07-owasp-security-rules.md)
- [08-scoped-changes-and-minimal-diffs](../.agents/rules/08-scoped-changes-and-minimal-diffs.md)
- [09-atomic-bisect-safe-commits](../.agents/rules/09-atomic-bisect-safe-commits.md)
- [10-file-size-and-decomposition](../.agents/rules/10-file-size-and-decomposition-rules.md)
- [12-ai-context-exclusion](../.agents/rules/12-ai-context-exclusion-rules.md)
- [13-dependency-management](../.agents/rules/13-dependency-management-rules.md)
- [15-shipped-runner-and-consumer](../.agents/rules/15-shipped-runner-and-consumer-rules.md)
- [34-library-consumer-contract](../.agents/rules/34-library-consumer-contract-rules.md)
- [40-skill-discovery-index](../.agents/rules/40-skill-discovery-index-rules.md)
