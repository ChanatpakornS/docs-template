# AGENTS.md

Operating instructions for every AI agent working in this repository. This file
is canonical. Tool-specific entry points point here instead of restating
anything, so the rules exist once.

Host environment: Linux, macOS, or WSL. Assume a POSIX shell.

## What this repository is

A template. It carries the harness — an agent instruction layer and a
documentation pipeline — and no application code. `src/` is empty on purpose;
the project built on this template fills it.

The harness lives under `.claude/` so that Claude Code registers its agents,
skills, hooks, and settings with no extra wiring. Nothing inside is
Claude-only: every file is plain Markdown that any agent can read, and the
paths below are the contract for all of them.

## Directory contract

| Path | Holds | You may |
|------|-------|---------|
| `.claude/skills/` | Language and domain standards, loaded on demand | add, edit |
| `.claude/agents/` | Role definitions for delegated work | add, edit |
| `.claude/schema/` | Templates for documents you write | change by decision only |
| `.claude/hooks/` | Scripts that enforce this file | change by decision only |
| `.claude/settings.json` | Which hook runs on which tool | change by decision only |
| `docs/raw/` | Unprocessed source material | add and read, never edit |
| `docs/wiki/` | Synthesized knowledge | edit, keep consistent |
| `docs/schema/` | The documentation protocol | change by decision only |
| `src/` | Project source code | add, edit |

## Capabilities layer

Before editing a file, load the standards for its type and follow them:

| File pattern | Load this context |
|--------------|-------------------|
| `*.go` | `.claude/skills/go-standards/SKILL.md` |

Rules:

- Load a skill file the first time a task touches a matching file, and keep it
  in mind for every later edit to that file type in the same task.
- A task spanning several file types loads every matching skill.
- No matching row means no standards file exists yet. Proceed on general best
  practice and say in your reply that a skill file is missing.
- Add a file type by writing `.claude/skills/<name>-standards/SKILL.md` and
  adding a row above. The table is the configuration.
- A skill file opens with YAML frontmatter carrying `name` and `description`,
  then the standards themselves. The frontmatter is what lets Claude Code
  register the skill and invoke it by name; the table is what gets it loaded
  before an edit. Both read the same file.

Two ways the table gets loaded:

- **Claude Code** runs `.claude/hooks/enforce_ai_skills.py` before every `Edit`
  and `Write`. It matches the target filename against the rows and injects the
  skill file as context, once per session per skill. It never blocks a call.
- **Every other agent** has no such hook. Read the matching skill file yourself
  before your first edit. This is your responsibility, not the harness's.

The hook finds rows with a regular expression that matches any table row whose
first two cells are both wrapped in backticks. Keep that shape exclusive to the
table above. Elsewhere in this file, never backtick two adjacent cells, or the
hook will read that row as a skill mapping.

## Delegated roles

`.claude/agents/` holds role definitions. Read one and adopt it when a task
matches its purpose:

| Role | Use it for | Definition |
|------|------------|------------|
| code-onboarding | Explaining what unfamiliar code does and why it exists | `.claude/agents/code-onboarding.md` |
| code-improver | Reviewing code that works and proposing concrete improvements | `.claude/agents/code-improver.md` |
| sql-tester | Writing SQL setup, fixture, verification, and teardown scripts | `.claude/agents/sql-tester.md` |

Each definition states its input, procedure, output format, refusals, and stop
condition. Follow all five. The refusals are the point — a role that reviews
code does not edit it, and a role that writes SQL does not run it.

Claude Code registers these as subagents and can dispatch them by name. No
other tool does. If yours supports delegation, hand it the definition's body as
the subagent's instructions; otherwise read the file and act in that role
yourself. The definition is the contract either way.

Add a role by writing `.claude/agents/<name>.md` in the same shape and adding a row
above.

## Document templates

`.claude/schema/docs/` holds the shape of the planning documents this project
writes: story, feature, task, and review, numbered in the order they are
produced. Read the matching template before writing one of those documents and
follow its headings. A template that is still empty carries no requirements —
write the document on general best practice and say which template was blank.

## Documentation pipeline

Everything under `docs/` follows the protocol in
[`docs/schema/AGENTS.md`](docs/schema/AGENTS.md). Read it before touching
`docs/`. In short: `docs/raw/` is read-only source material, `docs/wiki/` is
synthesized knowledge with one concept per page, `docs/wiki/index.md` is the
entry point, and `docs/wiki/log.md` is an append-only changelog.

## Tool entry points

Agents look for their instructions under different filenames. Every one of them
must resolve to this file.

| Tool | Entry point | Wiring |
|------|-------------|--------|
| Codex CLI, Jules, Zed, recent Cursor | AGENTS.md | reads this file directly |
| Claude Code | CLAUDE.md | imports this file |
| Gemini CLI | GEMINI.md | needs a pointer |
| GitHub Copilot | .github/copilot-instructions.md | needs a pointer |
| Aider | CONVENTIONS.md | needs a pointer |

Entry-point names change between releases. Verify the one your tool uses before
trusting this table.

A pointer is a symlink, so the content cannot drift:

```sh
ln -s AGENTS.md GEMINI.md
mkdir -p .github && ln -s ../AGENTS.md .github/copilot-instructions.md
```

Where symlinks are unavailable, write a one-line file that says to read
`AGENTS.md`, and never put rules in it.

## Adding a tool to the harness

1. Find the filename that tool reads.
2. Point it at this file by symlink, or by a one-line pointer.
3. If the tool can run something before an edit, wire it to the capabilities
   table the way `.claude/hooks/enforce_ai_skills.py` does. If it cannot, the
   tool loads skills by hand and nothing else changes.
4. Put tool-specific setup in that tool's own file. This file stays
   tool-agnostic.
