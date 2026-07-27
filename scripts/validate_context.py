#!/usr/bin/env python3
"""Validate Black Blaze context integrity without network access."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ".git",
    ".research-clones",
    ".research-venv",
    ".tmp",
    ".cache",
    "node_modules",
}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
}

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "context-engineering/00-start-here/STAGEME_START_HERE.md",
    "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md",
    "context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md",
    "context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md",
    "context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md",
    "context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md",
    "context-engineering/09-planning/DECISION_LOG.md",
    "context-engineering/10-sources/SOURCE_LEDGER.md",
    "context-engineering/10-sources/repositories.json",
]

ACTIVE_STATUS_FILES = [
    "README.md",
    "AGENTS.md",
    "context-engineering/00-start-here/EXECUTIVE_BRIEF.md",
    "context-engineering/00-start-here/CONTEXT_MAP.md",
    "context-engineering/00-start-here/STAGEME_START_HERE.md",
    "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md",
    "context-engineering/09-planning/STAGEME_SPIKE_PROTOCOL.md",
    "context-engineering/06-technical/STAGEME_SYSTEM_DESIGN.md",
    "context-engineering/08-strategy/STAGEME_REFERENCE_IMPLEMENTATIONS.md",
    "context-engineering/09-planning/STAGEME_AGENT_BUILD_HANDOFF.md",
]

STALE_PATTERNS = [
    re.compile(r"StageMe remains a hypothesis", re.I),
    re.compile(r"No build is selected", re.I),
    re.compile(r"StageMe[^\n]{0,80}not (?:yet )?selected", re.I),
    re.compile(r"ReachPack\s*/\s*AccessSpec is the leading", re.I),
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def is_excluded(path: Path) -> bool:
    """Return whether a repository-relative path sits under an ignored audit directory."""
    return bool(EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts))


def validate_required(errors: list[str]) -> None:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if is_excluded(path):
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"local link escapes repository: {path.relative_to(ROOT)} -> {raw}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"broken local link: {path.relative_to(ROOT)} -> {raw}"
                )


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if is_excluded(path):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - validator should report all parse errors
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")

    ledger_path = ROOT / "context-engineering/10-sources/repositories.json"
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except Exception:
        return

    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(ledger):
        label = f"repositories.json[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} is not an object")
            continue
        owner = item.get("owner")
        repo = item.get("repo")
        commit = item.get("commit")
        key = (str(owner).lower(), str(repo).lower())
        if key in seen:
            errors.append(f"duplicate repository entry: {owner}/{repo}")
        seen.add(key)
        if not owner or not repo:
            errors.append(f"{label} missing owner/repo")
        if not isinstance(commit, str) or not HEX40_RE.fullmatch(commit):
            errors.append(f"{label} has malformed commit: {commit!r}")
        if not item.get("license"):
            errors.append(f"{label} missing explicit license status")
        if not item.get("inspected_at"):
            errors.append(f"{label} missing inspected_at")


def validate_secrets(errors: list[str]) -> None:
    """Catch common credential forms in committed documentation and JSON."""
    candidates = [*ROOT.rglob("*.md"), *ROOT.rglob("*.json")]
    for path in candidates:
        if is_excluded(path):
            continue
        text = path.read_text(encoding="utf-8")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {name} in {path.relative_to(ROOT)}")


def validate_active_status(errors: list[str]) -> None:
    for rel in ACTIVE_STATUS_FILES:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in STALE_PATTERNS:
            if match := pattern.search(text):
                excerpt = match.group(0).replace("\n", " ")
                errors.append(f"stale active status in {rel}: {excerpt!r}")


def validate_core_phrase(errors: list[str]) -> None:
    product = (ROOT / "context-engineering/09-planning/STAGEME_PRODUCT_SPEC.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "rough sung performance",
        "original",
        "bounded",
        "non-goals",
        "source-conditioned",
    ]
    for term in required_terms:
        if term.lower() not in product.lower():
            errors.append(f"canonical product spec missing required term: {term}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_markdown_links(errors)
    validate_json(errors)
    validate_secrets(errors)
    validate_active_status(errors)
    validate_core_phrase(errors)

    if errors:
        print(f"FAIL: {len(errors)} context error(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    markdown_count = sum(1 for path in ROOT.rglob("*.md") if not is_excluded(path))
    json_count = sum(1 for path in ROOT.rglob("*.json") if not is_excluded(path))
    ledger_count = len(
        json.loads(
            (ROOT / "context-engineering/10-sources/repositories.json").read_text(
                encoding="utf-8"
            )
        )
    )
    print("PASS: context integrity checks succeeded")
    print(f"- markdown files checked: {markdown_count}")
    print(f"- JSON files checked: {json_count}")
    print(f"- repository ledger entries checked: {ledger_count}")
    print(f"- required StageMe files checked: {len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
