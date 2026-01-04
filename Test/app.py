# import tkinter as tk
# from tkinter import Button, Canvas, PhotoImage
# from pathlib import Path
# import ctypes
# import os
# from loader import loader

# # Relative assets path for cross-system portability (adjust to your folder structure)
# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"  # Example: place assets here

# def relative_to_assets(path: str) -> Path:
#     return ASSETS_PATH / Path(path)

# class NoteItUpApp:
#     def __init__(self):
#         self.root = tk.Tk()

#         self.load = loader(self.troot)

        
#          # Get screen dimensions for dynamic handling
#         screen_width = self.root.winfo_screenwidth()
#         screen_height = self.root.winfo_screenheight()  # Unused for now, but available
        
#         # Fixed base dimensions of our ui as designed from tkinter
#         self.BASE_WIDTH = 892
#         self.BASE_HEIGHT = 70

#         # Check for small screens and scale if needed (proportional resize)
#         scale_factor = 1.0
#         if screen_width < self.BASE_WIDTH:
#             scale_factor = screen_width / self.BASE_WIDTH
#             self.width = int(self.BASE_WIDTH * scale_factor)
#             self.height = int(self.BASE_HEIGHT * scale_factor)
#             print(f"[INFO] Screen width {screen_width} < {self.BASE_WIDTH}; scaling UI by {scale_factor:.2f}")
#         else:
#             self.width = self.BASE_WIDTH
#             self.height = self.BASE_HEIGHT
        
#         self.root.geometry(f"{self.width}x{self.height}")
#         self.root.overrideredirect(True)
#         # this attribute to make black clour transparent
#         self.root.wm_attributes("-transparentcolor", "#000000")
#         self.root.wm_attributes("-topmost", True)

#         # Make window non-focusable (Windows-specific; add platform checks if needed)
#         if 'win' in self.root.tk.call('tk', 'windowingsystem').lower():
#             hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
#             GWL_EXSTYLE = -20
#             WS_EX_NOACTIVATE = 0x08000000
#             style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
#             ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE)

#         # Create canvas with scaled dimensions
#         # give canvas bg as black as for ensure that it must be transparent all the time
#         self.canvas = Canvas(
#             self.root,
#             bg="#000000",
#             height=self.height,
#             width=self.width,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge"
#         )
#         self.canvas.place(x=0, y=0)

#         # Load images (assume they scale with window; Tkinter handles basic resize)
#         # Center gui bg called main circle while designing

#         # self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
#         # self.image_5 = self.canvas.create_image(self.width / 2, self.height / 2, image=self.image_image_5)
        

#         i5 = self.load.image_image_5
#         self.image_5 = self.canvas.create_image(self.width / 2, self.height / 2, image=i5)
    

#         # Drag handle image
#         # A small icon over the main center cirle bg also used for canvas drag option

#         # self.image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
#         # self.image_6 = self.canvas.create_image(self.width / 2, self.height / 2, image=self.image_image_6)
        
#         i6 = self.load.image_image_6
#         self.image_6 = self.canvas.create_image(self.width / 2, self.height / 2, image=i6)


#         # Initial center-top position
#         x = (screen_width - self.width) // 2
#         self.root.geometry(f"+{x}+0")

#     def run(self):
#         self.root.mainloop()

# note = NoteItUpApp()
# note.run()




from gui.gui_loader import ImageLoader
from gui.gui_layout import Layout
import tkinter as tk
from tkinter import Canvas, Button
import ctypes
import os

root = tk.Tk()
loader = ImageLoader()
layout = Layout()

width = layout.measurements["width"]
height = layout.measurements["height"]
s_width = layout.measurements["screen_w"]
s_height = layout.measurements["screen_h"]
b_width = layout.measurements["base_width"]
b_height = layout.measurements["base_height"]
scale = layout.measurements["scale"]

print(width, height, s_width, s_height, scale)

center_x = int((s_width - width) / 2)
root.geometry(f"{width}x{height}+{center_x}+0")


root.overrideredirect(True)
root.wm_attributes("-transparentcolor", "#000000")
root.wm_attributes("-topmost", True)

# Make window non-focusable (Windows)
if 'win' in root.tk.call('tk', 'windowingsystem').lower():
    try:
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        GWL_EXSTYLE = -20
        WS_EX_NOACTIVATE = 0x08000000
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE)
    except Exception:
        print("Error in making window non focusable")

