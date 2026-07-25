#!/usr/bin/env python3
"""Validate the Black Blaze context repository without network access."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".research-clones", ".research-venv"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
}
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "context-engineering/00-start-here/EXECUTIVE_BRIEF.md",
    "context-engineering/02-rules/ELIGIBILITY_AND_RULES.md",
    "context-engineering/03-submission/SUBMISSION_CHECKLIST.md",
    "context-engineering/06-technical/REPOSITORY_AUDITS.md",
    "context-engineering/10-sources/facts.json",
    "context-engineering/10-sources/repositories.json",
]


def main() -> int:
    errors: list[str] = []
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md")
        if not EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts)
    )
    json_files = sorted(
        path for path in ROOT.rglob("*.json")
        if not EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts)
    )

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - validator reports parser error
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repo: {path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken relative link: {path.relative_to(ROOT)} -> {target}")

        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {name} in {path.relative_to(ROOT)}")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"VALIDATION PASSED: {len(markdown_files)} Markdown files, "
        f"{len(json_files)} JSON files, required files present, "
        "relative links resolved, no matched secret patterns."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
