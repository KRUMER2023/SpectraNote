import time
import tkinter as tk
from tkinter import messagebox
import pyperclip
import pyautogui
import pygetwindow as gw
from .operation import apply_operation

def _warn(title, text):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(title, text)
    root.destroy()

def _error(title, text):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, text)
    root.destroy()

def Text_Extract():
    try:
        # Get currently active window (likely our GUI)
        current_window = gw.getActiveWindow()
        # Get all windows and assume the previous one is the one user was working in
        windows = gw.getWindowsWithTitle(current_window.title) if current_window else []

        # Wait a tiny bit for GUI to destroy
        time.sleep(0.05)

        # Activate previous window
        if windows:
            prev_window = windows[0]
            prev_window.activate()
            time.sleep(0.05)

        # Simulate Ctrl+C to copy selected text
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)  # give OS time to update clipboard
        text = pyperclip.paste()

        if not text or not text.strip():
            _warn("No Selection", "No text was copied. Please select text in another app and try again.")
            return None
        
        return text

    except Exception as e:
        _error("Extractor Error", f"Error extracting/applying operation:\n{e}")
        return None

# def Extractor(style: str):
#     """
#     Grab currently selected text from previous active window,
#     apply the style, save the document.
#     """
#     try:
#         # Get currently active window (likely our GUI)
#         current_window = gw.getActiveWindow()
#         # Get all windows and assume the previous one is the one user was working in
#         windows = gw.getWindowsWithTitle(current_window.title) if current_window else []

#         # Wait a tiny bit for GUI to destroy
#         time.sleep(0.05)

#         # Activate previous window
#         if windows:
#             prev_window = windows[0]
#             prev_window.activate()
#             time.sleep(0.05)

#         # Simulate Ctrl+C to copy selected text
#         pyautogui.hotkey('ctrl', 'c')
#         time.sleep(0.1)  # give OS time to update clipboard
#         text = pyperclip.paste()

#         if not text or not text.strip():
#             _warn("No Selection", "No text was copied. Please select text in another app and try again.")
#             return

#         # Apply style
#         apply_operation(text, style)

#     except Exception as e:
#         _error("Extractor Error", f"Error extracting/applying operation:\n{e}")
