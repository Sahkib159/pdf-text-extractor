# PDF Text Extractor

A free, local Python tool that extracts text from PDFs and can use OCR to read scanned pages. It splits long results into smaller `.txt` files and keeps page markers so you can find text in the original document.

**Your PDF is processed on your computer. This tool does not upload documents to a server.**

## Features

- Extract selectable text from ordinary PDFs
- Optional OCR for scanned/image-only pages using Tesseract
- OCR every page when needed, including mixed PDFs
- Split long output into manageable text files
- Preserve original page numbers in the output
- Support OCR languages installed in Tesseract, including English and Bangla
- Free and open source

## Requirements

- Python 3.10 or newer
- PyMuPDF (`pymupdf`)
- For OCR: Tesseract OCR installed separately, plus the language data you need

## Installation

### 1. Install Python

Download Python from [python.org](https://www.python.org/downloads/). On Windows, enable **Add Python to PATH** during installation if that option is shown.

### 2. Download this project

Click **Code → Download ZIP** on GitHub and extract the folder, or clone it:

```powershell
git clone https://github.com/YOUR-USERNAME/pdf-text-extractor.git
cd pdf-text-extractor
```

Replace `YOUR-USERNAME` with the GitHub account that hosts this project.

### 3. Install the Python dependency

```powershell
py -m pip install -r requirements.txt
```

### 4. Install OCR (only needed for scanned PDFs)

Follow the official [Tesseract OCR installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html). On Windows, the UB Mannheim installer is a commonly used option.

Make sure Tesseract is available on your `PATH`. Install the language data you need:
- English: `eng`
- Bangla: `ben`
- Both: `eng+ben`

You can check whether Tesseract is available by running:

```powershell
tesseract --version
tesseract --list-langs
```

If Windows says `tesseract` is not recognized, add the Tesseract installation folder to your `PATH`, then reopen PowerShell.

## Usage

Put your PDF anywhere on your computer, then run the script from the project folder.

### A. Extract text from a normal PDF

```powershell
py pdf_text_extractor.py "C:\path\to\document.pdf"
```

Text files will be saved to `converted_text`.

### B. Extract text and OCR pages that have no selectable text

```powershell
py pdf_text_extractor.py "C:\path\to\scanned-document.pdf" --ocr
```

This is a good default for PDFs containing a mixture of normal text pages and scanned pages.

### C. OCR every page

```powershell
py pdf_text_extractor.py "C:\path\to\scanned-document.pdf" --force-ocr
```

### D. OCR English and Bangla

```powershell
py pdf_text_extractor.py "C:\path\to\bangla-document.pdf" --ocr --language ben
```

For a document containing both languages:

```powershell
py pdf_text_extractor.py "C:\path\to\mixed-language.pdf" --force-ocr --language eng+ben
```

The language codes must be installed in Tesseract first.

### E. Choose output folder and chunk size

```powershell
py pdf_text_extractor.py "C:\path\to\document.pdf" --ocr --output-dir "my_text" --max-chars 50000
```

### F. Improve OCR for difficult scans

```powershell
py pdf_text_extractor.py "C:\path\to\document.pdf" --force-ocr --dpi 300
```

Higher DPI can improve recognition but uses more time and memory. The default is 200 DPI.

### See all options

```powershell
py pdf_text_extractor.py --help
```

## Output example

```text
converted_text/
├── part_001.txt
├── part_002.txt
└── part_003.txt
```

Each page is marked in the text:

```text
--- PAGE 1 ---
Recognized text from page one...

--- PAGE 2 ---
Recognized text from page two...
```

## Troubleshooting

### `No module named pymupdf`

```powershell
py -m pip install -r requirements.txt
```

### Tesseract or language data not found

Check `tesseract --version` and `tesseract --list-langs`. Confirm that the requested language is installed and Tesseract is on `PATH`. Close and reopen PowerShell after changing `PATH`.

### OCR output is inaccurate

Scans with low resolution, skew, handwriting, unusual fonts, columns, equations, or tables may produce errors. Try `--dpi 300`, use the correct language, or improve the scan. OCR output should be checked against the original for important work.

### A page is still empty

It may be blank, damaged, or in a language for which no OCR data is installed.

## Privacy and safety

- PDFs are read locally and are not sent to this project's author.
- Do not commit private PDFs, extracted text, or confidential documents to GitHub.
- OCR is performed by the local Tesseract installation.

## Limitations

- OCR is not perfect and can misread characters.
- Text extraction does not preserve the exact page layout.
- Tables, mathematical notation, columns, and diagrams may need manual review.
- This tool creates text files; it does not summarize or interpret the document.

## Contributing

Bug reports and improvements are welcome. Please include your operating system, Python version, command used, and a redacted error message. Do not attach confidential documents.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
