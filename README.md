# docs-template

A template repository carrying a reusable AI development environment: an
on-demand capabilities layer and a documentation pipeline. It ships no
application code — `src/` is left empty for whatever you build on top.

Target environment: Linux, macOS, or WSL.

## Layout

| Path | Role |
|------|------|
| `AGENTS.md` | Canonical instructions for every agent — the only copy of the rules |
| `CLAUDE.md` | Claude Code entry point; imports `AGENTS.md`, adds Claude-only notes |
| `.claude/skills/` | Language standards as registered skills, loaded on demand |
| `.claude/agents/` | Role definitions, registered as subagents |
| `.claude/schema/docs/` | Templates for story, feature, task, and review documents |
| `.claude/settings.json` | Wires the capabilities hook to `Edit` and `Write` |
| `.claude/hooks/enforce_ai_skills.py` | Injects the matching standards file before an edit |
| `docs/raw/` | Read-only source material — specs, notes, transcripts |
| `docs/wiki/` | Synthesized knowledge, plus `index.md` and `log.md` |
| `docs/schema/AGENTS.md` | The documentation protocol itself |
| `src/` | Project source code |

## Capabilities layer

`AGENTS.md` carries a table mapping a filename glob to the standards file an
agent must load before editing that kind of file:

| File pattern | Load this context |
|--------------|-------------------|
| `*.go` | `.claude/skills/go-standards/SKILL.md` |

`.claude/hooks/enforce_ai_skills.py` enforces the table instead of trusting
the agent to remember it. On every `Edit` or `Write`, the hook:

1. Parses the pattern/skill rows out of `AGENTS.md`.
2. Matches the target filename against each glob, first row wins.
3. Injects that skill file's full text as additional context — once per
   session per skill, then a short reminder for later edits.

The hook never blocks a tool call. A file type with no matching row passes
silently; a row pointing at a missing skill file yields a warning and the
edit proceeds on general best practice.

Add a language by writing `.claude/skills/<lang>-standards/SKILL.md` and adding
a row to the table in `AGENTS.md`. The hook needs no change — the table is the
configuration. A skill file carries YAML frontmatter with `name` and
`description`, which is what makes it invocable by name as well as
hook-injected. `go-standards` ships as the worked example: formatting, naming,
pass-by-reference rules, error wrapping, context, concurrency, and table-driven
tests.

## Documentation pipeline

`docs/schema/AGENTS.md` holds the full protocol. In short:

1. Source material lands in `docs/raw/`, named `YYYY-MM-DD-short-topic.md`.
   Those files are never edited or deleted — corrections arrive as new files.
2. An agent synthesizes them into `docs/wiki/<concept>.md`: one concept per
   page, a one-line definition first, a `## Sources` section last linking the
   raw files it came from.
3. `docs/wiki/index.md` lists every page with its definition, grouped into
   Concepts, Components, Decisions, and Processes. It is updated in the same
   change that adds or removes a page.
4. `docs/wiki/log.md` gets one append-only entry per synthesis action.

Mutability differs per directory: `docs/raw/` is add-and-read-only,
`docs/wiki/` is edited freely but kept internally consistent, and
`docs/schema/` changes only by deliberate decision.

## Using this template

1. Copy the repository and reset its git history.
2. Rewrite this README for your project.
3. Put the standards for your languages in `.claude/skills/` and update the
   `AGENTS.md` table to match.
4. Point your other agents at `AGENTS.md`. It lists the entry-point filename
   each tool reads and the symlink that wires it up.
5. Drop your first specs into `docs/raw/`, then ask the agent to synthesize.
6. Build in `src/`.

## Requirements

- `python3` on `PATH`, for the capabilities hook.
- An agent that reads `AGENTS.md` or `CLAUDE.md`. The hook itself is Claude
  Code specific; the rest of the pattern is portable, and every file under
  `.claude/` is plain Markdown that any agent can read.
