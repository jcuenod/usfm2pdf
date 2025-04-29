from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
import os
from html import escape
from css_helper import generate_css

DEFAULT_NOTO_URL = "https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,100..900;1,100..900&display=swap"


def usx_to_pdf(usx_elem, output_file, header="", custom_noto_url=None):
    """
    Convert USX XML element to a formatted PDF file using WeasyPrint.

    Args:
        usx_elem: The USX XML element from usfm-grammar
        output_file: Path to the output PDF file
    """
    # Create HTML content from USX
    html_content = generate_html_from_usx(usx_elem)

    # Create CSS for styling
    css_content = generate_css(header)

    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(
        suffix=".html", delete=False, mode="w", encoding="utf-8"
    ) as f:
        f.write(html_content)
        temp_html_path = f.name

    try:
        # Generate PDF using WeasyPrint
        html = HTML(filename=temp_html_path)
        main_stylesheet = CSS(string=css_content)
        font_url = custom_noto_url or DEFAULT_NOTO_URL
        html.write_pdf(
            output_file,
            stylesheets=[
                main_stylesheet,
                font_url,
            ],
        )
        print(f"PDF created: {output_file}")
    finally:
        # Clean up temporary file
        os.unlink(temp_html_path)


def generate_html_from_usx(usx_elem):
    """Generate HTML content from USX element."""
    # Start with HTML structure
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="UTF-8">',
        "<title>Bible Text</title>",
        "</head>",
        "<body>",
        '<div class="side-notice">FOR REVIEW - NOTE: This document does not reflect all USFM content. Footnotes and other elements are omitted.</div>',
        '<div class="bible-content">',
    ]

    # Process USX elements
    book_title = ""
    current_chapter = ""
    has_printed_current_chapter = False
    introductory_material = True

    for elem in usx_elem.iter():
        if elem.tag == "book":
            book_title = elem.text or elem.get("code", "")
            html.append(f'<h1 class="book-title">{escape(book_title)}</h1>')

        elif elem.tag == "chapter":
            chapter_num = elem.get("number", "")
            if chapter_num:
                introductory_material = False
                current_chapter = chapter_num
                has_printed_current_chapter = False
                # html.append(f'<h2 class="chapter-number">Chapter {escape(chapter_num)}</h2>')

        elif elem.tag == "para":
            style_name = elem.get("style", "p")

            # Determine paragraph class based on style
            para_class = "paragraph"
            if style_name in ["s", "s1", "s2"]:  # Section heading
                para_class = "section-heading"
            elif style_name == "q1":  # Poetry line
                para_class = "poetry-q1"
            elif style_name == "q2":  # Poetry line 2
                para_class = "poetry-q2"
            elif style_name == "b":  # Blank line
                html.append('<div class="blank-line"></div>')
                continue
            elif introductory_material:
                para_class = "introductory-material"

            should_maybe_print_chapter = not (
                para_class == "introductory-material" or para_class == "section-heading"
            )
            # Start paragraph
            if should_maybe_print_chapter and not has_printed_current_chapter:
                # We are going to add the chapter number to the first paragraph of the chapter
                # so we need to suppress the indent
                html.append(f'<p class="{para_class} suppress-indent">')
                html.append(
                    f'<span class="chapter-number">{escape(current_chapter)}</span>'
                )
                has_printed_current_chapter = True
            else:
                html.append(f'<p class="{para_class}">')

            # Process paragraph content
            if elem.text:
                html.append(escape(elem.text))

            for child in elem:
                if child.tag == "verse" and child.get("number"):
                    verse_num = child.get("number")
                    if verse_num != "1":
                        html.append(
                            f'<span class="verse-number">{escape(verse_num)}</span>'
                        )

                    # Add verse text
                    if child.text:
                        html.append(escape(child.text))

                elif child.tag == "char":
                    style = child.get("style", "")
                    if style == "nd":  # Divine name
                        html.append(
                            f'<span class="divine-name">{escape(child.text or "")}</span>'
                        )
                    else:
                        html.append(escape(child.text or ""))

                else:
                    html.append(escape(child.text or ""))

                # Add tail text
                if child.tail:
                    html.append(escape(child.tail))

            # End paragraph
            html.append("</p>")

    # Add side note
    html.append(
        '<div class="side-note">DRAFT: This PDF does not reflect all USFM content. Footnotes and other elements are omitted.</div>'
    )

    # Close HTML structure
    html.append("</div>")  # Close bible-content
    html.append("</body>")
    html.append("</html>")

    return "\n".join(html)
