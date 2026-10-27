#!/usr/bin/env python3
"""Check every skill's frontmatter and every relative Markdown link. Exit 1 on any problem."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith(" "):
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    errors: list[str] = []
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if not skills:
        errors.append("skills/: no skill directories")
    for skill in skills:
        path = skill / "SKILL.md"
        rel = path.relative_to(ROOT)
        if not path.is_file():
            errors.append(f"{rel}: missing")
            continue
        meta = frontmatter(path.read_text(encoding="utf-8"))
        if meta is None:
            errors.append(f"{rel}: no YAML frontmatter")
            continue
        name, description = meta.get("name", ""), meta.get("description", "")
        if name != skill.name:
            errors.append(f"{rel}: name {name!r} differs from directory {skill.name!r}")
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{rel}: name must be lowercase-hyphenated, at most 64 characters")
        if not description:
            errors.append(f"{rel}: empty description")
        elif len(description) > 1024:
            errors.append(f"{rel}: description is {len(description)} characters (max 1024)")
        if extra := sorted(set(meta) - ALLOWED_KEYS):
            errors.append(f"{rel}: unexpected frontmatter keys {extra}")

    for manifest in (ROOT / ".claude-plugin").glob("*.json"):
        try:
            json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{manifest.relative_to(ROOT)}: invalid JSON ({exc})")

    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            if not (md.parent / target.split("#", 1)[0]).exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link {target}")

    for error in errors:
        print(f"error: {error}")
    print(f"{len(skills)} skill(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
