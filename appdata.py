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
        
        # Panel toggle flags
        self.toggle_left = False
        self.toggle_right = False

    # ---------- setters ----------
    def set_file_name(self, name): 
        self.file_name = name
    def set_folder_path(self, path): 
        self.folder_path = path
    def set_style(self, style): 
        self.style = style
        
    def set_toggle_left(self, state):
        self.toggle_left = state
    def set_toggle_right(self, state):
        self.toggle_right = state

    # ---------- getters ----------
    def get_file_name(self): 
        return self.file_name
    def get_folder_path(self): 
        return self.folder_path
    def get_style(self): 
        return self.style
        
    def get_toggle_left(self):
        return self.toggle_left
    def get_toggle_right(self):
        return self.toggle_right

    def get_file_path(self):
        return self.folder_path + "/" + self.file_name