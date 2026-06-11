#!/usr/bin/env python3
"""Create a new chapter, renumbering existing chapters as needed."""

import argparse
import re
from pathlib import Path

CHAPTERS_DIR = Path(__file__).parent / "chapters"

_ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen",
]
_TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def num_to_word(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + (f"-{_ONES[ones]}" if ones else "")
    return str(n)


TEMPLATE = """\
---
title: "{title}"
label: "Chapter {num_word}"
published: true
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
        key=lambda p: parse_num(p) or 0,
    )


def renumber(path: Path, new_num: int) -> Path:
    new_name = f"{new_num:02d}-{stem_suffix(path)}.md"
    new_path = path.parent / new_name
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'^(label:\s*"Chapter\s+)[^"]+(")',
        f'\\g<1>{num_to_word(new_num)}\\g<2>',
        text,
        flags=re.MULTILINE,
    )
    path.rename(new_path)
    new_path.write_text(text, encoding="utf-8")
    print(f"  {path.name} -> {new_name}")
    return new_path


def update_labels() -> None:
    """Ensure every chapter's label matches its filename number."""
    chapters = all_chapters()
    if not chapters:
        print("No chapters found.")
        return
    changed = 0
    for ch in chapters:
        num = parse_num(ch)
        if num is None:
            continue
        expected = num_to_word(num)
        text = ch.read_text(encoding="utf-8")
        new_text = re.sub(
            r'^(label:\s*"Chapter\s+)[^"]+(")',
            f'\\g<1>{expected}\\g<2>',
            text,
            flags=re.MULTILINE,
        )
        if new_text != text:
            ch.write_text(new_text, encoding="utf-8")
            print(f"  {ch.name}: updated label to Chapter {expected}")
            changed += 1
        else:
            print(f"  {ch.name}: ok")
    print(f"\n{changed} file(s) updated.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new chapter")
    parser.add_argument("number", type=int, nargs="?", help="Chapter number (e.g. 3)")
    parser.add_argument("title", nargs="?", help="Chapter title")
    parser.add_argument("--update", action="store_true", help="Sync all chapter labels to their filename numbers")
    args = parser.parse_args()

    if args.update:
        update_labels()
    else:
        if args.number is None or args.title is None:
            parser.error("number and title are required when not using --update")

        num: int = args.number
        title: str = args.title

        CHAPTERS_DIR.mkdir(exist_ok=True)

        # Collect chapters that need to shift up (num >= target, in reverse order)
        to_shift = [ch for ch in reversed(all_chapters()) if (parse_num(ch) or 0) >= num]
        if to_shift:
            print("Renumbering:")
            for ch in to_shift:
                renumber(ch, (parse_num(ch) or 0) + 1)

        slug = slugify(title)
        new_path = CHAPTERS_DIR / f"{num:02d}-{slug}.md"
        new_path.write_text(TEMPLATE.format(title=title, num_word=num_to_word(num)), encoding="utf-8")
        print(f"Created: {new_path.name}")
