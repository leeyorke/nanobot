"""Detect slash-command skill invocations and annotate the message for the LLM."""

from __future__ import annotations

from typing import Any


def skill_command_prompt(content: str, skills_loader: Any) -> str:
    """If *content* is ``/skill-name`` matching a known skill, annotate it.

    The annotation tells the LLM to read the skill's SKILL.md and follow its
    instructions, bridging the gap between a raw slash command and the
    progressive-loading skill mechanism.

    Returns the original *content* unchanged when there is no match.
    """
    text = content.strip()
    if not text.startswith("/"):
        return content

    cmd = text[1:].strip().lower()
    if not cmd or "/" in cmd:
        # Empty command or sub-path like /foo/bar — not a skill name.
        return content

    # Avoid intercepting known built-in slash commands.
    # Priority (stop/restart/status) and most exact commands are handled by
    # the CommandRouter before BUILD, but /skill and /pairing are exact
    # commands that could coincide with a skill name.  Checking them here
    # is a safety net.
    _builtin_commands = frozenset({
        "new", "help", "history", "model", "goal", "dream",
        "dream-log", "dream-restore", "skill", "pairing", "status",
    })
    if cmd in _builtin_commands:
        return content

    # Build a name lookup from the skills loader.
    skills = getattr(skills_loader, "list_skills", None)
    if not callable(skills):
        return content

    for entry in skills(filter_unavailable=True):
        if entry.get("name", "").lower() == cmd:
            skill_name = entry["name"]
            skill_path = entry.get("path", "")
            annotation = (
                f"[Skill Invocation: \"{skill_name}\"]\n"
                f"The user typed /{skill_name} which invokes this skill. "
                f"Start by reading its SKILL.md at {skill_path} with read_file, "
                f"then follow its instructions to respond."
            )
            return f"{content}\n\n{annotation}"

    return content
