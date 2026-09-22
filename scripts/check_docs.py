"""Check local Markdown links in maintained guides; no network or dependencies."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAINTAINED_DOCS = (
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "README_CHVG.md",
    "README_VARIANT_C.md",
    "TRAINING_GUIDE_CHVG4.md",
    "data/README.md",
    "bytetrack_ppe/README.md",
    "docs/README.md",
    "docs/QUICKSTART.md",
    "docs/QUICKSTART_VI.md",
    "docs/architecture.md",
    "docs/CLI.md",
    "docs/TESTING.md",
    "docs/TROUBLESHOOTING.md",
    "docs/TRAINING_PATHS.md",
    "docs/TRAINING.md",
    "docs/EVENT_ENGINE.md",
    "docs/INTEGRATION.md",
)
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\s*\)")
HTML_LINK = re.compile(r'\bhref=["\']([^"\']+)["\']')


def prose(text: str, *, remove_inline: bool = True) -> str:
    """Remove fenced and inline code so examples are not interpreted as links."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(\x60{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(re.sub(r"(\x60+).*?\1", "", line) if remove_inline else line)
    return "\n".join(lines)


def heading_ids(text: str) -> set[str]:
    """Support ordinary ATX headings and duplicate GitHub-style slugs."""
    identifiers = set()
    counts: dict[str, int] = {}
    for match in re.finditer(
        r"^#{1,6}\s+(.+)$", prose(text, remove_inline=False), re.MULTILINE
    ):
        heading = re.sub(r"\s+#+\s*$", "", match.group(1))
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        duplicate = counts.get(slug, 0)
        identifiers.add(f"{slug}-{duplicate}" if duplicate else slug)
        counts[slug] = duplicate + 1
    identifiers.update(re.findall(r'\bid=["\']([^"\']+)["\']', text))
    return identifiers


def check_documents(root: Path, documents=MAINTAINED_DOCS) -> list[str]:
    root = root.resolve()
    errors = []
    for relative in documents:
        source = root / relative
        if not source.is_file():
            errors.append(f"{relative}: document missing")
            continue
        text = prose(source.read_text(encoding="utf-8"))
        targets = [m.group(1).strip("<>") for m in LINK.finditer(text)]
        targets.extend(HTML_LINK.findall(text))
        for href in targets:
            if href.startswith("//"):
                continue
            parsed = urlsplit(href)
            if parsed.scheme in {"http", "https", "mailto"}:
                continue
            if parsed.scheme or parsed.netloc or parsed.path.startswith(("/", "\\")):
                errors.append(f"{relative}: non-portable link {href}")
                continue
            destination = (
                (source.parent / unquote(parsed.path)).resolve()
                if parsed.path else source.resolve()
            )
            if not destination.is_relative_to(root):
                errors.append(f"{relative}: link escapes repository: {href}")
            elif not destination.exists():
                errors.append(f"{relative}: missing target: {href}")
            elif parsed.fragment and destination.suffix.lower() == ".md":
                anchors = heading_ids(destination.read_text(encoding="utf-8"))
                if unquote(parsed.fragment) not in anchors:
                    errors.append(f"{relative}: missing heading: {href}")
    return errors


def main() -> int:
    errors = check_documents(ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Documentation links: PASS ({len(MAINTAINED_DOCS)} maintained guides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
