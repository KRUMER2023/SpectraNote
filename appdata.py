# appdata.py

# Lightweight global state holder for SpectraNote.
# Stores:
    # - file name
    # - folder path
    # - selected style

class AppData:
    def __init__(self):

        # User-selected file info
        self.file_name = ""
        self.folder_path = ""
        self.style = ""

    # ---------- setters ----------
    def set_file_name(self, name): 
        self.file_name = name
    def set_folder_path(self, path): 
        self.folder_path = path
    def set_style(self, style): 
        self.style = style

    # ---------- getters ----------
    def get_file_name(self): 
        return self.file_name
    def get_folder_path(self): 
        return self.folder_path
    def get_style(self): 
        return self.style

    def get_file_path(self):
        return self.folder_path + "/" + self.file_name