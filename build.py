#!/usr/bin/env python3
"""Build OOPology: converts Markdown chapters to styled HTML."""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).parent
CHAPTERS_DIR = REPO_ROOT / "chapters"
DOCS_DIR = REPO_ROOT / "docs"
TEMPLATE = REPO_ROOT / "template.html"

BOOK_TITLE = "OOPology"
BOOK_AUTHOR = "Bruce Eckel"

HEADING_FONT = "Lexend Deca"
HEADING_FONT_GOOGLE = "Lexend+Deca:wght@400;600;700"


def parse_frontmatter(md_path: Path) -> tuple[dict, str]:
    """Extract YAML-ish frontmatter and body from a Markdown file."""
    text = md_path.read_text(encoding="utf-8")
    meta: dict = {}
    if text.startswith("---"):
        end = text.index("---", 3)
        front = text[3:end].strip()
        for line in front.splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"')
        body = text[end + 3:].strip()
    else:
        body = text
    return meta, body


def is_published(md_path: Path) -> bool:
    meta, _ = parse_frontmatter(md_path)
    return meta.get("published", "true").lower() == "true"


def chapter_files() -> list[Path]:
    all_chapters = sorted(CHAPTERS_DIR.glob("*.md"))
    unpublished = [ch.name for ch in all_chapters if not is_published(ch)]
    if unpublished:
        print(f"Skipping unpublished: {', '.join(unpublished)}")
    return [ch for ch in all_chapters if is_published(ch)]


def slug(path: Path) -> str:
    return path.stem


def html_name(path: Path) -> str:
    return f"{slug(path)}.html"


def build_chapter(
    md_path: Path,
    prev_chapter: Path | None,
    next_chapter: Path | None,
    index: int,
    total: int,
) -> None:
    meta, _ = parse_frontmatter(md_path)
    title = meta.get("title", md_path.stem.replace("-", " ").title())
    label = meta.get("label", f"Chapter {index}")

    vars: list[str] = [
        f"--variable=title:{title}",
        f"--variable=chapter-label:{label}",
        f"--variable=heading-font:{HEADING_FONT}",
        f"--variable=heading-font-google:{HEADING_FONT_GOOGLE}",
    ]

    if prev_chapter:
        prev_meta, _ = parse_frontmatter(prev_chapter)
        prev_title = prev_meta.get("title", prev_chapter.stem)
        vars += [
            f"--variable=prev-url:{html_name(prev_chapter)}",
            f"--variable=prev-title:{prev_title}",
        ]
    if next_chapter:
        next_meta, _ = parse_frontmatter(next_chapter)
        next_title = next_meta.get("title", next_chapter.stem)
        vars += [
            f"--variable=next-url:{html_name(next_chapter)}",
            f"--variable=next-title:{next_title}",
        ]

    out = DOCS_DIR / html_name(md_path)
    cmd = [
        "pandoc",
        str(md_path),
        "--template", str(TEMPLATE),
        "--output", str(out),
        "--from", "markdown+smart",
        "--syntax-highlighting", "tango",
        *vars,
    ]
    subprocess.run(cmd, check=True)
    print(f"  {md_path.name} → {out.name}")


def build_index(chapters: list[Path]) -> None:
    items = []
    for i, ch in enumerate(chapters, 1):
        meta, _ = parse_frontmatter(ch)
        title = meta.get("title", ch.stem.replace("-", " ").title())
        items.append((i, html_name(ch), title))

    toc_items = "\n".join(
        f'    <li><span class="toc-num">{i:02d}</span>'
        f'<a href="{url}">{title}</a></li>'
        for i, url, title in items
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{BOOK_TITLE}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family={HEADING_FONT_GOOGLE}&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Cormorant+SC:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="page">
    <p class="book-author">{BOOK_AUTHOR}</p>
    <h1 class="book-title">{BOOK_TITLE}</h1>
    <div class="title-rule"></div>
    <ul class="toc-list">
{toc_items}
    </ul>
    <p class="copyright">© 2026 {BOOK_AUTHOR}. All Rights Reserved.<br>
    Freely readable online. No reproduction without permission.</p>
  </div>
</body>
</html>"""

    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")
    print("  index.html")


def build_css() -> None:
    """Write shared CSS to docs/ (index page uses it; chapters are self-contained)."""
    css = f"""
:root {{
  --ink: #1a1612; --paper: #f5f0e8; --muted: #7a6e62;
  --accent: #8b1a1a; --rule: #c8bfb0; --max-width: 680px;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ font-size: 18px; }}
body {{ background: var(--paper); color: var(--ink);
  font-family: Georgia, serif; line-height: 1.75;
  padding: 0 1.5rem; }}
.page {{ max-width: var(--max-width); margin: 0 auto; padding: 4rem 0 6rem; }}
.book-title {{ font-family: '{HEADING_FONT}', sans-serif; font-size: 3.5rem;
  font-weight: 600; line-height: 1.1; margin-bottom: 0.5rem; }}
.book-author {{ font-family: 'Cormorant SC', serif; font-size: 0.85rem;
  letter-spacing: 0.15em; color: var(--muted); margin-bottom: 0.5rem; }}
.title-rule {{ width: 3rem; height: 1px; background: var(--accent);
  margin: 1.5rem 0 2.5rem; }}
.toc-list {{ list-style: none; margin-top: 2rem; }}
.toc-list li {{ display: flex; align-items: baseline;
  padding: 0.6rem 0; border-bottom: 1px solid var(--rule); }}
.toc-list li:first-child {{ border-top: 1px solid var(--rule); }}
.toc-num {{ font-family: 'Cormorant SC', serif; font-size: 0.7rem;
  letter-spacing: 0.1em; color: var(--muted); min-width: 2.5rem; }}
.toc-list a {{ font-family: 'Cormorant Garamond', serif; font-size: 1.15rem;
  color: var(--ink); text-decoration: none; flex: 1; }}
.toc-list a:hover {{ color: var(--accent); }}
.copyright {{ margin-top: 5rem; font-size: 0.78rem; color: var(--muted);
  font-family: 'Cormorant SC', serif; letter-spacing: 0.05em; }}
"""
    (DOCS_DIR / "style.css").write_text(css.strip(), encoding="utf-8")
    print("  style.css")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build OOPology book site")
    parser.add_argument("--clean", action="store_true", help="Remove docs/ before building")
    args = parser.parse_args()

    if args.clean and DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
        print("Cleaned docs/")

    DOCS_DIR.mkdir(exist_ok=True)

    chapters = chapter_files()
    if not chapters:
        print("No chapters found in chapters/")
        return

    print("Building chapters:")
    for i, ch in enumerate(chapters):
        prev_ch = chapters[i - 1] if i > 0 else None
        next_ch = chapters[i + 1] if i < len(chapters) - 1 else None
        build_chapter(ch, prev_ch, next_ch, i + 1, len(chapters))

    print("Building index:")
    build_index(chapters)
    build_css()
    print(f"\nDone. {len(chapters)} chapter(s) → docs/")


if __name__ == "__main__":
    main()
