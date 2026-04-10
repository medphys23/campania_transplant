"""
Compare figure, table, and caption structure between two DOCX files.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


@dataclass
class BlockInfo:
    index: int
    kind: str
    text: str
    has_drawing: bool = False


def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        parent_elm = getattr(parent, "element", parent)
        if hasattr(parent_elm, "body"):
            parent_elm = parent_elm.body
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def has_drawing(paragraph: Paragraph) -> bool:
    return bool(paragraph._element.xpath(".//*[local-name()='drawing' or local-name()='pict']"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def summarize_table(table: Table) -> str:
    rows = []
    for row in table.rows[:3]:
        rows.append(" | ".join(normalize(cell.text) for cell in row.cells[:5]))
    return " / ".join(filter(None, rows))


def collect_blocks(doc_path: Path) -> list[BlockInfo]:
    doc = Document(doc_path)
    blocks: list[BlockInfo] = []
    for index, block in enumerate(iter_block_items(doc)):
        if isinstance(block, Paragraph):
            text = normalize(block.text)
            blocks.append(
                BlockInfo(
                    index=index,
                    kind="paragraph",
                    text=text,
                    has_drawing=has_drawing(block),
                )
            )
        else:
            blocks.append(
                BlockInfo(
                    index=index,
                    kind="table",
                    text=summarize_table(block),
                )
            )
    return blocks


def collect_key_items(blocks: list[BlockInfo]) -> dict[str, dict]:
    items: dict[str, dict] = {}
    for i, block in enumerate(blocks):
        if block.kind != "paragraph":
            continue
        if not block.text.startswith(("Figure ", "Table ")):
            continue
        next_block = blocks[i + 1] if i + 1 < len(blocks) else None
        items[block.text] = {
            "index": block.index,
            "has_drawing_next": bool(next_block and next_block.kind == "paragraph" and next_block.has_drawing),
            "next_kind": next_block.kind if next_block else None,
            "next_text": next_block.text if next_block else "",
        }
    return items


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: compare_docx_versions.py <old.docx> <new.docx> [out.json]", file=sys.stderr)
        return 1

    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    old_items = collect_key_items(collect_blocks(old_path))
    new_items = collect_key_items(collect_blocks(new_path))

    report = {
        "old_path": str(old_path),
        "new_path": str(new_path),
        "missing_in_new": {k: v for k, v in old_items.items() if k not in new_items},
        "missing_in_old": {k: v for k, v in new_items.items() if k not in old_items},
        "changed_following_object": {},
    }

    for caption in sorted(set(old_items) & set(new_items)):
        if old_items[caption]["next_kind"] != new_items[caption]["next_kind"] or old_items[caption]["has_drawing_next"] != new_items[caption]["has_drawing_next"]:
            report["changed_following_object"][caption] = {
                "old": old_items[caption],
                "new": new_items[caption],
            }

    output = json.dumps(report, indent=2, ensure_ascii=False)
    if out_path:
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
