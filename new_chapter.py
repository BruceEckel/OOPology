#!/usr/bin/env python3
"""Create a new chapter, renumbering existing chapters as needed."""

import argparse
import re
from pathlib import Path

CHAPTERS_DIR = Path(__file__).parent / "chapters"

TEMPLATE = """\
---
title: "{title}"
label: "Chapter {num:02d}"
published: false
---

"""

NUM_RE = re.compile(r"^(\d+)-(.+)$")


def parse_num(path: Path) -> int | None:
    m = NUM_RE.match(path.stem)
    return int(m.group(1)) if m else None


def stem_suffix(path: Path) -> str:
    """The part after the number prefix, e.g. 'what-is-an-object'."""
    m = NUM_RE.match(path.stem)
    return m.group(2) if m else path.stem


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def all_chapters() -> list[Path]:
    return sorted(
        (p for p in CHAPTERS_DIR.glob("*.md") if parse_num(p) is not None),
        key=parse_num,
    )


def renumber(path: Path, new_num: int) -> Path:
    new_name = f"{new_num:02d}-{stem_suffix(path)}.md"
    new_path = path.parent / new_name
    path.rename(new_path)
    print(f"  {path.name} → {new_name}")
    return new_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new chapter")
    parser.add_argument("number", type=int, help="Chapter number (e.g. 3)")
    parser.add_argument("title", help="Chapter title")
    args = parser.parse_args()

    num: int = args.number
    title: str = args.title

    CHAPTERS_DIR.mkdir(exist_ok=True)

    # Collect chapters that need to shift up (num >= target, in reverse order)
    to_shift = [ch for ch in reversed(all_chapters()) if parse_num(ch) >= num]
    if to_shift:
        print("Renumbering:")
        for ch in to_shift:
            renumber(ch, parse_num(ch) + 1)  # type: ignore[arg-type]

    slug = slugify(title)
    new_path = CHAPTERS_DIR / f"{num:02d}-{slug}.md"
    new_path.write_text(TEMPLATE.format(title=title, num=num), encoding="utf-8")
    print(f"Created: {new_path.name}")


if __name__ == "__main__":
    main()
