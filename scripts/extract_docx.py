"""
Extract text and tables from a Word document for auditing.
Outputs paragraphs and tables in document order, and notes figure/image positions.s
"""
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    print("python-docx is required. Run: pip install python-docx", file=sys.stderr)
    sys.exit(1)


def iter_block_items(parent):
    """Yield paragraphs and tables in document order (body, then each section)."""
    from docx.document import Document as _Document
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl
    from docx.table import _Cell, Table
    from docx.text.paragraph import Paragraph

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


def table_to_markdown(table: Table) -> str:
    """Convert a docx Table to a markdown table string."""
    rows = []
    for i, row in enumerate(table.rows):
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
        rows.append("| " + " | ".join(cells) + " |")
    if not rows:
        return "[Empty table]\n"
    # Header separator
    num_cols = len(table.rows[0].cells)
    rows.insert(1, "| " + " | ".join(["---"] * num_cols) + " |")
    return "\n".join(rows) + "\n"


def has_drawing(paragraph: Paragraph) -> bool:
    """Check if paragraph contains a drawing (image/chart)."""
    nodes = paragraph._element.xpath(".//*[local-name()='drawing' or local-name()='pict']")
    return len(nodes) > 0


def main():
    root = Path(__file__).resolve().parent.parent
    default_docx = root / "documents" / "campania_transplant_final.docx"
    default_out = root / "documents" / "campania_transplant_extracted.md"

    docx_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_docx
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_out

    if not docx_path.exists():
        print(f"Error: file not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    doc = Document(docx_path)
    out_lines = [
        "# Extracted content",
        f"Source: {docx_path.name}",
        "",
    ]

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if has_drawing(block):
                out_lines.append("")
                out_lines.append("---")
                out_lines.append("[FIGURE/IMAGE]")
                if text:
                    out_lines.append(text)
                out_lines.append("---")
                out_lines.append("")
            elif text:
                # Preserve heading style if detectable (outline level)
                out_lines.append(text)
                out_lines.append("")
        elif isinstance(block, Table):
            out_lines.append("")
            out_lines.append(table_to_markdown(block))
            out_lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Written: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
