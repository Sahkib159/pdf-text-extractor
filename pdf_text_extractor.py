#!/usr/bin/env python3
"""Extract text from PDFs, with optional OCR for scanned pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    print("PyMuPDF is not installed. Run: py -m pip install -r requirements.txt")
    raise SystemExit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs and optionally OCR scanned pages.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF")
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=Path("converted_text"),
        help="Folder where text files will be saved",
    )
    parser.add_argument(
        "--ocr", action="store_true",
        help="OCR only pages that have no extractable text (requires Tesseract)",
    )
    parser.add_argument(
        "--force-ocr", action="store_true",
        help="OCR every page, including pages that already contain selectable text",
    )
    parser.add_argument(
        "--language", default="eng",
        help="Tesseract language code, e.g. eng, ben, or eng+ben",
    )
    parser.add_argument(
        "--dpi", type=int, default=200,
        help="OCR resolution. Higher values may improve recognition but take longer",
    )
    parser.add_argument(
        "--max-chars", type=int, default=80000,
        help="Approximate maximum characters per output text file",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.pdf.exists() or not args.pdf.is_file():
        print(f"Error: PDF not found: {args.pdf}")
        return 2
    if args.pdf.suffix.lower() != ".pdf":
        print("Error: input file must have a .pdf extension.")
        return 2
    if args.dpi < 72 or args.dpi > 600:
        print("Error: --dpi must be between 72 and 600.")
        return 2
    if args.max_chars < 1000:
        print("Error: --max-chars must be at least 1000.")
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    part_number = 1
    buffer: list[str] = []
    buffer_chars = 0
    saved_files: list[Path] = []
    pages_without_text: list[int] = []

    try:
        with pymupdf.open(args.pdf) as pdf:
            if pdf.needs_pass:
                print("Error: this PDF is password-protected.")
                return 2

            total_pages = len(pdf)
            print(f"Input: {args.pdf}")
            print(f"Pages: {total_pages}")
            print("Mode: OCR every page" if args.force_ocr else
                  "Mode: OCR pages without text" if args.ocr else
                  "Mode: text extraction only")
            print()

            for index, page in enumerate(pdf):
                page_number = index + 1
                print(f"Processing page {page_number}/{total_pages}...", end=" ")

                text = page.get_text("text").strip()
                should_ocr = args.force_ocr or (args.ocr and not text)

                if should_ocr:
                    try:
                        text_page = page.get_textpage_ocr(
                            language=args.language,
                            dpi=args.dpi,
                            full=True,
                        )
                        text = page.get_text("text", textpage=text_page).strip()
                    except Exception as exc:
                        print("OCR failed.")
                        print(
                            "\nOCR could not run. Check that Tesseract OCR is installed, "
                            "its language data is installed, and Tesseract is available "
                            "on your PATH.\n"
                            f"Details: {exc}"
                        )
                        return 1

                if not text:
                    pages_without_text.append(page_number)
                    text = "[No text could be extracted from this page.]"

                page_block = f"\n\n--- PAGE {page_number} ---\n{text}\n"

                if buffer and buffer_chars + len(page_block) > args.max_chars:
                    out_file = args.output_dir / f"part_{part_number:03}.txt"
                    out_file.write_text("".join(buffer), encoding="utf-8")
                    saved_files.append(out_file)
                    print(f"saved {out_file.name}")
                    part_number += 1
                    buffer = []
                    buffer_chars = 0
                else:
                    print("done.")

                buffer.append(page_block)
                buffer_chars += len(page_block)

            if buffer:
                out_file = args.output_dir / f"part_{part_number:03}.txt"
                out_file.write_text("".join(buffer), encoding="utf-8")
                saved_files.append(out_file)

    except Exception as exc:
        print(f"\nError while reading the PDF: {exc}")
        return 1

    print("\nConversion complete!")
    print(f"Text files created: {len(saved_files)}")
    print(f"Output folder: {args.output_dir.resolve()}")
    for out_file in saved_files:
        print(f"  - {out_file.name}")

    if pages_without_text:
        print(
            "\nWarning: no text was recognized on these pages: "
            + ", ".join(map(str, pages_without_text))
        )
        print("They may be blank, image-only, or need a different OCR language.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
