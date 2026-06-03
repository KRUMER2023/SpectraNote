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
        
        # Panel toogle flags
        self.Toogle_left = False
        self.Toogle_right = False

    # ---------- setters ----------
    def set_file_name(self, name): 
        self.file_name = name
    def set_folder_path(self, path): 
        self.folder_path = path
    def set_style(self, style): 
        self.style = style
        
    def set_Toogle_left(self, state):
        self.Toogle_left = state
    def set_Toogle_right(self, state):
        self.Toogle_right = state

    # ---------- getters ----------
    def get_file_name(self): 
        return self.file_name
    def get_folder_path(self): 
        return self.folder_path
    def get_style(self): 
        return self.style
        
    def get_Toogle_left(self):
        return self.Toogle_left
    def get_Toogle_right(self):
        return self.Toogle_right

    def get_file_path(self):
        return self.folder_path + "/" + self.file_name