# Documentation Protocol

This protocol governs everything under `docs/`. Follow it exactly.

## Layout

| Directory     | Role                    | Mutability                          |
|---------------|-------------------------|-------------------------------------|
| `docs/raw/`   | Unprocessed source      | Add and read only; never edit files here |
| `docs/wiki/`  | Synthesized knowledge   | Edit freely, keep consistent        |
| `docs/schema/`| This protocol           | Change only by deliberate decision  |

## 1. Raw specs (`docs/raw/`)

- Drop-zone for source material: specifications, design notes, meeting
  transcripts, RFCs, pasted research.
- Treat every file as read-only input. Do not rewrite, summarize in place,
  or delete raw files. Corrections come in as new raw files.
- Name files `YYYY-MM-DD-short-topic.md` so ordering is obvious.

## 2. Synthesis (`docs/wiki/`)

When new raw material arrives, or on request, synthesize it into the wiki:

- One concept per file: `docs/wiki/<concept>.md`. A concept is a component,
  a domain idea, a decision, or a process — something a reader would look
  up by name.
- Each wiki page starts with a one-line definition, then the detail.
- Every wiki page ends with a `## Sources` section listing the
  `docs/raw/` files it was derived from, as relative links.
- When raw material contradicts an existing page, update the page and
  record the change in the log (below). Keep the page internally
  consistent — do not leave both versions.
- Do not copy raw text verbatim. Restructure it into durable, deduplicated
  knowledge.

## 3. Knowledge graph (`docs/wiki/index.md`)

- The index is the entry point: a categorized list of every wiki page with
  its one-line definition.
- Update the index in the same change that adds or removes a wiki page.
- Express relationships between concepts as links between their pages.

## 4. Changelog (`docs/wiki/log.md`)

- Append-only. Never edit or delete an existing entry.
- Add new entries at the end of the file.
- One entry per synthesis action, in this format:

  ```
  ## YYYY-MM-DD — <short title>

  - <what raw material was ingested>
  - <which wiki pages were created or changed>
  - <index updates>
  ```

## Working order

1. Read new files in `docs/raw/`.
2. Create or update the relevant `docs/wiki/` pages, with `## Sources`.
3. Update `docs/wiki/index.md`.
4. Append an entry to `docs/wiki/log.md`.
