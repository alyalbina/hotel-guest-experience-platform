"""A local publication gate, not a replacement for credential rotation."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".venv", "data", "__pycache__", ".pytest_cache", ".ruff_cache", "htmlcov"}
PATTERNS = [
    re.compile(rb"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    re.compile(rb"\b[0-9]{7,12}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(rb'"private_key"\s*:\s*"[^"\s]'),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
]


def main():
    problems = []
    inspected = 0
    for file in ROOT.rglob("*"):
        relative = file.relative_to(ROOT)
        if not file.is_file() or any(part in IGNORED for part in relative.parts):
            continue
        if file.name.startswith(".coverage"):
            continue
        if file.name in {".env", "credits.json"} or file.suffix in {
            ".pem",
            ".key",
            ".sqlite",
            ".db",
            ".zip",
            ".pdf",
        }:
            problems.append(str(relative) + " (prohibited public file)")
        if file.suffix in {".png", ".jpg", ".jpeg"}:
            continue
        inspected += 1
        if any(pattern.search(file.read_bytes()) for pattern in PATTERNS):
            problems.append(str(relative) + " (potential credential)")
    if problems:
        raise SystemExit("Publication gate failed: " + "; ".join(problems))
    print(f"Publication gate passed: {inspected} text files; no prohibited files or credential patterns")


if __name__ == "__main__":
    main()
