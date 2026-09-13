#!/usr/bin/env python3
"""PreToolUse hook: enforces the AGENTS.md capabilities-layer convention.

Before an Edit/Write touches a file matching a row in AGENTS.md's
"File pattern -> Load this context" table, this injects that row's
`.ai/skills/*.md` file into the model's context (once per session per
skill), so the standards are actually loaded instead of relying on the
agent to remember to read them.

Never blocks the tool call -- this only adds context.
"""
import fnmatch
import json
import re
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = REPO_ROOT / "AGENTS.md"

# Matches markdown table rows like: | `*.go` | `.ai/skills/go-standards.md` |
TABLE_ROW_RE = re.compile(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|")


def load_table():
    """Parse (glob_pattern, skill_relpath) pairs out of AGENTS.md."""
    try:
        text = AGENTS_MD.read_text()
    except OSError:
        return []
    return TABLE_ROW_RE.findall(text)


def main():
    hook_input = json.load(sys.stdin)
    tool_input = hook_input.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path")
    session_id = hook_input.get("session_id", "unknown-session")

    if not file_path:
        return  # nothing to match against; allow silently

    filename = Path(file_path).name
    table = load_table()

    match = next(
        ((pattern, skill_rel) for pattern, skill_rel in table
         if fnmatch.fnmatch(filename, pattern)),
        None,
    )
    if match is None:
        return  # no row in AGENTS.md covers this file type; allow silently

    pattern, skill_rel = match
    skill_path = REPO_ROOT / skill_rel

    if not skill_path.is_file():
        print(json.dumps({
            "systemMessage": (
                f"AGENTS.md maps {pattern} -> {skill_rel}, but that skill "
                f"file doesn't exist. Proceeding without loaded standards."
            ),
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": (
                    f"[AGENTS.md capabilities layer] No skill file found at "
                    f"{skill_rel} for {pattern} files. Per AGENTS.md, note "
                    f"that a skill file is missing and proceed with general "
                    f"best practice."
                ),
            },
        }))
        return

    state_dir = Path(tempfile.gettempdir()) / "claude-ai-skill-hook" / session_id
    marker = state_dir / (skill_path.stem + ".loaded")

    if marker.exists():
        # Already loaded this session -- short reminder, no need to resend
        # the whole file.
        print(json.dumps({
            "suppressOutput": True,
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": (
                    f"[AGENTS.md capabilities layer] Reminder: keep "
                    f"following {skill_rel} ({pattern} standards, already "
                    f"loaded this session) for this edit."
                ),
            },
        }))
        return

    state_dir.mkdir(parents=True, exist_ok=True)
    marker.touch()

    skill_content = skill_path.read_text()
    print(json.dumps({
        "systemMessage": f"Loaded {skill_rel} into context (first {pattern} edit this session).",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": (
                f"[AGENTS.md capabilities layer] Editing a {pattern} file. "
                f"Per AGENTS.md, load and follow these standards from "
                f"{skill_rel} for this and every later {pattern} edit in "
                f"this task:\n\n{skill_content}"
            ),
        },
    }))


if __name__ == "__main__":
    main()