# Canvas (transparent)
canvas = Canvas(
    root,
    bg="#000000",
    width=width,
    height=height,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.place(x=0, y=0)



def toggle_left_buttons():
    temp = list(Left_panel_elements["button"].keys())
    if Left_panel_elements["button"][temp[-1]].winfo_ismapped():
        toogle_button["toggle_left"].configure(image=loader.images["toggle_left"])
        for lf in Left_panel_elements["button"].keys():
            Left_panel_elements["button"][lf].place_forget()

        for lf in Left_panel_elements["bg"].keys():
            canvas.itemconfigure(Left_panel_elements["bg"][lf], state="hidden")
    else:
        toogle_button["toggle_left"].configure(image=loader.images["toggle_right"])
        for lf in Left_panel_elements["bg"].keys():
            canvas.itemconfigure(Left_panel_elements["bg"][lf], state="normal")

        for lf in Left_panel_elements["button"].keys():
            x = layout.positions["Left_panel"]["button"][lf][0]
            y = layout.positions["Left_panel"]["button"][lf][1]
            Left_panel_elements["button"][lf].place(x = x*scale, y = y*scale, width=42*scale, height=46*scale)

def toggle_right_buttons():
    temp = list(Right_panel_elements["button"].keys())
    if Right_panel_elements["button"][temp[-1]].winfo_ismapped():
        toogle_button["toggle_right"].configure(image=loader.images["toggle_right"])
        for ri in Right_panel_elements["button"].keys():
            Right_panel_elements["button"][ri].place_forget()

        for ri in Right_panel_elements["bg"].keys():
            canvas.itemconfigure(Right_panel_elements["bg"][ri], state="hidden")
    else:
        toogle_button["toggle_right"].configure(image=loader.images["toggle_left"])
        for ri in Right_panel_elements["bg"].keys():
            canvas.itemconfigure(Right_panel_elements["bg"][ri], state="normal")

        for ri in Right_panel_elements["button"].keys():
            x = layout.positions["Right_panel"]["button"][ri][0]
            y = layout.positions["Right_panel"]["button"][ri][1]
            Right_panel_elements["button"][ri].place(x = x*scale, y = y*scale, width=42*scale, height=46*scale)

actions = {
    # toggle buttons
    "toggle_left":  toggle_left_buttons,
    "toggle_right": toggle_right_buttons,    

    # right panel buttons
    "exit":         lambda : root.destroy(),
    "bullet":       lambda : print("bullet"),
    "h2":           lambda : print("h2"),
    "h1":           lambda : print("h1"),
    "bold":         lambda : print("bold"),
    "italic":       lambda : print("italic"),
    "normal":       lambda : print("normal"),
    
    # left panel buttons
    "folder":       lambda : print("folder"),
    "file":         lambda : print("file"),
    "chatbot":      lambda : print("chatbot"),
    "summary":      lambda : print("summary"),
    "translator":   lambda : print("translator"),
    "search":       lambda : print("Search"),
    "youtube":      lambda : print("yt")
}


toogler = layout.positions["Toogler"]

mian_bgs = []

for bg in toogler["bg"].keys():
    bg_circle = canvas.create_image(
            width / 2, height / 2,
            image=loader.images[bg]
        )
    mian_bgs.append(bg_circle)

toogle_button = {}
for btn in toogler["button"].keys():
    
    bt = Button(
        root,
        image=loader.images[btn],
        borderwidth=0,
        highlightthickness=0,
        command=actions[btn],
        relief="flat"
    )

    bt.place(x=toogler["button"][btn][0], y=layout.positions["Toogler"]["button"][btn][1], width=23*scale, height=30*scale)
    toogle_button[btn] = bt


# Left panel ....

Left_panel_elements = {"bg":{}, "button":{}}

Left_panel = layout.positions["Left_panel"]

for lf in Left_panel["bg"].keys():
    x = layout.positions["Left_panel"]["bg"][lf][0]
    bg = canvas.create_image(
        width * x / b_width,
        height / 2,
        image=loader.images[lf],
        state="hidden"
    )
    Left_panel_elements["bg"][lf] = bg

for obj in mian_bgs:
    canvas.tag_raise(obj)

for lf in Left_panel["button"].keys():
    bt = Button(
        root,
        image= loader.images[lf],
        borderwidth=0,
        highlightthickness=0,
        command = actions[lf] ,
        relief="flat"
    )
    Left_panel_elements["button"][lf] = bt



# Right panel ....   
Right_panel_elements = {"bg":{}, "button":{}}

Right_panel = layout.positions["Right_panel"]

for ri in Right_panel["bg"].keys():
    x = layout.positions["Right_panel"]["bg"][ri][0]
    bg = canvas.create_image(
        width * x / b_width,
        height / 2,
        image=loader.images[ri],
        state="hidden"
    )
    Right_panel_elements["bg"][ri] = bg

for obj in mian_bgs:
    canvas.tag_raise(obj)

for ri in Right_panel["button"].keys():
    bt = Button(
        root,
        image= loader.images[ri],
        borderwidth=0,
        highlightthickness=0,
        command = actions[ri] ,
        relief="flat"
    )
    Right_panel_elements["button"][ri] = bt


root.mainloop()

