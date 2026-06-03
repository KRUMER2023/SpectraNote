from docx import Document
import os

def create_docx(full_path):
    """
    Create an empty .docx at `path`, set current_doc/current_path and return Document.
    """
    folder = os.path.dirname(full_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    doc = Document()
    doc.save(full_path)

def open_docx(app_data):
    """
    Open an existing docx and return the Document object.
    If path is None, uses data (folder + dname). Raises on missing file.
    Also sets current_doc/current_path.
    """
    # fetching the file name and folder loc. 
    file = app_data.get_file_name()
    folder = app_data.get_folder_path()

    if not os.path.isfile(f"{folder}/{file}"):
        raise FileNotFoundError(f"{folder}/{file} does not exist.")

    doc = Document(f"{folder}/{file}")
    return doc
