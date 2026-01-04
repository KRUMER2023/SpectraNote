# import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path
# import ctypes
# import os

# Relative assets path for cross-system portability (adjust to your folder structure)
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"  # Example: place assets here

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class loader:
    def __init__(self,troot):
        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))

