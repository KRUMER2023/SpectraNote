
import sys
import time
import os
from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

from appdata import AppData
import tkinter as tk
from tkinter import filedialog, messagebox
from gui.gui_destination_selector import start_folder_selection
from gui.gui_runner import SpectraToolbar
from gui.gui_loader import ImageLoader
from gui.gui_layout import Layout
from doc_task.text_extractor import Text_Extract
from doc_task.operation import apply_operation
from task_bar_menu.tray_icon import SystemTrayIcon


def main():

    print("[INFO] Starting SpectraNote...")

    app_data = AppData()

    # 1: Folder + file selection
    start_folder_selection(app_data)

    if not app_data.get_folder_path() or not app_data.get_file_name():
        print("[ERROR] File not selected. Exiting...")
        sys.exit(0)
    
    file_path = app_data.get_folder_path() + '/' + app_data.get_file_name()
    fl_name = app_data.get_file_name()
    fld_path = app_data.get_folder_path()
    
    # print(f"[INFO] Using note file: {app_data.get_folder_path()}/{app_data.get_file_name()}")
    print(f"[INFO] Using note file: {file_path}")

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
    print("[INFO] Starting System Tray Icon...")
    tray = SystemTrayIcon()
    tray.start_in_thread()

    while True:

        troot = tk.Toplevel(root)
        troot.withdraw()
        app = SpectraToolbar(app_data, Images, layout, troot)
        app.run()

        print("\n[INFO] Return from the note bar main funtion...")
        print("[INFO] Going for the state extraction and implementation...")

        state = app_data.get_style()

        # print(f"[INFO] State = {state}")

        if state == "Exit":  # user clicked X
            print("\n[INFO] User requested exit. Exiting loop.")
            tray.stop()
            break

        if state == "snapshot":
            from SnapShot_task.SS_auto_doc_appending import ModernSnippingTool
            # Instantiate tool (it creates its own Toplevel internally)
            snip_app = ModernSnippingTool(fld_path, fl_name)
            # Wait for the snipping tool's internal root window to close
            root.wait_window(snip_app.root)
            continue
        # print("[INFO] Started text extract")
        # Extract selected text
        print(f"\n[INFO] Going for the text extraction with state = {state} ...")
        text = Text_Extract()
        if text is None: continue

        print(f"[INFO] Text extraction ended with state = {state} ...")


        # TODO : Implement for the other states:
        #   Search
        #   translator
        #   summary

        if state == "YT":

            # Handle YT button click using Extractor for text.
            from gui.yt_handler import handle_yt_from_text

            # Pass text to YT handler if available
            handle_yt_from_text(app_data,text.strip())

        else:
            # if none of the above state, then the callback is for appending the text so apply_operation used
            try:
                apply_operation(app_data, text, state)
            except Exception as e:
                # Show error message box for operational errors
                try:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Operation Error",
                                       f"An error occurred while applying the format:\n{type(e).__name__}: {str(e)}")
                    root.destroy()
                except:
                    pass  # If we can't show message box, just continue
                print(f"[ERROR] Operation failed: {type(e).__name__}: {str(e)}")



if __name__ == "__main__":
    main()
