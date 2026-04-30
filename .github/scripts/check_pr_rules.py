#!/usr/bin/env python3
"""Validate contribution rules that can be checked automatically."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUSPICIOUS_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}
SUSPICIOUS_CONTENT = (
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "ghp_",
    "github_pat_",
    "xoxb-",
    "xoxa-",
    "aws_secret_access_key",
    "api_key=",
    "secret=",
)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    if not TEMPLATES.is_dir():
        fail("templates/ folder is missing.", errors)
        report(errors)
        return 1

    templates_readme = TEMPLATES / "README.md"
    if not templates_readme.is_file():
        fail("templates/README.md is missing.", errors)

    for template_dir in sorted(p for p in TEMPLATES.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if template_dir.name == "__pycache__":
            continue

        if not NAME_RE.fullmatch(template_dir.name):
            fail(
                f"Template folder '{template_dir.name}' should use lowercase letters, numbers, and hyphens only.",
                errors,
            )

        readme = template_dir / "README.md"
        if not readme.is_file():
            fail(f"Template folder '{template_dir.name}' is missing a README.md file.", errors)

        for path in template_dir.rglob("*"):
            if not path.is_file():
                continue

            if path.name.lower() in SUSPICIOUS_FILES:
                fail(
                    f"Template '{template_dir.name}' contains a sensitive-looking file name: {path.relative_to(ROOT)}",
                    errors,
                )

            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for marker in SUSPICIOUS_CONTENT:
                if marker in text:
                    fail(
                        f"Template '{template_dir.name}' contains a suspicious secret-like pattern in {path.relative_to(ROOT)}.",
                        errors,
                    )
                    break

    if errors:
        report(errors)
        return 1

    print("PR rules check passed.")
    return 0


def report(errors: list[str]) -> None:
    print("PR rules check failed:\n", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
