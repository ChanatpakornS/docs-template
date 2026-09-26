# CLAUDE.md

Claude Code reads this file. The rules for every agent in this repository live
in `AGENTS.md`, and the import below loads them. Do not restate them here —
one copy, no drift.

@AGENTS.md

## Claude Code specifics

- `.claude/settings.json` registers a `PreToolUse` hook on `Edit` and `Write`.
  `.claude/hooks/enforce_ai_skills.py` reads the capabilities table in
  `AGENTS.md`, matches the target filename, and injects the matching standards
  file into context — once per session per skill, then a short reminder. It
  never blocks a call, and a missing skill file only produces a warning.
- The hook fires on `Edit` and `Write` only. Editing a file through `Bash`
  bypasses it, so load the skill yourself when you do that.
- Role definitions live in `.claude/agents/`, so they register as subagents.
  Dispatch them by name with the `Agent` tool: `code-onboarding`,
  `code-improver`, `sql-tester`. Their refusals are part of the definition; do
  not override them from the call site.
- Skills live in `.claude/skills/<name>/SKILL.md` and register under their
  frontmatter `name`, so `go-standards` is invocable with the `Skill` tool. You
  rarely need to invoke it — the hook already injects it on the first `.go`
  edit of a session.
