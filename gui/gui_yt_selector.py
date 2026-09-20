import tkinter as tk
from tkinter import messagebox, Checkbutton, IntVar, Button, Label, Frame, Canvas, Scrollbar
import requests
import io

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def show_yt_selector(items: list, original_query: str, on_submit_callback) -> None:
    """
    Popup dialog to select YouTube videos with checkboxes, thumbnails, and action buttons.

    :param items: List of YouTube API search item dictionaries.
    :param original_query: The query text used to search.
    :param on_submit_callback: Callback function taking (selected_urls: list, is_all: bool)
    """
    root = tk.Toplevel()
    root.title("YouTube Suggestions")
    root.geometry("500x400")
    root.resizable(False, False)

    vars_ = []
    video_map = {}
    thumbnails_cache = []

    # Main container
    main_frame = Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Scrollable frame for video items
    canvas = Canvas(main_frame)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for item in items:
        snippet = item['snippet']
        video_id = item['id']['videoId']
        title = snippet['title']
        url = f"https://www.youtube.com/watch?v={video_id}"

        thumbnails = snippet.get('thumbnails', {})
        thumb_url = thumbnails.get('medium', {}).get('url') or \
                    thumbnails.get('high', {}).get('url') or \
                    thumbnails.get('default', {}).get('url')

        item_frame = Frame(scrollable_frame, relief="groove", borderwidth=1)
        item_frame.pack(fill=tk.X, pady=5, padx=5)

        if PIL_AVAILABLE and thumb_url:
            try:
                response = requests.get(thumb_url, timeout=5)
                img_data = Image.open(io.BytesIO(response.content))
                img_data = img_data.resize((120, 90), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_data)
                thumbnails_cache.append(photo)

                thumb_label = Label(item_frame, image=photo)
                thumb_label.pack(side=tk.LEFT, padx=5, pady=5)
            except Exception as e:
                print(f"[WARNING] Could not load thumbnail: {e}")
                thumb_label = Label(item_frame, text="[No Thumbnail]", width=15)
                thumb_label.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            thumb_label = Label(item_frame, text="[Thumbnail]", width=15, bg="lightgray")
            thumb_label.pack(side=tk.LEFT, padx=5, pady=5)

        text_frame = Frame(item_frame)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        display_title = title[:60] + "..." if len(title) > 60 else title
        title_label = Label(text_frame, text=display_title, wraplength=250, justify="left")
        title_label.pack(anchor="w")

        var = IntVar()
        vars_.append(var)
        check_btn = Checkbutton(text_frame, text="Select", variable=var)
        check_btn.pack(anchor="w")

        video_map[title] = {
            'title': title,
            'url': url,
            'thumbnail_url': thumb_url
        }

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_add_selected():
        selected_titles = [items[i]['snippet']['title'] for i, var in enumerate(vars_) if var.get()]
        if not selected_titles:
            messagebox.showwarning("No Selection", "No videos selected!")
            return
        selected_urls = [video_map[title]['url'] for title in selected_titles]
        root.destroy()
        on_submit_callback(selected_urls, is_all=False)

    def on_add_all():
        urls = [video_map[items[i]['snippet']['title']]['url'] for i in range(len(items))]
        root.destroy()
        on_submit_callback(urls, is_all=True)

    button_frame = Frame(root)
    button_frame.pack(fill=tk.X, pady=10)

    Button(button_frame, text="ASTD (Add Selected To Doc)", command=on_add_selected).pack(side=tk.LEFT, padx=20, pady=5)
    Button(button_frame, text="AATD (Add All To Doc)", command=on_add_all).pack(side=tk.RIGHT, padx=20, pady=5)

    root.wait_window()
