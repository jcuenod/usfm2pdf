from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate

def usx_to_pdf(usx_elem, output_file):
    """
    Convert USX XML element to a formatted PDF file.
    
    Args:
        usx_elem: The USX XML element from usfm-grammar
        output_file: Path to the output PDF file
    """
    # Register a Unicode font
    pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-R.ttf'))
    pdfmetrics.registerFont(TTFont('Ubuntu Bold', 'Ubuntu-B.ttf'))
    
    # Parse the USX XML string
    root = usx_elem
    
    # Define a function to add the side note to each page
    def add_side_note(canvas, doc):
        canvas.saveState()
        canvas.setFont('Ubuntu', 8)  # Small font size
        canvas.setFillColorRGB(0.38, 0.45, 0.56)  # Gray color for subtlety
        
        # Position the text vertically along the right margin
        note_text = "NOTE: This PDF is for review purposes only amd does not reflect all USFM content. Footnotes and other elements are omitted."

        canvas.rotate(90)
        canvas.drawString(
            doc.bottomMargin + 20,
            -doc.leftMargin + 20,
            note_text
        )
        
        # Debug: Print page number to console
        print(f"Adding note to page {canvas.getPageNumber()}")
        
        canvas.restoreState()
    
    # Create PDF document with custom page template
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Create a frame for the main content
    content_frame = Frame(
        doc.leftMargin, 
        doc.bottomMargin, 
        doc.width, 
        doc.height,
        id='normal'
    )
    
    # Create a page template that includes our side note
    template = PageTemplate(
        id='main_template',
        frames=[content_frame],
        onPage=add_side_note
    )
    
    # Add the template to the document
    doc.addPageTemplates([template])
    
    styles = getSampleStyleSheet()
    
    # Modify styles to use Unicode font and adjust line height and indentation
    for style_name in styles.byName:
        styles[style_name].fontName = 'Ubuntu'
        
        # Only set leading if fontSize exists
        if hasattr(styles[style_name], 'fontSize'):
            styles[style_name].leading = styles[style_name].fontSize * 1.6  # Set line height to 1.6
        
        # Add first line indent to paragraph styles (but not headings or titles)
        if style_name in ['Normal', 'BodyText']:
            styles[style_name].firstLineIndent = 20  # 20 points indent for first line
    
    # Container for PDF elements
    elements = []
    
    # Process USX elements
    for elem in root.iter():
        if elem.tag == 'book':
            book_title = elem.text or elem.get('code', '')
            elements.append(Paragraph(book_title, styles['Title']))
            elements.append(Spacer(1, 12))
        
        elif elem.tag == 'chapter':
            chapter_num = elem.get('number', '')
            if chapter_num:
                elements.append(Paragraph(f"Chapter {chapter_num}", styles['Heading1']))
                elements.append(Spacer(1, 6))
        
        elif elem.tag == 'para':
            style_name = elem.get('style', 'p')
            para_style = styles['Normal']
            
            # Handle different paragraph styles
            if style_name in ['s1', 's2']:
                para_style = styles['Heading2']
            elif style_name in ['q1', 'q2']:
                para_style = styles['Italic']
                # For poetry lines, don't indent first line
                para_style.firstLineIndent = 0
                # For q1, no indent; for q2, add left indent
                if style_name == 'q2':
                    para_style.leftIndent = 20
            elif style_name == 'b':  # Blank line
                elements.append(Spacer(1, 12))
                continue
            
            # Build paragraph text with proper handling of verses
            para_text = elem.text or ""
            
            for child in elem:
                # Handle verse numbers as inline blue superscript
                if child.tag == 'verse' and child.get('number'):
                    verse_num = child.get('number')
                    para_text += f' <super><font color="#2b7fff"><span fontname="Ubuntu Bold" fontsize="7">{verse_num}</span></font></super> '
                    # Add the text content of the verse
                    if child.text:
                        para_text += child.text
                
                # Handle other elements like char
                elif child.tag == 'char':
                    style = child.get('style', '')
                    if style == 'nd':  # Divine name
                        para_text += f'<b>{child.text or ""}</b>'
                    else:
                        para_text += child.text or ""
                
                # Add any other element text
                else:
                    para_text += child.text or ""
                
                # Add tail text (text that follows the child element)
                if child.tail:
                    para_text += child.tail
            
            # Add the paragraph if it has content
            if para_text.strip():
                elements.append(Paragraph(para_text, para_style))
                if style_name not in ['q1', 'q2']:  # Don't add space after poetry lines
                    elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements, onFirstPage=add_side_note, onLaterPages=add_side_note)
    print(f"PDF created: {output_file}")
