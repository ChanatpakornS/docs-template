# AGENTS.md

Operating instructions for AI agents working in this repository.

`harness` is a meta / boilerplate repository. It carries an AI development
environment — a modular skills layer and an LLM wiki — rather than
application code. The files under `.ai/skills/` are reusable standards
templates; the files under `docs/` are a documentation pipeline.

## Capabilities layer — dynamic context loading

Before editing a file, load the standards for its language and follow them:

| File pattern        | Load this context                |
|---------------------|----------------------------------|
| `*.go`              | `.ai/skills/go-standards.md`     |
| `*.php`             | `.ai/skills/php-standards.md`    |

Rules:

- Load a skill file the first time a task touches a matching file, and keep
  it in mind for every later edit to that language in the same task.
- If a task spans multiple languages, load each relevant skill.
- If no skill matches the language, proceed with general best practice and
  note that a skill file is missing.
- `.ai/agents/` holds role-specific agent definitions. Load one when a task
  matches its stated purpose.

When you add a new language to this repo, add a matching
`.ai/skills/<lang>-standards.md` and a row to the table above.

## Documentation layer — the LLM wiki

All work with `docs/` follows the protocol in
[`docs/schema/AGENTS.md`](docs/schema/AGENTS.md). In short: `docs/raw/` is
read-only source material, `docs/wiki/` is synthesized structured
knowledge, and `docs/wiki/log.md` is an append-only changelog.
