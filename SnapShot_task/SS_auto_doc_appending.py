import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, messagebox, Toplevel
from pathlib import Path
from PIL import Image, ImageGrab, ImageDraw
import sys
# import os
import datetime
# import time
from ctypes import windll
from . import image_appender  # Custom module for Word appending

# --- DPI Configuration ---
try:
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    windll.user32.SetProcessDPIAware()

# --- Assets Helper ---
ASSETS_PATH = Path(__file__).parent / "assets" / "frame0"
def get_asset(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ModernSnippingTool:
    def __init__(self, fld_path, fl_name):
        self.fld_path = fld_path
        self.fl_name = fl_name
        self.file_path = fld_path + '/' + fl_name

        self.root = Toplevel()
        self._setup_main_window()
        
        # --- State Variables ---
        self.snip_mode = None  # 'rect', 'circle', 'free'
        self.start_pos = (0, 0)
        self.current_pos = (0, 0)
        self.free_draw_points = []
        self.original_screenshot = None
        
        # --- UI Storage ---
        # We only keep this list to prevent Python from deleting images from memory
        self._images_cache = [] 
        
        # --- Build UI ---
        self._build_toolbar()

    def _setup_main_window(self):

        """Sets up the transparent floating toolbar properties."""
        # root already initialized as class variable
        self.root.title("Snipping Tool")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "#000000")
        self.root.wm_attributes("-topmost", True)
        
        # Geometry
        w, h = 253, 73
        x = (self.root.winfo_screenwidth() - w) // 2
        self.root.geometry(f"{w}x{h}+{x}+0")

    def _build_toolbar(self):
        """Creates the Figma-style UI using a loop for efficiency."""
        # Background
        canvas = Canvas(self.root, bg="#000000", height=73, width=253, bd=0, highlightthickness=0)
        canvas.place(x=0, y=0)
        
        bg_img = PhotoImage(file=get_asset("image_1.png"))
        self._images_cache.append(bg_img)
        canvas.create_image(126.5, 36.5, image=bg_img)

        # Button Configuration: (ImageName, X_Position, Command)
        buttons_config = [
            ("button_1.png", 22, lambda: self.start_snip('rect')),
            ("button_2.png", 64, lambda: self.start_snip('circle')),
            ("button_3.png", 106, lambda: self.start_snip('free')),
            ("button_4.png", 148, self.take_fullscreen),
            ("button_5.png", 190, self.exit_app)
        ]

        for img_name, x_pos, cmd in buttons_config:
            img = PhotoImage(file=get_asset(img_name))
            self._images_cache.append(img) # Keep reference
            btn = Button(
                self.root, image=img, command=cmd,
                borderwidth=0, highlightthickness=0, relief="flat"
            )
            btn.place(x=x_pos, y=17.0, width=42.0, height=39.0)

    # ----------------------------------------------------------------
    # CORE LOGIC
    # ----------------------------------------------------------------

    def start_snip(self, mode):
        """Unified starter for all snip modes."""
        self.snip_mode = mode
        self.free_draw_points = []
        
        # 1. Hide Toolbar
        self.root.withdraw()
        # 2. Capture Screen
        self.original_screenshot = ImageGrab.grab()
        # 3. Create Overlay
        self._create_overlay()

    def _create_overlay(self):
        """Creates the full-screen transparent window for selection."""
        # dim(less transperancy black bg) ui
        self.overlay = Toplevel(self.root)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.attributes('-alpha', 0.3)
        self.overlay.configure(background='black', cursor="cross")
        
        # Canvas for drawing the red selection lines
        self.canvas_overlay = tk.Canvas(self.overlay, bg="grey11", cursor="cross")
        self.canvas_overlay.pack(fill=tk.BOTH, expand=True)

        # Bind Mouse Events
        self.canvas_overlay.bind("<ButtonPress-1>", self.on_press)
        self.canvas_overlay.bind("<B1-Motion>", self.on_drag)
        self.canvas_overlay.bind("<ButtonRelease-1>", self.on_release)
        self.overlay.bind("<Escape>", lambda e: self._close_overlay())

    def take_fullscreen(self):
        self.root.withdraw()
        # Small delay to ensure UI is gone, then grab and process
        self.root.after(200, lambda: self._process_and_exit(ImageGrab.grab()))

    def exit_app(self):
        self.root.destroy()

    def _close_overlay(self):
        if hasattr(self, 'overlay'):
            self.overlay.destroy()
        self.root.deiconify() # Bring toolbar back

    # ----------------------------------------------------------------
    # MOUSE EVENTS
    # ----------------------------------------------------------------

    def on_press(self, event):
        self.start_pos = (self.canvas_overlay.canvasx(event.x), self.canvas_overlay.canvasy(event.y))
        self.free_draw_points = [self.start_pos]
        
        # Create the shape ID (placeholder)
        if self.snip_mode == 'rect':
            self.shape_id = self.canvas_overlay.create_rectangle(*self.start_pos, *self.start_pos, outline='white', width=3, dash=(15,5))
        elif self.snip_mode == 'circle':
            self.shape_id = self.canvas_overlay.create_oval(*self.start_pos, *self.start_pos, outline='white', width=3, dash=(15,5))

    def on_drag(self, event):
        cur_x, cur_y = self.canvas_overlay.canvasx(event.x), self.canvas_overlay.canvasy(event.y)
        
        if self.snip_mode in ['rect', 'circle']:
            self.canvas_overlay.coords(self.shape_id, self.start_pos[0], self.start_pos[1], cur_x, cur_y)
        
        elif self.snip_mode == 'free':
            self.free_draw_points.append((cur_x, cur_y))
            if len(self.free_draw_points) > 1:
                self.canvas_overlay.create_line(self.free_draw_points[-2], self.free_draw_points[-1], fill="#ff0000", width=3 )

    def on_release(self, event):
        self.current_pos = (self.canvas_overlay.canvasx(event.x), self.canvas_overlay.canvasy(event.y))
        if not self.perform_snip(): 
            # Note: perform_snip calls _process_and_exit which exits the app.
            # If we didn't exit (e.g. invalid snip), we would close overlay here.
            self._close_overlay()

    # ----------------------------------------------------------------
    # IMAGE PROCESSING
    # ----------------------------------------------------------------

    def perform_snip(self):
        """Calculates coordinates and crops the image based on mode."""
        # 1. Calculate Bounds (Bounding Box)
        if self.snip_mode == 'free':
            if len(self.free_draw_points) < 3: return
            xs = [p[0] for p in self.free_draw_points]
            ys = [p[1] for p in self.free_draw_points]
            x1, x2 = int(min(xs)), int(max(xs))
            y1, y2 = int(min(ys)), int(max(ys))
        else:
            x1 = int(min(self.start_pos[0], self.current_pos[0]))
            y1 = int(min(self.start_pos[1], self.current_pos[1]))
            x2 = int(max(self.start_pos[0], self.current_pos[0]))
            y2 = int(max(self.start_pos[1], self.current_pos[1]))

        # Validate size
        width, height = x2 - x1, y2 - y1
        if width < 5 or height < 5: return False

        # 2. Basic Crop
        cropped = self.original_screenshot.crop((x1, y1, x2, y2))

        # 3. Apply Masks (for Circle/Free)
        if self.snip_mode != 'rect':
            cropped = cropped.convert("RGBA")
            mask = Image.new('L', (width, height), 0) # Black mask
            draw = ImageDraw.Draw(mask)

            if self.snip_mode == 'circle':
                draw.ellipse((0, 0, width, height), fill=255)
            elif self.snip_mode == 'free':
                # Shift points to match the cropped image coordinates
                offset_points = [(x - x1, y - y1) for x, y in self.free_draw_points]
                draw.polygon(offset_points, fill=255)
            
            cropped.putalpha(mask)

        # Instead of preview, directly process
        self._process_and_exit(cropped)
        return True

    def _process_and_exit(self, image):
        """Saves image to temp, appends to doc, and exits."""
        try:
            # 1. Setup paths
            note_img_dir = Path(self.fld_path) / "Notes_images"
            note_img_dir.mkdir(exist_ok=True)
            
            # 2. Save Screenshot
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            img_name = f"Snippet_{timestamp}.png"

            # making the folder for present notes images saving 
            present_note_imgs_path = note_img_dir / self.fl_name.strip(".docx")
            present_note_imgs_path.mkdir(exist_ok=True)

            # Add the img name in path to save it
            present_note_imgs_path = present_note_imgs_path / img_name
            
            image.save(present_note_imgs_path)
            
            # Brief pause to ensure filesystem has flushed changes
            # time.sleep(1.0)
            
            # 3. Append to Word Doc
            # doc_path = base_dir / "test.docx"
            # success, error_msg = image_appender.append_image_to_doc(str(save_path), str(doc_path))

            success, error_msg = image_appender.append_image_to_doc(str(present_note_imgs_path), str(self.file_path))
            
            if not success:
               messagebox.showerror("Error", f"Failed to append image to document.\nDetails: {error_msg}")
               
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
        finally:
            # 4. Exit Application
            self.root.destroy()

    def exit_app(self):
        self.root.destroy()

