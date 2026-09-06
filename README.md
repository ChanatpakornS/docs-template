# harness

Version 0.0.1

A meta / boilerplate repository carrying a reusable AI development
environment: a modular skills layer and an LLM wiki. It holds no
application code — just the scaffolding pattern.

## Layout

```
.ai/
  skills/     Language standards loaded on demand (go, php)
  agents/     Role-specific agent definitions
AGENTS.md     Root protocol — maps file types to the skill to load
docs/
  raw/        Read-only source material (specs, notes, transcripts)
  wiki/       Synthesized knowledge, one concept per page
  schema/     The documentation protocol itself
```

## How it works

- **Capabilities layer.** When an agent edits a file, `AGENTS.md` tells it
  which `.ai/skills/*-standards.md` to load first (`*.go` → Go standards,
  `*.php` → PHP standards). Add a language by adding a skill file and a row
  to the table in `AGENTS.md`.
- **LLM wiki.** Raw material lands in `docs/raw/` untouched. Agents
  synthesize it into structured pages under `docs/wiki/`, keep
  `docs/wiki/index.md` current, and append every change to
  `docs/wiki/log.md`. Full protocol in `docs/schema/AGENTS.md`.

## Changelog

### 0.0.1

- Initial scaffold: `.ai/skills/` (Go and PHP standards), `.ai/agents/`,
  root `AGENTS.md`, and the `docs/` LLM-wiki pipeline
  (`raw/`, `wiki/`, `schema/`).
