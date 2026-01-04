# gui_runner.py

import tkinter as tk
from tkinter import Button, Canvas
import ctypes
import os


class SpectraToolbar:
    """
    Creates the floating SpectraNote toolbar using preloaded resources
    from gui_loader.py and stores user button clicks into AppData.
    """

    def __init__(self, app_data):
        self.app_data = app_data
        resources = app_data.ui_resources

        # self.images = resources["images"]
        # load PhotoImage objects HERE (correct root)
        self.images = {
            key: tk.PhotoImage(file=path)
            for key, path in self.app_data.ui_resources["paths"].items()
        }


        self.positions = resources["positions"]
        self.layout = resources["layout"]

        # -----------------------------
        # Root Window
        # -----------------------------
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "#000000")
        self.root.wm_attributes("-topmost", True)

        # Dynamic window size
        self.width = self.layout["width"]
        self.height = self.layout["height"]

        self.root.geometry(f"{self.width}x{self.height}")

        # Place at top-center
        scr_w = self.layout["screen_w"]
        x = (scr_w - self.width) // 2
        self.root.geometry(f"+{x}+0")

        # Windows-specific: Prevent window from taking focus
        try:
            if 'win' in self.root.tk.call('tk', 'windowingsystem').lower():
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                GWL_EXSTYLE = -20
                WS_EX_NOACTIVATE = 0x08000000
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE)
        except:
            pass

        # Canvas (transparent)
        self.canvas = Canvas(
            self.root,
            bg="#000000",
            width=self.width,
            height=self.height,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.place(x=0, y=0)

        self.scale = self.layout["scale"]

        # -----------------------------
        # Main Images: Center BG + Drag Icon
        # -----------------------------
        self.bg_circle = self.canvas.create_image(
            self.width / 2,
            self.height / 2,
            image=self.images["bg_circle"]
        )

        self.drag_icon = self.canvas.create_image(
            self.width / 2,
            self.height / 2,
            image=self.images["drag_icon"]
        )

        # Enable drag
        self.canvas.tag_bind(self.drag_icon, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.drag_icon, "<B1-Motion>", self.do_drag)

        # -----------------------------
        # Button Groups (Left & Right Panels)
        # -----------------------------
        self.left_buttons = []
        self.right_buttons = []

        self.create_all_buttons()

    # =====================================================================
    # Create All Buttons
    # =====================================================================
    def create_all_buttons(self):
        """
        Creates all toolbar buttons using the positions+images from loader.
        """

        # -----------------------------
        # Right Panel Buttons (Exit, bullet, h1, h2, bold, italic, normal)
        # -----------------------------
        right_list = [
            ("exit",      lambda: self.press_and_quit()),
            ("bullet",    lambda: self.save_state("bullet")),
            ("h2",        lambda: self.save_state("h2")),
            ("h1",        lambda: self.save_state("h1")),
            ("bold",      lambda: self.save_state("bold")),
            ("italic",    lambda: self.save_state("italic")),
            ("normal",    lambda: self.save_state("normal")),
        ]

        for key, callback in right_list:
            x, y = self.positions[key]
            img = self.images[key]
            btn = Button(
                self.root,
                image=img,
                borderwidth=0,
                highlightthickness=0,
                command=callback,
                relief="flat",
            )
            btn.place(x=x, y=y, width=42*self.scale, height=46*self.scale)
            self.right_buttons.append(btn)

        # -----------------------------
        # Left Panel Buttons (folder, file, chatbot, summary...)
        # -----------------------------
        left_list = [
            ("folder",     lambda: self.open_folder()),
            ("file",       lambda: self.open_file()),
            ("chatbot",    lambda: print("Chatbot Feature (coming soon)")),
            ("summary",    lambda: print("Summarizer (coming soon)")),
            ("translator", lambda: print("Translator (coming soon)")),
            ("search",     lambda: print("Search (coming soon)")),
            ("youtube",    lambda: self.save_state("YT")),
        ]

        for key, callback in left_list:
            x, y = self.positions[key]
            img = self.images[key]
            btn = Button(
                self.root,
                image=img,
                borderwidth=0,
                highlightthickness=0,
                command=callback,
                relief="flat",
            )
            btn.place(x=x, y=y, width=42*self.scale, height=46*self.scale)
            self.left_buttons.append(btn)

        # -----------------------------
        # Toggle Buttons
        # -----------------------------
        toggle_left_pos = self.positions["toggle_left"]
        toggle_right_pos = self.positions["toggle_right"]

        self.toggle_left_btn = Button(
            self.root,
            image=self.images["toggle_left"],
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            command=self.toggle_right_panel  # right panel hides/shows
        )
        self.toggle_left_btn.place(
            x=toggle_left_pos[0],
            y=toggle_left_pos[1],
            width=23*self.scale,
            height=30*self.scale
        )

        self.toggle_right_btn = Button(
            self.root,
            image=self.images["toggle_right"],
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            command=self.toggle_left_panel  # left panel
        )
        self.toggle_right_btn.place(
            x=toggle_right_pos[0],
            y=toggle_right_pos[1],
            width=23*self.scale,
            height=30*self.scale
        )

        # Start with panels hidden
        self.right_panel_visible = False
        self.left_panel_visible = False

        self.hide_right_panel()
        self.hide_left_panel()

    # =====================================================================
    # Toggle Panels
    # =====================================================================
    def toggle_left_panel(self):
        if self.left_panel_visible:
            self.hide_left_panel()
        else:
            self.show_left_panel()

    def toggle_right_panel(self):
        if self.right_panel_visible:
            self.hide_right_panel()
        else:
            self.show_right_panel()

    def show_left_panel(self):
        for btn in self.left_buttons:
            btn.place_configure()
        self.left_panel_visible = True

    def hide_left_panel(self):
        for btn in self.left_buttons:
            btn.place_forget()
        self.left_panel_visible = False

    def show_right_panel(self):
        for btn in self.right_buttons:
            btn.place_configure()
        self.right_panel_visible = True

    def hide_right_panel(self):
        for btn in self.right_buttons:
            btn.place_forget()
        self.right_panel_visible = False

    # =====================================================================
    # Drag Support
    # =====================================================================
    def start_drag(self, event):
        self.drag_offset_x = event.x_root - self.root.winfo_x()

    def do_drag(self, event):
        x = event.x_root - self.drag_offset_x
        screen_w = self.layout["screen_w"]
        x = max(0, min(x, screen_w - self.width))
        self.root.geometry(f"+{int(x)}+0")

    # =====================================================================
    # Button Actions
    # =====================================================================
    def save_state(self, state):
        """Save which button was pressed."""
        self.app_data.set_style(state)
        self.root.destroy()

    def press_and_quit(self):
        self.app_data.set_style("Exit")
        self.root.destroy()

    def open_folder(self):
        folder = self.app_data.get_folder_path()
        if folder and os.path.exists(folder):
            os.startfile(folder)

    def open_file(self):
        path = self.app_data.get_full_path()
        if path and os.path.exists(path):
            os.startfile(path)

    # =====================================================================
    # Mainloop
    # =====================================================================
    def run(self):
        self.root.mainloop()



from gui_loader import ImageLoader
from gui_layout import Layout
from appdata import AppData


layout = Layout()

troot = tk.Tk()
troot.withdraw()
images = ImageLoader()
appdata = AppData()
appdata.set_file_name("newSpectraNote.docx")
appdata.set_folder_path("E:/Testing/")
app = SpectraToolbar(appdata,images, layout, troot)
app.run()


