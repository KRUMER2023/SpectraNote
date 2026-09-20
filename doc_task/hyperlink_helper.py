from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

def add_hyperlink(paragraph, url: str, text: str):
    """
    Add a clickable hyperlink to a python-docx paragraph.
    
    :param paragraph: The paragraph to add the hyperlink to.
    :param url: The URL for the hyperlink.
    :param text: The display text for the hyperlink.
    """
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '1D4ED8')  # Clean modern blue (#1D4ED8)
    rPr.append(color)
    underline = OxmlElement('w:u')
    underline.set(qn('w:val'), 'single')  # Single underline
    rPr.append(underline)
    
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    r.append(t)
    
    hyperlink.append(r)
    paragraph._p.append(hyperlink)


def append_yt_links_to_doc(app_data, video_entries: list, original_query: str):
    """
    Append YouTube suggestions in the requested structured format:
    
    YouTube Suggestions for 'QUERY': (Bold, Normal style)
    - VIDEO_TITLE   ||  CHANNEL_NAME
        URL
    - VIDEO_TITLE   ||  CHANNEL_NAME
        URL
    """
    file = app_data.get_file_name()
    folder = app_data.get_folder_path()
    path = f"{folder}/{file}"
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Document not found at: {path}")

    doc = Document(path)

    # 1. Header (Bold, Normal paragraph, not H1/H2)
    p_header = doc.add_paragraph(style="Normal")
    p_header.paragraph_format.space_before = Pt(6)
    p_header.paragraph_format.space_after = Pt(3)
    run_header = p_header.add_run(f"YouTube Suggestions for '{original_query}':")
    run_header.bold = True

    # 2. Video Entries
    for item in video_entries:
        if isinstance(item, dict):
            url = item.get("url", "")
            title = item.get("title", url)
            channel = item.get("channel", "")
        else:
            url = str(item)
            title = url
            channel = ""

        if not url:
            continue

        # Line 1: - VIDEO_TITLE   ||  CHANNEL_NAME
        p_title = doc.add_paragraph(style="Normal")
        p_title.paragraph_format.left_indent = Inches(0.2)
        p_title.paragraph_format.space_before = Pt(3)
        p_title.paragraph_format.space_after = Pt(1)

        run_dash = p_title.add_run("- ")
        run_dash.bold = True

        run_title = p_title.add_run(f"{title}")
        run_title.bold = True

        if channel:
            run_sep = p_title.add_run("   ||   ")
            run_sep.bold = False
            run_channel = p_title.add_run(f"{channel}")
            run_channel.bold = False

        # Line 2: Indented clickable URL
        p_url = doc.add_paragraph(style="Normal")
        p_url.paragraph_format.left_indent = Inches(0.45)
        p_url.paragraph_format.space_before = Pt(0)
        p_url.paragraph_format.space_after = Pt(4)

        add_hyperlink(p_url, url, url)

    doc.save(path)
