from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import requests
import tkinter as tk
from tkinter import messagebox, Checkbutton, IntVar, Button, Label, Frame

API_KEY = "AIzaSyD2UddlwYVCVZD6_jTeAxE3SY5gsNwSvaQ"  # Replace with your API key or use os.getenv('YOUTUBE_API_KEY')
BASE_URL = "https://www.googleapis.com/youtube/v3/search"

def add_hyperlink(paragraph, url, text):
    """
    Add a hyperlink to a paragraph.
    
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
    color.set(qn('w:val'), '0000FF')  # Blue color
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

def fetch_yt_suggestions(query: str, max_results: int = 4):
    """Fetch top 4 YouTube video suggestions for the query."""
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'relevance',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise ValueError(f"API error: {response.text}")
    data = response.json()
    if 'error' in data:
        raise ValueError(f"API error: {data['error']['message']}")
    return data.get('items', [])

def show_yt_selector(app_data, items, original_query: str):
    """Popup to select videos with checkboxes and action buttons."""
    root = tk.Toplevel()
    root.title("YouTube Suggestions")
    root.geometry("400x300")
    root.resizable(False, False)

    vars_ = []
    video_map = {}
    frame = Frame(root)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    for i, item in enumerate(items):
        title = item['snippet']['title'][:50] + "..." if len(item['snippet']['title']) > 50 else item['snippet']['title']
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        var = IntVar()
        vars_.append(var)
        Checkbutton(frame, text=title, variable=var).grid(row=i, column=0, sticky="w")
        video_map[title] = (title, url)

    def add_selected_to_doc():
        selected = [i for i, var in enumerate(vars_) if var.get()]
        if not selected:
            messagebox.showwarning("No Selection", "No videos selected!")
            return
        insert_yt_to_docx(app_data, [video_map[items[i]['snippet']['title'][:50] + "..." if len(items[i]['snippet']['title']) > 50 else items[i]['snippet']['title']][1] for i in selected], original_query, all=False)
        root.destroy()

    def add_all_to_doc():
        urls = [video_map[items[i]['snippet']['title'][:50] + "..." if len(items[i]['snippet']['title']) > 50 else items[i]['snippet']['title']][1] for i in range(len(items))]
        insert_yt_to_docx(app_data, urls, original_query, all=True)
        root.destroy()

    Button(root, text="ASTD (Add Selected To Doc)", command=add_selected_to_doc).pack(pady=5)
    Button(root, text="AATD (Add All To Doc)", command=add_all_to_doc).pack(pady=5)

    # root.mainloop()
    root.wait_window() # using this as thr root is obj with Toplevel not Tk

def insert_yt_to_docx(app_data, urls: list, original_query: str, all: bool):
    """Add selected/all YT links as bullets in the current DOCX."""
    path = app_data.get_folder_path()  + "/" + app_data.get_file_name()
    if not path:
        raise ValueError("No DOCX open!")
    doc = Document(path)
    p = doc.add_paragraph(f"YouTube Suggestions for '{original_query}':", style="Heading 2")
    p.paragraph_format.space_after = 0
    for url in urls:
        p = doc.add_paragraph("", style="List Bullet")
        add_hyperlink(p, url, "Watch Video")
        p.paragraph_format.left_indent = Inches(0.5)
    doc.save(path)
    messagebox.showinfo("Success", f"Added {'all' if all else 'selected'} YT suggestions to notes!")

def handle_yt_from_text(app_data, text):
    """Main handler: Fetch and show suggestions."""
    if not text.strip():
        messagebox.showwarning("No Text", "Select text first!")
        return
    try:
        items = fetch_yt_suggestions(text)
        if not items:
            messagebox.showinfo("No Results", "No YT suggestions found.")
            return
        show_yt_selector(app_data, items, text)
    except Exception as e:
        messagebox.showerror("YT Error", f"Failed to fetch suggestions: {e}")

# if __name__ == "__main__":
#     handle_yt_from_text("Python tutorials")