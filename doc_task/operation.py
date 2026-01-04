from . import doc_manager

# --- helper to clean and split text into paragraphs ---
def _prepare_text(text: str):
    # 1. Strip leading/trailing whitespace/newlines
    text = text.strip()
    # 2. Split into lines, skipping completely empty lines
    lines = [line for line in text.splitlines() if line.strip()]
    return lines

# --- style functions ---
def add_normal(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(line, style="Normal")
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

def add_h1(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(line, style="Heading 1")
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

def add_h2(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(line, style="Heading 2")
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

def add_bold(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(style="Normal")
        run = p.add_run(line)
        run.bold = True
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

def add_italic(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(style="Normal")
        run = p.add_run(line)
        run.italic = True
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

def add_underline(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(style="Normal")
        run = p.add_run(line)
        run.underline = True
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

def add_bullet(doc, text: str):
    for line in _prepare_text(text):
        p = doc.add_paragraph(line, style="List Bullet")
        p.paragraph_format.space_before = 0
        p.paragraph_format.space_after = 0

# --- dispatcher map ---
STYLE_FUNCTIONS = {
    "normal": add_normal,
    "h1": add_h1,
    "h2": add_h2,
    "bold": add_bold,
    "italic": add_italic,
    "underline": add_underline,
    "bullet": add_bullet,
}

def apply_operation(app_data , text, style):
    """
    Open the current doc (from saveNames if not opened), apply style, save doc.
    """
    if not text or not text.strip():
        raise ValueError("Empty text provided to apply_operation.")

    # open the document
    doc = doc_manager.open_docx(app_data)   # may raise FileNotFoundError

    # get the function and call it
    func = STYLE_FUNCTIONS.get(style, add_normal)
    func(doc, text)

    # save changes
    full_path = app_data.get_folder_path() +"/" + app_data.get_file_name()
    doc.save(full_path)
