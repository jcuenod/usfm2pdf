main_css = """
body {
    font-family: Noto Serif, serif;
    font-size: 9pt;
    line-height: 1.4;
    color: oklch(0.208 0.042 265.755);
}

/* Side notice that runs up the left side */
.side-notice {
    position: absolute;
    left: -0.4in;  /* Position it in the left margin */
    top: 50%;      /* Center vertically */
    width: 7in;    /* Long enough to span the page height */
    transform: rotate(270deg) translateX(-50%);  /* Rotate and adjust position */
    transform-origin: left top;  /* Set rotation origin */
    font-size: 8pt;
    color: oklch(0.554 0.046 257.417);
    text-align: center;
    font-style: italic;
}

.bible-content {
    margin: 0 auto;
    column-count: 2;
    column-gap: 2em;
    column-rule: 1px solid oklch(0.929 0.013 255.508);
}

/* Ensure these elements don't break across columns */
.book-title, .introductory-material {
    column-span: all;      /* Make headings span across all columns */
}

.book-title {
    font-size: 14pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1em;
}

.book-title ~ .section-heading,
.introductory-material ~ .section-heading,
.book-title ~ .paragraph,
.introductory-material ~ .paragraph {
    margin-top: 0;
}

.chapter-number {
    font-size: 16pt;
    font-weight: bold;
    margin: 0 0.2em;
    float: left;
}

.paragraph {
    text-indent: 1.5em;
    margin-bottom: 0.5em;
    text-align: justify;
}

.paragraph.suppress-indent {
    text-indent: 0;
}

.section-heading {
    font-size: 9pt;
    font-weight: bold;
    margin-top: 1em;
    margin-bottom: 0.5em;
    text-indent: 0;
}

.poetry-q1 {
    margin-left: 1.5em;
    text-indent: 0;
}

.paragraph ~ .poetry-q1,
.poetry-q1 ~ .poetry-q2,
.poetry-q2 ~ .poetry-q1 {
    margin-top: -0.5em;
}

.poetry-q2 {
    margin-left: 2.5em;
    text-indent: 0;
}

.verse-number {
    font-size: 6pt;
    color: oklch(0.546 0.245 262.881);
    font-weight: bold;
    vertical-align: super;
    margin-right: 0.2em;
}

.divine-name {
    font-variant: small-caps;
}

.blank-line {
    height: 0.8em;
}

.side-note {
    display: none;
}

/* Prevent orphans and widows */
p {
    orphans: 2;
    widows: 2;
}
"""


def get_edge_css(header=""):
    header_css = ""
    if header:
        escaped_header = header.replace("'", "\\'").replace('"', '\\"')
        header_css = f"""
            @top-center {{
                content: "{escaped_header}";
                font-family: Noto Serif, serif;
                font-weight: bold;
                font-size: 9pt;
                color: oklch(0.554 0.046 257.417);
            }}
        """

    return f"""    
    /* First page styles */
    @page:first {{
        size: letter;
        margin: 1in;

        {header_css}

        /* Remove top-right page number on first page */
        @top-right {{
            content: "";
        }}

        /* Add page number at bottom center of first page */
        @bottom-center {{
            content: counter(page);
            font-family: Noto Serif, serif;
            font-size: 9pt;
            color: oklch(0.208 0.042 265.755);
        }}
    }}

    @page {{
        size: letter;
        margin: 1in;

        {header_css}
        
        /* Add page number at top right */
        @top-right {{
            content: counter(page);
            font-family: Noto Serif, serif;
            font-size: 9pt;
        }}
    }}
    """


def generate_css(header=""):
    """Generate CSS for styling the HTML content."""
    # Prepare header CSS based on whether a header was provided

    return get_edge_css(header) + main_css
