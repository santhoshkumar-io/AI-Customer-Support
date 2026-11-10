"""Load knowledge_base/*.md into the knowledge_base table.

Each file is one section, named after the file. Each "## " heading inside the
file is one entry: the heading is the title, the lines under it are the content.

Run from the project root:

    uv run python -m scripts.seed_knowledge_base

Rerunning updates the content of existing entries instead of adding duplicates,
so anything edited in the dashboard is overwritten.
"""

from pathlib import Path

from app.db import connect

KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"

UPSERT = """
insert into knowledge_base (section, title, content) values (%s, %s, %s)
on conflict (section, title) do update
  set content = excluded.content, updated_at = now()
"""


def parse_file(path: Path) -> list[tuple[str, str, str]]:
    """Split one markdown file into (section, title, content) rows."""
    section = path.stem
    text = path.read_text(encoding="utf-8")
    entries = []
    # The first chunk is the "# Title" preamble above the first heading.
    for block in text.split("\n## ")[1:]:
        title, _, content = block.partition("\n")
        entries.append((section, title.strip(), content.strip()))
    return entries


def main() -> None:
    paths = sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))
    if not paths:
        raise SystemExit(f"No markdown files in {KNOWLEDGE_BASE_DIR}")

    total = 0
    with connect() as conn:
        for path in paths:
            entries = parse_file(path)
            for entry in entries:
                conn.execute(UPSERT, entry)
            print(f"{path.stem}: {len(entries)} entries")
            total += len(entries)
    print(f"total: {total} entries")


if __name__ == "__main__":
    main()
