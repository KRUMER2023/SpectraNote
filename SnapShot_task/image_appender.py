import os
from docx import Document
from docx.shared import Inches

def append_image_to_doc(image_path: str, doc_path: str):
    """
    Appends the image at image_path to the Word document at doc_path.
    Creates the document if it doesn't exist.
    Scales the image to fit within standard page margins (approx 6 inches width)
    if it is too large.
    """
    try:
        # Check if document exists, load or create
        if os.path.exists(doc_path):
            try:
                doc = Document(doc_path)
            except Exception:
                # If file exists but is corrupt or not a valid docx (e.g. 0 bytes),
                # print warning and create new
                print(f"Warning: Could not open {doc_path}. Creating new document.")
                doc = Document()
        else:
            doc = Document()

        # Add a new paragraph for the image
        p = doc.add_paragraph()
        run = p.add_run()
        
        # Add picture. 
        # docx.add_picture auto-calculates height if width is specified.
        # We start by adding it with native size to check dimensions or just default to width=6 inches 
        # for consistency if it's a large screenshot.
        
        # A robust way to "scale if too big" without opening the image twice:
        # Just use docx's add_picture. If we want to constrain width to page size (e.g. 6 inches),
        # we can just set width=Inches(6). This might upscale small images though.
        # Better approach: Let's assume screenshots are usually large (full screen/regions).
        # We can enforce a max width of 6 inches.
        
        # Custom Logic: check image width.
        # If > 6 inches, scale to 6 inches. Else keep original.
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                width_px, _ = img.size
                dpi = img.info.get('dpi', (96, 96))[0]
                width_inches = width_px / dpi
                
            if width_inches > 6.0:
                 run.add_picture(image_path, width=Inches(6))
            else:
                 run.add_picture(image_path)
        except Exception:
             # Fallback if PIL fails
             run.add_picture(image_path, width=Inches(6))

        doc.save(doc_path)
        print(f"Successfully appended {image_path} to {doc_path}")
        return True, "Success"

    except Exception as e:
        error_msg = f"Error appending image to document: {e}"
        print(error_msg)
        return False, str(e)
