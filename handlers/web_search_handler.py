import webbrowser
import urllib.parse
import tkinter as tk
from tkinter import messagebox

def handle_web_search_from_text(text: str):
    """
    Takes extracted text, encodes it, and opens a Google search in the default browser.
    """
    query = text.strip()
    if not query:
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Empty Query", "No text selected to search.")
        root.destroy()
        return

    try:
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        print(f"[INFO] Opening web search for: '{query}' -> {search_url}")
        webbrowser.open(search_url)
    except Exception as e:
        print(f"[ERROR] Failed to open browser search: {e}")
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Web Search Error", f"Failed to perform search:\n{e}")
            root.destroy()
        except:
            pass
