# gui_loader.py

from tkinter import PhotoImage
from pathlib import Path

class ImageLoader:

    def asset(self,path: str) -> Path:
        """Helper: return full asset path."""
        return self.ASSETS_PATH / path

    def __init__(self):

        # Base path: gui/assets/frame0/
        self.ASSETS_PATH = Path(__file__).parent / "assets" / "frame0"

        self.image_bg_circle = PhotoImage(file=self.asset("image_5.png"))
        self.image_drag_icon = PhotoImage(file=self.asset("image_6.png"))

        # Panel background images
        self.image_panel_left_1 = PhotoImage(file=self.asset("image_1.png"))
        self.image_panel_left_2 = PhotoImage(file=self.asset("image_2.png"))
        self.image_panel_right_1 = PhotoImage(file=self.asset("image_3.png"))
        self.image_panel_right_2 = PhotoImage(file=self.asset("image_4.png"))

        # Toggle arrows
        self.image_toggle_left = PhotoImage(file=self.asset("button_16.png"))
        self.image_toggle_right = PhotoImage(file=self.asset("button_15.png"))

        # Right panel buttons
        self.image_exit =  PhotoImage(file=self.asset("button_8.png"))
        self.image_bullet =  PhotoImage(file=self.asset("button_9.png"))
        self.image_h2 = PhotoImage(file=self.asset("button_10.png"))
        self.image_h1 = PhotoImage(file=self.asset("button_11.png"))
        self.image_bold = PhotoImage(file=self.asset("button_12.png"))
        self.image_italic = PhotoImage(file=self.asset("button_13.png"))
        self.image_normal = PhotoImage(file=self.asset("button_14.png"))

        # Left panel buttons
        self.image_folder =  PhotoImage(file=self.asset("button_7.png"))
        self.image_file =  PhotoImage(file=self.asset("button_6.png"))
        self.image_chatbot =  PhotoImage(file=self.asset("button_5.png"))
        self.image_summary =  PhotoImage(file=self.asset("button_4.png"))
        self.image_translator =  PhotoImage(file=self.asset("button_3.png"))
        self.image_search =  PhotoImage(file=self.asset("button_2.png"))
        self.image_youtube =  PhotoImage(file=self.asset("button_1.png"))

        self.images ={

            # toggler
            "toggle_left":      self.image_toggle_left,
            "toggle_right":     self.image_toggle_right,
            
            "main_bg":          self.image_bg_circle,
            "icon":             self.image_drag_icon,
            
            # right panel
            "exit":             self.image_exit,
            "bullet":           self.image_bullet,
            "h2":               self.image_h2,
            "h1":               self.image_h1,
            "bold":             self.image_bold,
            "italic":           self.image_italic,
            "normal":           self.image_normal,
            
            "right_bg_bg":      self.image_panel_right_1,
            "right_line_bg":    self.image_panel_right_2,
            
            
            # left panel
            "folder":           self.image_folder,
            "file":             self.image_file,
            "chatbot":          self.image_chatbot,
            "summary":          self.image_summary,
            "translator":       self.image_translator,
            "search":           self.image_search,
            "youtube":          self.image_youtube,
            
            "left_bg_bg":       self.image_panel_left_1,
            "left_line_bg":     self.image_panel_left_2
        }

        