# Changelog

Append-only. Newest entries at the bottom. Never edit or remove past entries.
Format defined in [`../schema/AGENTS.md`](../schema/AGENTS.md).

## 2026-09-06 — Repository scaffold

- Ingested: setup task defining the AI boilerplate environment (LLM wiki
  pattern + modular skills architecture). No files added to `docs/raw/`.
- Created capabilities layer: `.ai/skills/go-standards.md`,
  `.ai/skills/php-standards.md`, `.ai/agents/` (empty), and root
  `AGENTS.md` with the dynamic context-loading rules.
- Created documentation layer: `docs/raw/`, `docs/wiki/`, `docs/schema/`,
  the documentation protocol at `docs/schema/AGENTS.md`, and this log.
- Index: initialized `docs/wiki/index.md` with empty category sections.

## 2026-09-26 — Harness moved from `.ai/` to `.claude/`

- Ingested: request to make the template usable as a harness by any AI agent,
  then to relocate the capabilities layer. No files added to `docs/raw/`.
- Moved `.ai/skills/go-standards.md` to
  `.claude/skills/go-standards/SKILL.md` and gave it `name` and `description`
  frontmatter, so Claude Code registers it as an invocable skill as well as a
  hook-injected standards file. The `.ai/` directory is gone; the paths
  recorded in the 2026-09-06 entry above are historical.
- Moved the role definitions to `.claude/agents/` — `code-improver`,
  `code-onboarding`, `sql-tester` — where Claude Code registers them as
  subagents. Each was rewritten to state input, procedure, output format,
  refusals, and stop condition.
- Moved the document templates to `.claude/schema/docs/`. Only `02_feature.md`
  has content; `index.md`, `01_story.md`, `03_task.md`, and `04_review.md` are
  still empty.
- Rewrote root `AGENTS.md` as the canonical, tool-agnostic instruction file,
  covering the directory contract, capabilities table, role registry, document
  templates, and the entry-point filename each agent tool reads. `CLAUDE.md`
  now imports it and holds only Claude Code specifics.
- Wrote `README.md` describing the template under the name `docs-template`.
- Wiki pages: none created or changed.
- Index: no change — no wiki pages added.
