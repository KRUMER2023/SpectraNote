import tkinter as tk
from tkinter import messagebox, Checkbutton, IntVar, Button, Label, Frame, Canvas, Scrollbar
import requests
import io
import webbrowser

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def show_yt_selector(items: list, original_query: str, on_submit_callback) -> None:
    """
    Modern, resizable popup dialog to select YouTube videos with responsive cards,
    thumbnails, channel names, a sleek '↗' browser preview button aligned directly
    next to the checkbox, and rich document export.

    :param items: List of YouTube API/Innertube search item dictionaries.
    :param original_query: The query text used to search.
    :param on_submit_callback: Callback function taking (selected_entries: list, is_all: bool)
    """
    root = tk.Toplevel()
    root.title(f"YouTube Suggestions - '{original_query[:30]}'")
    root.geometry("680x540")
    root.minsize(580, 440)
    root.resizable(True, True)
    root.configure(bg="#F8FAFC")

    vars_ = []
    video_map = {}
    item_titles = []
    thumbnails_cache = []
    card_frames = []

    # ---------------------------------------------------------
    # 1. Header Area
    # ---------------------------------------------------------
    header_frame = Frame(root, bg="#FFFFFF", padx=18, pady=12, highlightthickness=1, highlightbackground="#E2E8F0")
    header_frame.pack(fill=tk.X, side=tk.TOP)

    header_title = Label(
        header_frame,
        text="📺 YouTube Video Suggestions",
        font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF",
        fg="#0F172A"
    )
    header_title.pack(anchor="w")

    header_sub = Label(
        header_frame,
        text=f"Query: \"{original_query}\" • {len(items)} videos available",
        font=("Segoe UI", 9),
        bg="#FFFFFF",
        fg="#64748B"
    )
    header_sub.pack(anchor="w", pady=(2, 0))

    # ---------------------------------------------------------
    # 2. Bottom Action Bar
    # ---------------------------------------------------------
    bottom_bar = Frame(root, bg="#FFFFFF", padx=18, pady=12, highlightthickness=1, highlightbackground="#E2E8F0")
    bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)

    selection_status = Label(
        bottom_bar,
        text="0 selected",
        font=("Segoe UI", 9, "bold"),
        bg="#FFFFFF",
        fg="#64748B"
    )
    selection_status.pack(side=tk.LEFT)

    def update_status():
        count = sum(1 for v in vars_ if v.get())
        selection_status.config(text=f"{count} of {len(items)} selected")

    def on_add_selected():
        selected_entries = [video_map[item_titles[i]] for i, var in enumerate(vars_) if var.get()]
        if not selected_entries:
            messagebox.showwarning("No Selection", "Please select at least one video to add.")
            return
        root.destroy()
        on_submit_callback(selected_entries, is_all=False)

    def on_add_all():
        all_entries = [video_map[t] for t in item_titles]
        root.destroy()
        on_submit_callback(all_entries, is_all=True)

    btn_add_selected = Button(
        bottom_bar,
        text="✓ Add Selected to Doc",
        font=("Segoe UI", 9, "bold"),
        bg="#2563EB",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=6,
        command=on_add_selected
    )
    btn_add_selected.pack(side=tk.RIGHT, padx=(8, 0))

    btn_add_all = Button(
        bottom_bar,
        text="Add All Videos",
        font=("Segoe UI", 9),
        bg="#F1F5F9",
        fg="#334155",
        activebackground="#E2E8F0",
        activeforeground="#0F172A",
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=6,
        command=on_add_all
    )
    btn_add_all.pack(side=tk.RIGHT)

    # ---------------------------------------------------------
    # 3. Main Scrollable Container
    # ---------------------------------------------------------
    container = Frame(root, bg="#F8FAFC")
    container.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

    canvas = Canvas(container, bg="#F8FAFC", highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#F8FAFC")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_canvas_resize(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", on_canvas_resize)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def cleanup_mousewheel(e):
        canvas.unbind_all("<MouseWheel>")

    root.bind("<Destroy>", cleanup_mousewheel)

    # ---------------------------------------------------------
    # 4. Video Cards
    # ---------------------------------------------------------
    for i, item in enumerate(items):
        snippet = item.get('snippet', {})
        video_id = item.get('id', {}).get('videoId', '')
        title = snippet.get('title', 'Untitled Video')
        channel = snippet.get('channelTitle', '')
        url = f"https://www.youtube.com/watch?v={video_id}"

        item_titles.append(title)
        thumbnails = snippet.get('thumbnails', {})
        thumb_url = thumbnails.get('medium', {}).get('url') or \
                    thumbnails.get('high', {}).get('url') or \
                    thumbnails.get('default', {}).get('url')

        video_map[title] = {
            'title': title,
            'url': url,
            'channel': channel,
            'thumbnail_url': thumb_url
        }

        # Card container
        card = Frame(
            scrollable_frame,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            relief="flat",
            padx=12,
            pady=10
        )
        card.pack(fill=tk.X, expand=True, pady=6, padx=2)
        card_frames.append(card)

        # Thumbnail (Left)
        thumb_frame = Frame(card, bg="#E2E8F0", width=125, height=75)
        thumb_frame.pack_propagate(False)
        thumb_frame.pack(side=tk.LEFT, padx=(0, 12))

        if PIL_AVAILABLE and thumb_url:
            try:
                res = requests.get(thumb_url, timeout=4)
                img_data = Image.open(io.BytesIO(res.content))
                img_data = img_data.resize((125, 75), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_data)
                thumbnails_cache.append(photo)

                thumb_lbl = Label(thumb_frame, image=photo, bg="#E2E8F0")
                thumb_lbl.pack(fill=tk.BOTH, expand=True)
            except Exception:
                thumb_lbl = Label(thumb_frame, text="▶ No Preview", bg="#E2E8F0", fg="#64748B", font=("Segoe UI", 8))
                thumb_lbl.pack(fill=tk.BOTH, expand=True)
        else:
            thumb_lbl = Label(thumb_frame, text="▶ Video", bg="#E2E8F0", fg="#64748B", font=("Segoe UI", 9, "bold"))
            thumb_lbl.pack(fill=tk.BOTH, expand=True)

        # Right Action Area: "↗" Button + Checkbox (aligned together on the right)
        right_action_frame = Frame(card, bg="#FFFFFF")
        right_action_frame.pack(side=tk.RIGHT, padx=(8, 2))

        def make_open_handler(video_url):
            return lambda: webbrowser.open(video_url)

        btn_open_browser = Button(
            right_action_frame,
            text="↗",
            font=("Segoe UI", 11, "bold"),
            bg="#EFF6FF",
            fg="#2563EB",
            activebackground="#DBEAFE",
            activeforeground="#1D4ED8",
            relief="flat",
            cursor="hand2",
            width=2,
            padx=3,
            pady=2,
            command=make_open_handler(url)
        )
        btn_open_browser.pack(side=tk.LEFT, padx=(0, 10))

        var = IntVar()
        vars_.append(var)

        check_btn = Checkbutton(
            right_action_frame,
            variable=var,
            text="",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            cursor="hand2",
            command=update_status
        )
        check_btn.pack(side=tk.LEFT)

        # Middle Content Area
        content_frame = Frame(card, bg="#FFFFFF")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_lbl = Label(
            content_frame,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
            justify="left",
            wraplength=360,
            anchor="w"
        )
        title_lbl.pack(fill=tk.X, expand=True, anchor="w")

        def update_wraplength(event, lbl=title_lbl):
            lbl.config(wraplength=max(180, event.width - 20))

        content_frame.bind("<Configure>", update_wraplength)

        # Channel Sub-row
        if channel:
            channel_lbl = Label(
                content_frame,
                text=f"👤 {channel}",
                font=("Segoe UI", 8, "bold"),
                fg="#475569",
                bg="#FFFFFF",
                anchor="w"
            )
            channel_lbl.pack(fill=tk.X, anchor="w", pady=(4, 0))

        # Toggle selection on clicking card or title
        def make_toggle_handler(v):
            def _toggle(e=None):
                v.set(0 if v.get() else 1)
                update_status()
            return _toggle

        toggle_fn = make_toggle_handler(var)
        card.bind("<Button-1>", toggle_fn)
        content_frame.bind("<Button-1>", toggle_fn)
        title_lbl.bind("<Button-1>", toggle_fn)
        thumb_lbl.bind("<Button-1>", toggle_fn)

    # Initialize counter
    update_status()

    root.grab_set()
    root.wait_window()
