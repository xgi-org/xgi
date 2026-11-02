# XGI agent skill

This directory contains an [agent skill](https://www.thepromptindex.com/how-to-use-ai-agent-skills-the-complete-guide.html)
distributed alongside the `xgi` Python package. AI coding assistants that
support the SKILL.md open standard (Claude Code, Codex, Cursor, Gemini CLI,
and skill-manager tools like `agent-skills-sdk`) discover it automatically
once `xgi` is installed.

## What it contains

- `SKILL.md` — the entire skill in one file. YAML frontmatter (name,
  description, when to activate) followed by basics, the stats interface,
  common gotchas, and idiomatic patterns. Points at the online docs for
  the rest.
- `__init__.py` — exposes `SKILL_DIR` and `SKILL_FILE` paths so
  skill-aware tools can locate the file programmatically.

## How to use this skill

### As a user of an agent that auto-discovers skills

Install xgi (`pip install xgi`) and the skill ships with it. Your agent
should find it via the standard discovery mechanism.

### As a user of an agent that needs a manual hint

Point your agent at this directory. Examples:

- Claude Code: this directory is recognized as a skill via `SKILL.md`'s
  frontmatter.
- Cursor: add a rule file at `.cursor/rules/xgi.md` with the contents
  `Use the XGI skill at <path-to-xgi>/skill/SKILL.md when working with XGI.`
- Codex / Aider / Continue: pass the file as additional context, or
  point a custom rule file to it.

### For the XGI team

The skill is one file (`SKILL.md`), hand-maintained. Update it when the
documented behavior changes. A CI check that runs the code snippets and
fails if they break would catch most drift; that hasn't been added yet.

## Why this exists

Hackathon feedback (June 2026) showed roughly half of XGI users used the
library like NetworkX and never reached the stats / generators / algorithms /
drawing surface. AI coding assistants amplify this problem: without an
explicit skill, they default to the most NetworkX-like API and miss XGI's
actual capabilities. This skill closes that gap.
