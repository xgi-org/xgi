"""XGI agent skill package marker.

Exposes the on-disk path of the skill directory so that skill-aware tools
can discover it without scanning. The agent-facing content is in the
adjacent ``.md`` files.
"""

from pathlib import Path

SKILL_DIR = Path(__file__).parent
"""Filesystem path to the directory containing SKILL.md and associated files."""

SKILL_FILE = SKILL_DIR / "SKILL.md"
"""Filesystem path to the SKILL.md entry point."""

__all__ = ["SKILL_DIR", "SKILL_FILE"]
