import requests
import tkinter as tk
from tkinter import messagebox

from gui.gui_yt_selector import show_yt_selector
from doc_task.hyperlink_helper import append_yt_links_to_doc

INNERTUBE_URL = "https://www.youtube.com/youtubei/v1/search"


def fetch_yt_suggestions(query: str, max_results: int = 4):
    """
    Fetch top YouTube video suggestions for the query using YouTube's direct
    Innertube public endpoint without requiring any external API keys.
    """
    payload = {
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20231201.00.00"
            }
        },
        "query": query
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(INNERTUBE_URL, json=payload, headers=headers, timeout=8)
        if response.status_code != 200:
            raise ValueError(f"HTTP {response.status_code}: {response.text[:200]}")
        
        data = response.json()
    except Exception as err:
        raise ValueError(f"Failed to query YouTube search endpoint: {err}")

    items = []
    contents = (
        data.get("contents", {})
            .get("twoColumnSearchResultsRenderer", {})
            .get("primaryContents", {})
            .get("sectionListRenderer", {})
            .get("contents", [])
    )

    for section in contents:
        item_section = section.get("itemSectionRenderer", {}).get("contents", [])
        for item in item_section:
            video = item.get("videoRenderer")
            if video and len(items) < max_results:
                video_id = video.get("videoId")
                if not video_id:
                    continue

                # Extract title
                title_runs = video.get("title", {}).get("runs", [])
                title = "".join([r.get("text", "") for r in title_runs]) if title_runs else "Untitled Video"

                # Extract channel / author name
                owner_runs = video.get("ownerText", {}).get("runs") or video.get("shortBylineText", {}).get("runs")
                channel_name = owner_runs[0].get("text", "") if owner_runs else ""

                # Extract highest quality thumbnail
                thumbnails = video.get("thumbnail", {}).get("thumbnails", [])
                thumb_url = thumbnails[-1].get("url") if thumbnails else ""
                if thumb_url and thumb_url.startswith("//"):
                    thumb_url = "https:" + thumb_url

                items.append({
                    "id": {"videoId": video_id},
                    "snippet": {
                        "title": title,
                        "channelTitle": channel_name,
                        "thumbnails": {
                            "medium": {"url": thumb_url},
                            "default": {"url": thumb_url}
                        }
                    }
                })

    return items


def handle_yt_from_text(app_data, text: str):
    """
    Main handler for YouTube workflow:
    1. Validates text
    2. Fetches video suggestions (keyless)
    3. Displays UI selector dialog with direct preview link
    4. Inserts rich selected video links into the document
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

        def on_submit(video_entries: list, is_all: bool):
            try:
                append_yt_links_to_doc(app_data, video_entries, query)
                messagebox.showinfo(
                    "Success",
                    f"Added {'all' if is_all else 'selected'} YouTube suggestions to notes!"
                )
            except Exception as doc_err:
                messagebox.showerror("Document Error", f"Failed to add links to document:\n{doc_err}")

        # Show UI selector
        show_yt_selector(items, query, on_submit)

    except Exception as e:
        messagebox.showerror("YouTube Error", f"Failed to fetch suggestions: {e}")
