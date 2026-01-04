
# runner.py
import sys
import time

from appdata import AppData
# from gui.gui_loader import load_ui_resources
import tkinter as tk
from tkinter import filedialog, messagebox

from gui.gui_destination_selector import start_folder_selection
from gui.gui_runner import SpectraToolbar
from gui.gui_loader import ImageLoader
from gui.gui_layout import Layout
from doc_task.text_extractor import Text_Extract
from doc_task.operation import apply_operation


def main():
    print("[INFO] 🚀Starting SpectraNote...")

    app_data = AppData()

    # 1: Folder + file selection
    start_folder_selection(app_data)

    if not app_data.get_folder_path() or not app_data.get_file_name():
        print("[ERROR] File not selected. Exiting...")
        sys.exit(0)

    print(f"[INFO] Using note file: {app_data.get_folder_path()}/{app_data.get_file_name()}")

    # 2: Preload UI resources
    try:
        print("[INFO] Preloading UI resources...")
        root = tk.Tk()
        root.withdraw()
        layout = Layout()

        Images = ImageLoader()
        print("[INFO] SpectraNote UI assets loaded successfully.")
    except Exception as e:
            messagebox.showerror("Error", f"Failed to create file:\n{e}")
            return

    # 3: Main loop
    while True:

        troot = tk.Toplevel(root)
        troot.withdraw()
        app = SpectraToolbar(app_data, Images, layout, troot)
        app.run()

        # print("[INFO] app stop")

        state = app_data.get_style()

        # print(f"[INFO] State = {state}")

        if state == "Exit":  # user clicked X
            print("[INFO] User requested exit. Exiting loop.")
            break

        # print("[INFO] Started text extract")
        # Extract selected text
        text = Text_Extract()
        if text is None: continue

        # print("[INFO] Ended text extract")

        if state == "YT":

            """Handle YT button click using Extractor for text."""
            from gui.yt_handler import handle_yt_from_text

            # Pass text to YT handler if available
            handle_yt_from_text(app_data,text.strip())

        else:
            # if none of the above state, then the callback is for appending the text so apply_operation used
            apply_operation(app_data, text, state)



if __name__ == "__main__":
    main()
