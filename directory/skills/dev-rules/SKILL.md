---
name: "dev-rules"
description: "Engineering rules and working modes from everything-claude-code — coding style, git workflow, testing, security, performance, patterns, agent use and hooks. Use when writing, reviewing or committing code (including Pip sites), when the user asks for code standards, a git/PR workflow, test coverage, a security pass, or switches mode (\"dev mode\", \"research mode\", \"review mode\")."
---

# Dev rules

Rules from everything-claude-code (MIT, Affaan Mustafa; see `LICENSE-everything-claude-code.txt`
at the plugin root). Read only the file that fits the task:

| Task | Read |
|---|---|
| Writing or refactoring code | `rules/coding-style.md`, `rules/patterns.md` |
| Commits, branches, PRs | `rules/git-workflow.md` |
| Tests, TDD, coverage | `rules/testing.md` |
| Secrets, input handling, auth | `rules/security.md` |
| Speed, bundle size, queries | `rules/performance.md` |
| When to call which agent | `rules/agents.md` |
| What the plugin's hooks do | `rules/hooks.md` |

Working modes (`contexts/`): `dev.md` (build), `research.md` (explore before acting),
`review.md` (critique). When the user names a mode, read that file and follow it for the rest
of the task.

For Pip sites: apply `coding-style`, `performance` and `security` to the site code, and
use the `e2e-runner` agent to test the built page before delivery.
