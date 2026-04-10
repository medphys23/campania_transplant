"""
Map DOCX drawing paragraphs to nearby captions and image relationship targets.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.oxml.ns import qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


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


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def paragraph_image_targets(paragraph: Paragraph) -> list[str]:
    targets: list[str] = []
    for blip in paragraph._element.xpath(".//*[local-name()='blip']"):
        embed = blip.get(qn("r:embed"))
        if not embed:
            continue
        rel = paragraph.part.related_parts.get(embed)
        if rel is not None:
            targets.append(getattr(rel.partname, "filename", str(rel.partname)))
    return targets


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: map_docx_media.py <docx> [out.json]", file=sys.stderr)
        return 1

    doc_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    doc = Document(doc_path)
    blocks = list(iter_block_items(doc))
    report = []

    for idx, block in enumerate(blocks):
        if not isinstance(block, Paragraph):
            continue
        targets = paragraph_image_targets(block)
        if not targets:
            continue

        prev_text = ""
        next_text = ""
        for back in range(idx - 1, max(-1, idx - 4), -1):
            candidate = blocks[back]
            if isinstance(candidate, Paragraph) and normalize(candidate.text):
                prev_text = normalize(candidate.text)
                break
        for forward in range(idx + 1, min(len(blocks), idx + 4)):
            candidate = blocks[forward]
            if isinstance(candidate, Paragraph) and normalize(candidate.text):
                next_text = normalize(candidate.text)
                break

        report.append(
            {
                "block_index": idx,
                "targets": targets,
                "prev_text": prev_text,
                "next_text": next_text,
            }
        )

    output = json.dumps(report, indent=2, ensure_ascii=False)
    if out_path:
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
