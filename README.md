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
python main.py path/to/your/bible.sfm -o output.pdf
```

### Options

- `-o, --output`: Specify output PDF file path (default: output.pdf)

## Font Requirements

The script uses the Ubuntu font by default. Make sure you have the following font files available in your cache:
- Ubuntu-R.ttf (Regular)
- Ubuntu-B.ttf (Bold)

You can download these fonts from the [Ubuntu Font Family](https://design.ubuntu.com/font/) website.

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

- [ReportLab](https://www.reportlab.com/) for the PDF generation library
- [USFM Grammar](https://github.com/ubsicap/usfm-grammar) for USFM parsing
