from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
import os
import xml.etree.ElementTree as ET
from html import escape

def usx_to_pdf(usx_elem, output_file):
    """
    Convert USX XML element to a formatted PDF file using WeasyPrint.
    
    Args:
        usx_elem: The USX XML element from usfm-grammar
        output_file: Path to the output PDF file
    """
    # Create HTML content from USX
    html_content = generate_html_from_usx(usx_elem)
    
    # Create CSS for styling
    css_content = generate_css()
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
        f.write(html_content)
        temp_html_path = f.name
    
    try:
        # Generate PDF using WeasyPrint
        html = HTML(filename=temp_html_path)
        css = CSS(string=css_content)
        html.write_pdf(
            output_file,
            stylesheets=[css],
            font_config=font_config
        )
        print(f"PDF created: {output_file}")
    finally:
        # Clean up temporary file
        os.unlink(temp_html_path)

def generate_html_from_usx(usx_elem):
    """Generate HTML content from USX element."""
    # Start with HTML structure
    html = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="UTF-8">',
        '<title>Bible Text</title>',
        '</head>',
        '<body>',
        '<div class="bible-content">'
    ]
    
    # Process USX elements
    book_title = ""
    current_chapter = ""
    
    for elem in usx_elem.iter():
        if elem.tag == 'book':
            book_title = elem.text or elem.get('code', '')
            html.append(f'<h1 class="book-title">{escape(book_title)}</h1>')
        
        elif elem.tag == 'chapter':
            chapter_num = elem.get('number', '')
            if chapter_num:
                current_chapter = chapter_num
                html.append(f'<h2 class="chapter-number">Chapter {escape(chapter_num)}</h2>')
        
        elif elem.tag == 'para':
            style_name = elem.get('style', 'p')
            
            # Determine paragraph class based on style
            para_class = 'paragraph'
            if style_name in ['s1', 's2']:
                para_class = 'section-heading'
            elif style_name == 'q1':
                para_class = 'poetry-q1'
            elif style_name == 'q2':
                para_class = 'poetry-q2'
            elif style_name == 'b':
                html.append('<div class="blank-line"></div>')
                continue
            
            # Start paragraph
            html.append(f'<p class="{para_class}">')
            
            # Process paragraph content
            if elem.text:
                html.append(escape(elem.text))
            
            for child in elem:
                if child.tag == 'verse' and child.get('number'):
                    verse_num = child.get('number')
                    html.append(f'<span class="verse-number">{escape(verse_num)}</span>')
                    
                    # Add verse text
                    if child.text:
                        html.append(escape(child.text))
                
                elif child.tag == 'char':
                    style = child.get('style', '')
                    if style == 'nd':  # Divine name
                        html.append(f'<span class="divine-name">{escape(child.text or "")}</span>')
                    else:
                        html.append(escape(child.text or ""))
                
                else:
                    html.append(escape(child.text or ""))
                
                # Add tail text
                if child.tail:
                    html.append(escape(child.tail))
            
            # End paragraph
            html.append('</p>')
    
    # Add side note
    html.append('<div class="side-note">DRAFT: This PDF does not reflect all USFM content. Footnotes and other elements are omitted.</div>')
    
    # Close HTML structure
    html.append('</div>')  # Close bible-content
    html.append('</body>')
    html.append('</html>')
    
    return '\n'.join(html)

def generate_css():
    """Generate CSS for styling the HTML content."""
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,100..900;1,100..900&display=swap');
    
    @page {
        size: letter;
        margin: 1in;
        @bottom-left {
            content: "DRAFT: This PDF does not reflect all USFM content. Footnotes and other elements are omitted.";
            font-family: Noto Serif, serif;
            font-size: 7pt;
            color: #666;
        }
    }
    
    body {
        font-family: Noto Serif, serif;
        font-size: 10pt; /* Reduced from 12pt */
        line-height: 1.5;
        color: #000;
    }
    
    .bible-content {
        margin: 0 auto;
        column-count: 2;       /* Create two columns */
        column-gap: 1.5em;     /* Space between columns */
        column-rule: 1px solid #eee; /* Optional: thin line between columns */
    }
    
    /* Ensure these elements don't break across columns */
    .book-title, .chapter-number, .section-heading {
        column-span: all;      /* Make headings span across all columns */
    }
    
    .book-title {
        font-size: 20pt;       /* Reduced from 24pt */
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    }
    
    .chapter-number {
        font-size: 16pt;       /* Reduced from 18pt */
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    
    .paragraph {
        text-indent: 1.5em;
        margin-bottom: 0.5em;
        text-align: justify;   /* Justify text for cleaner column edges */
    }
    
    .section-heading {
        font-size: 12pt;       /* Reduced from 14pt */
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.5em;
        text-indent: 0;
    }
    
    .poetry-q1 {
        margin-left: 1.5em;
        text-indent: 0;
    }
    
    .poetry-q2 {
        margin-left: 2.5em;    /* Reduced from 3em to save space */
        text-indent: 0;
    }
    
    .verse-number {
        font-size: 6pt;        /* Reduced from 7pt */
        color: blue;
        font-weight: bold;
        vertical-align: super;
        margin-right: 0.2em;
    }
    
    .divine-name {
        font-variant: small-caps;
        font-weight: bold;
    }
    
    .blank-line {
        height: 0.8em;         /* Reduced from 1em */
    }
    
    .side-note {
        display: none;         /* Hidden in body, shown via @page rule */
    }
    
    /* Prevent orphans and widows */
    p {
        orphans: 2;
        widows: 2;
    }
    """
    return css

# Optional: Add a direct conversion function for convenience
def convert_usfm_to_pdf(usfm_string, output_file):
    """
    Convert USFM string directly to PDF.
    
    Args:
        usfm_string: USFM content as string
        output_file: Path to the output PDF file
    """
    from usfm_grammar import USFMParser
    
    # Parse USFM to USX
    parser = USFMParser(usfm_string)
    usx_elem = parser.to_usx()
    
    # Convert USX to PDF
    usx_to_pdf(usx_elem, output_file)
