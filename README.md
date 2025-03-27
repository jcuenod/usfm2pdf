# USFM2PDF

A tool to convert USFM (Unified Standard Format Markers) Bible text to acceptably formatted PDF documents.

## Installation

First, clone this repository:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Convert a single file
python main.py path/to/your/bible.sfm -o output.pdf

# Convert multiple files using a glob pattern
python main.py "path/to/your/*.sfm"

# Convert multiple files and save to a specific directory
python main.py "path/to/your/*.sfm" --output-dir path/to/output
```

### Options

- `-o, --output`: Specify output PDF file path (default: output.pdf)
- `-d, --output-dir`: Specify output directory for multiple files (default: same as input)
- `--header`: Optional header text to display (will be printed in the top center of every page)

## Fonts

The script uses Noto Serif, which is loaded from Google Fonts. No local font installation is required.

## Example Output

The generated PDF will have:

- Chapter numbers as headings
- Verse numbers as blue superscript at the beginning of each verse
- Paragraph indentation
- Divine names in bold
- A side note on each page indicating that the PDF is for review purposes

## Limitations

This tool currently does not support:

- Footnotes
- Cross-references
- Study notes
- Images
- Tables
- Complex layout features

## License

MIT

## Acknowledgements

- [WeasyPrint](https://weasyprint.org/) for the PDF generation library
- [USFM Grammar](https://github.com/ubsicap/usfm-grammar) for USFM parsing
