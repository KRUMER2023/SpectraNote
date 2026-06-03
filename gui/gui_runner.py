import tkinter as tk
from tkinter import Button, Canvas
import ctypes
import os

class SpectraToolbar:

    def __init__(self, app_data, loader, layout, troot):

        self.app_data = app_data
        self.loader = loader
        self.layout = layout

        self.width = layout.measurements["width"]
        self.height = layout.measurements["height"]
        self.screen_w = layout.measurements["screen_w"]
        self.screen_h = layout.measurements["screen_h"]
        self.scale = layout.measurements["scale"]
        self.base_w = layout.measurements["base_width"]
        self.base_h = layout.measurements["base_height"]


        # layout positions
        self.toogler_positions = layout.positions["Toogler"]
        self.left_positions = layout.positions["Left_panel"]
        self.right_positions = layout.positions["Right_panel"]

        self.root = self._build_window(troot)

        self.canvas = self._build_canvas()


        # storing UI elements
        self.main_bg_items = []
        self.left_objs = {"bg": {}, "button": {}}
        self.right_objs = {"bg": {}, "button": {}}
        self.toggle_buttons = {}

        # Created dictionary of actions (LIKE app.py)
        self.actions = {
            # toggle buttons
            "toggle_left":      self.toggle_left_panel,
            "toggle_right":     self.toggle_right_panel,

            # Right-panel formatting buttons
            "exit":             lambda: self._exit_toolbar(),
            "bullet":           lambda: self._extract_and_close("bullet"),
            "h2":               lambda: self._extract_and_close("h2"),
            "h1":               lambda: self._extract_and_close("h1"),
            "bold":             lambda: self._extract_and_close("bold"),
            "italic":           lambda: self._extract_and_close("italic"),
            "normal":           lambda: self._extract_and_close("normal"),

            # Left-panel utility buttons
            "folder":           lambda: self.open_folder(self.app_data.get_folder_path()),
            "file":             lambda: self.open_file(self.app_data.get_file_path()),
            "chatbot":          lambda: print("chatbot"),
            "summary":          lambda: self._extract_and_close("summary"),
            "translator":       lambda: self._extract_and_close("translator"),
            "snapshot":           lambda: self._extract_and_close("snapshot"),
            "youtube":          lambda: self._extract_and_close("YT"),
        }

        
        # ----------------------------------------------------------------
        # Enable high dpi for clear gui
        # ----------------------------------------------------------------
        from ctypes import windll
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            windll.user32.SetProcessDPIAware()



        # BUILD UI
        self.create_main_background()

        self.create_toggler_buttons()

        self.create_left_panel()

        self.create_right_panel()


        for obj in self.main_bg_items:
            self.canvas.tag_raise(obj)
            

        if self.app_data.get_Toogle_left():
            # simulate toggle left
            # trick: to run it successfully, ensure last btn is hidden so it expands
            self.toggle_left_panel()

        if self.app_data.get_Toogle_right():
            self.toggle_right_panel()

        self.enable_dragging()

    # -------------------------------------------------------------------------
    def _build_window(self, troot):
        win = tk.Toplevel(troot)
        center_x = int((self.screen_w - self.width) / 2)
        win.geometry(f"{self.width}x{self.height}+{center_x}+0")
        win.overrideredirect(True)
        win.wm_attributes("-transparentcolor", "#D9D9DA")
        win.wm_attributes("-topmost", True)

        try:
            if "win" in win.tk.call('tk', 'windowingsystem').lower():
                hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
                GWL_EXSTYLE = -20
                WS_EX_NOACTIVATE = 0x08000000
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE,
                                                    style | WS_EX_NOACTIVATE)
        except:
            print("[INFO] Couldn't apply no-focus mode")
        return win

    # -------------------------------------------------------------------------
    def _build_canvas(self):
        canvas = Canvas(
            self.root,
            bg="#D9D9DA",
            width=self.width,
            height=self.height,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )


        canvas.place(x=0, y=0)
       
        return canvas

    # -------------------------------------------------------------------------
    # MAIN CENTER BACKGROUND
    # -------------------------------------------------------------------------
    def create_main_background(self):
        for name in self.toogler_positions["bg"].keys():
            if name == "trans_bg":
                continue
            img = self.canvas.create_image(
                self.width / 2,
                self.height / 2,
                image=self.loader.images[name]
            )
            self.main_bg_items.append(img)

    # -------------------------------------------------------------------------
    # TOGGLER BUTTONS
    # -------------------------------------------------------------------------
    def create_toggler_buttons(self):
        for name, pos in self.toogler_positions["button"].items():
            x, y = pos
            btn = Button(
                self.root,
                image=self.loader.images[name],
                borderwidth=0,
                highlightthickness=0,
                relief="flat",
                command=self.actions[name]     # map button to its action
            )
            btn.place(x=x, y=y, width=23*self.scale, height=30*self.scale)
            self.toggle_buttons[name] = btn

    # -------------------------------------------------------------------------
    # LEFT PANEL
    # -------------------------------------------------------------------------
    def create_left_panel(self):

        # left panel bg
        for name, (x, _) in self.left_positions["bg"].items():
            img = self.canvas.create_image(
                self.width * x / self.base_w,
                self.height / 2,
                image=self.loader.images[name],
                state="hidden"
            )
            self.left_objs["bg"][name] = img


        # left panel buttons
        for name, (x, y) in self.left_positions["button"].items():
            btn = Button(
                self.root,
                image=self.loader.images[name],
                borderwidth=0,
                command=self.actions[name]      # map button to its action
            )
            self.left_objs["button"][name] = btn

    # -------------------------------------------------------------------------
    # RIGHT PANEL
    # -------------------------------------------------------------------------
    def create_right_panel(self):
        
        # right panel bg
        for name, (x, _) in self.right_positions["bg"].items():
            img = self.canvas.create_image(
                self.width * x / self.base_w,
                self.height / 2,
                image=self.loader.images[name],
                state="hidden"
            )
            self.right_objs["bg"][name] = img

        

        # right panel buttons
        for name, (x, y) in self.right_positions["button"].items():
            btn = Button(
                self.root,
                image=self.loader.images[name],
                borderwidth=0,
                command=self.actions[name]      # map button to its action
            )
            self.right_objs["button"][name] = btn


    # -------------------------------------------------------------------------
    # PANEL TOGGLE
    # -------------------------------------------------------------------------
    def toggle_left_panel(self):
        keys = list(self.left_objs["button"].keys())
        last_btn = self.left_objs["button"][keys[-1]]

        if last_btn.winfo_ismapped():
            self.toggle_buttons["toggle_left"].configure(
                image=self.loader.images["toggle_left"]
            )
            for b in self.left_objs["button"].values(): b.place_forget()
            for bg in self.left_objs["bg"].values():
                self.canvas.itemconfigure(bg, state="hidden")
            self.app_data.set_Toogle_left(False)
        else:
            self.toggle_buttons["toggle_left"].configure(
                image=self.loader.images["toggle_right"]
            )
            for name, img in self.left_objs["bg"].items():
                self.canvas.itemconfigure(img, state="normal")

            for name, (x, y) in self.left_positions["button"].items():
                self.left_objs["button"][name].place(
                    x=x*self.scale, y=y*self.scale,
                    width=42*self.scale, height=46*self.scale
                )
            self.app_data.set_Toogle_left(True)

    def toggle_right_panel(self):
        keys = list(self.right_objs["button"].keys())
        last_btn = self.right_objs["button"][keys[-1]]

        if last_btn.winfo_ismapped():
            self.toggle_buttons["toggle_right"].configure(
                image=self.loader.images["toggle_right"]
            )
            for b in self.right_objs["button"].values(): b.place_forget()
            for bg in self.right_objs["bg"].values():
                self.canvas.itemconfigure(bg, state="hidden")
            self.app_data.set_Toogle_right(False)
        else:
            self.toggle_buttons["toggle_right"].configure(
                image=self.loader.images["toggle_left"]
            )
            for name, img in self.right_objs["bg"].items():
                self.canvas.itemconfigure(img, state="normal")

            for name, (x, y) in self.right_positions["button"].items():
                self.right_objs["button"][name].place(
                    x=x*self.scale, y=y*self.scale,
                    width=42*self.scale, height=46*self.scale
                )
            self.app_data.set_Toogle_right(True)

    # -------------------------------------------------------------------------
    # DRAGGING (Copied from gui_main_circle.py with same calculations)
    # -------------------------------------------------------------------------
    def enable_dragging(self):

        # same dynamic center offset
        self.IMAGE_2_X = self.width / 2
        self.FULL_WIDTH = self.width

        # -----------------------------
        # get_min_x (SAME as gui_main_circle)
        # -----------------------------
        def get_min_x(left_panel_visible):
            if left_panel_visible:
                return 0
            else:
                return -self.IMAGE_2_X   # shift half-width left

        # -----------------------------
        # get_max_x (SAME as gui_main_circle)
        # -----------------------------
        def get_max_x(right_panel_visible):
            screen_width = self.screen_w
            if right_panel_visible:
                return screen_width - self.FULL_WIDTH
            else:
                return screen_width - self.IMAGE_2_X

        # -----------------------------
        # Start dragging — store offset
        # -----------------------------
        def start_drag(event):
            self.drag_offset_x = event.x_root - self.root.winfo_x()

        # -----------------------------
        # Drag movement — apply limits
        # -----------------------------
        def do_drag(event):
            x = event.x_root - self.drag_offset_x

            # detect visibility just like gui_main_circle
            left_panel_visible = self.left_objs["button"]["folder"].winfo_ismapped()
            right_panel_visible = self.right_objs["button"]["exit"].winfo_ismapped()

            # compute bounds
            min_x = get_min_x(left_panel_visible)
            max_x = get_max_x(right_panel_visible)

            # clamp x inside the allowed range
            x = max(min_x, min(x, max_x))

            self.root.geometry(f"+{int(x)}+0")

        # -----------------------------
        # Bind dragging ONLY on center-drag-image (same behavior as gui_main_circle)
        # -----------------------------
        # In  main_bg_items[1] = the small drag icon
        self.canvas.tag_bind(self.main_bg_items[1], "<ButtonPress-1>", start_drag)
        self.canvas.tag_bind(self.main_bg_items[1], "<B1-Motion>", do_drag)


    # -------------------------------------------------------------------------
    # ACTION HELPERS
    # -------------------------------------------------------------------------
    
    # -----------------------------
    # Method for opening the present note folder
    # -----------------------------
    def open_folder(self, folder_path):
        """Open the folder containing the current notes DOCX."""
        
        if folder_path and os.path.exists(folder_path):
            if os.path.exists(folder_path):
                os.startfile(folder_path)  # Opens folder in default file explorer (Windows)
            else:
                tk.messagebox.showwarning("Folder Error", "Notes folder not found!")
        else:
            tk.messagebox.showwarning("No File", "No notes file currently open!")

    # -----------------------------
    # Method for opening the present note file
    # -----------------------------
    def open_file(self, file_path):
        if file_path and os.path.exists(file_path):
            os.startfile(file_path)
        else:
            tk.messagebox.showwarning("No File", "No notes file currently open!")


    def _extract_and_close(self, style):
        self.app_data.set_style(style)
        self.root.destroy()

    def _exit_toolbar(self):
        self.app_data.set_style("Exit")
        self.root.destroy()

    # -------------------------------------------------------------------------
    def run(self):
        # self.root.mainloop()
        self.root.wait_window() # using this as thr root is obj with Toplevel not Tk

