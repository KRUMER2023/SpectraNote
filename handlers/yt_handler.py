import os
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

from gui.gui_yt_selector import show_yt_selector
from doc_task.hyperlink_helper import append_yt_links_to_doc

# Load environment variables
load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')
BASE_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_yt_suggestions(query: str, max_results: int = 4):
    """
    Fetch top YouTube video suggestions for the query using YouTube Data API v3.
    """
    if not API_KEY:
        raise ValueError("YOUTUBE_API_KEY environment variable is not set. Please check your .env file.")
    
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'relevance',
        'maxResults': max_results,
        'key': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise ValueError(f"API error: {response.text}")
    data = response.json()
    if 'error' in data:
        raise ValueError(f"API error: {data['error']['message']}")
    return data.get('items', [])


def handle_yt_from_text(app_data, text: str):
    """
    Main handler for YouTube workflow:
    1. Validates text
    2. Fetches video suggestions
    3. Displays UI selector dialog
    4. Inserts selected links into the document
    """
    query = text.strip()
    if not query:
        messagebox.showwarning("No Text", "Select text first!")
        return

    try:
        items = fetch_yt_suggestions(query)
        if not items:
            messagebox.showinfo("No Results", "No YouTube suggestions found.")
            return

        def on_submit(urls: list, is_all: bool):
            try:
                append_yt_links_to_doc(app_data, urls, query)
                messagebox.showinfo(
                    "Success",
                    f"Added {'all' if is_all else 'selected'} YouTube suggestions to notes!"
                )
            except Exception as doc_err:
                messagebox.showerror("Document Error", f"Failed to add links to document:\n{doc_err}")

        # Show UI selector
        show_yt_selector(items, query, on_submit)

    except Exception as e:
        messagebox.showerror("YouTube Error", f"Failed to fetch suggestions:\n{e}")
