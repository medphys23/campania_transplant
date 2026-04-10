"""
Search PDF text for exact or near-exact strings.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

from pypdf import PdfReader


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or " ").strip()


def extract_pages(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    return [normalize(page.extract_text() or "") for page in reader.pages]


def main() -> int:
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("query")
    parser.add_argument("--ignore-case", action="store_true")
    parser.add_argument("--context", type=int, default=120)
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    query = args.query
    pages = extract_pages(pdf_path)

    haystack_query = query.lower() if args.ignore_case else query

    for page_num, text in enumerate(pages, start=1):
        haystack = text.lower() if args.ignore_case else text
        start = 0
        found = False
        while True:
            idx = haystack.find(haystack_query, start)
            if idx == -1:
                break
            found = True
            left = max(0, idx - args.context)
            right = min(len(text), idx + len(query) + args.context)
            snippet = text[left:right]
            print(f"PAGE {page_num}: {snippet}")
            start = idx + len(query)
        if found:
            print("-" * 40)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
