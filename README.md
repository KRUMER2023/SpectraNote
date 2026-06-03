

# <img width="56" height="56" alt="icon" src="https://github.com/user-attachments/assets/8e108c95-2be7-424a-b484-47f3887a38b5" />  SpectraNote : Your floating capture assistant

**The Ultimate Desktop Productivity & Research Companion**

SpectraNote is a high-performance, non-intrusive floating desktop application designed to streamline research, note-taking, and content curation. It acts as an invisible bridge between your active workspace (browsers, PDFs, videos) and Microsoft Word, allowing you to capture, format, and organize information without ever breaking your focus or switching windows.

---

## Why SpectraNote?

Traditional research requires constant context switching—copying text, alt-tabbing to Word, pasting, formatting, and repeating. SpectraNote eliminates this friction. With a sleek, transparent floating toolbar that never steals window focus, you can shoot text, formatted notes, screenshots, and YouTube links directly into your target `.docx` file on the fly.

<img width="131" height="73" alt="UI_Collapsed" src="https://github.com/user-attachments/assets/570f476e-e293-4a77-875d-f546b2914e07" />
<img width="892" height="77" alt="UI_UnCollapsed" src="https://github.com/user-attachments/assets/fdb37d76-23b7-4515-8c88-f6bcc9541428" />


## Key Features

- **Ghost-Mode Floating Toolbar**: A completely borderless, transparent UI that floats above your work. It uses advanced Windows API hooks (`WS_EX_NOACTIVATE`) to ensure it never steals focus from your active application.
- **Smart Text Extraction & Appending**: Highlight any text, click a format button (e.g., H1, Bold, Bullet), and SpectraNote automatically extracts it via clipboard emulation and appends it to your Word document with the correct styling.
- **Advanced Integrated Snipping Tool**: A custom-built, multi-mode screenshot utility supporting:
  - **Rectangular** Selection
  - **Circular** Selection
  - **Freehand** Lasso Selection
  Automatically crops, applies alpha masks, and scales high-res images before inserting them directly into your notes.
- **YouTube Integration**: Seamlessly extract text, search YouTube via REST APIs, and inject clickable hyperlink references (`w:hyperlink`) directly into your document.
- **tray System Tray Operation**: Runs silently in the background with a minimal footprint, accessible via the Windows System Tray.

---

## Tech Stack & Architecture

SpectraNote is built for speed and reliability, leveraging a unique **State-Return Loop** architecture to prevent UI freezing during heavy document operations.

- **Core**: Python 3.x
- **GUI**: Highly customized `Tkinter` (Borderless, Transparent, High DPI Aware)
- **Document Processing**: `python-docx`
- **Image Processing**: `Pillow` (PIL)
- **System Integration**: `pyautogui`, `pyperclip`, `pystray`, `screeninfo`
- **APIs**: YouTube Data API (REST)

---

## Installation & Setup

### Prerequisites
- Windows OS (Requires Windows API for focus management)
- Python 3.8+
- Microsoft Word (to view the generated `.docx` files)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/SpectraNote.git
   cd SpectraNote
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements
   ```

4. **Environment Variables:**
   Rename `.env.example` to `.env` and add your YouTube Data API key if you plan to use the YouTube integration features.

---

## How to Use

1. **Launch the App:**
   ```bash
   python runner.py
   ```
2. **Initialize Workspace:** On startup, select a destination folder and either create a new Word document or select an existing one to append to.
3. **Capture Text:** Highlight text in your browser or PDF, then click a styling button (H1, H2, Bold, Normal) on the SpectraNote toolbar.
4. **Capture Images:** Click the Camera icon, select your snip mode (Rect, Circle, Freehand), and draw on the screen. The image is instantly saved and embedded in your document.
5. **Exit:** Close the application via the "X" on the toolbar or right-click the system tray icon and select "Exit".

---

##  Under the Hood (For Developers)

SpectraNote avoids standard Tkinter mainloop blocking by utilizing a **State-Return Loop**:
- The GUI runs and waits for user input.
- Upon clicking a button, the GUI updates a global state and destroys its own window.
- The main `runner.py` loop regains execution, performs the heavy lifting (DOM manipulation in Word, saving images), and then instantly respawns the GUI.
This ensures the UI is always snappy and never enters a "Not Responding" state.

---
## File Structure

The project is organized into modular directories, each responsible for a specific aspect of the application.

```
SpectraNote/
├── runner.py                 # Main Entry Point
├── appdata.py                # Configuration and State Management
├── requirements              # Project Dependencies
├── .env.example              # Environment Variables Template
├── gui/                      # Graphical User Interface Modules
│   ├── gui_runner.py         # Main Toolbar Class (SpectraToolbar)
│   ├── gui_loader.py         # Image/Asset Loader
│   ├── gui_layout.py         # Toolbar Layout Configuration
│   ├── gui_destination_selector.py # File/Folder Selection Dialog
│   ├── yt_handler.py         # YouTube Content Handler
│   └── assets/               # UI Assets for Main Toolbar
├── SnapShot_task/            # Screenshot & Image Logic
│   ├── SS_auto_doc_appending.py # ModernSnippingTool Implementation
│   ├── image_appender.py     # Logic to append images to Word
│   └── assets/               # UI Assets for Snipping Tool
├── doc_task/                 # Document Operations
│   ├── operation.py          # Text Styles & Appending Logic
│   ├── text_extractor.py     # Text Extraction Utility
│   └── doc_manager.py        # Word Document Management
└── task_bar_menu/            # System Integration
    ├── tray_icon.py          # System Tray Icon Logic
    └── icon.png              # Taskbar Tray Icon
```

---

##  TODO's :

- **AI Chatbot Integration**: Context-aware AI assistant built directly into the floating toolbar.
- **Real-Time Translator**: On-the-fly translation of captured text before injecting it into the document.
- **Cloud Sync**: Native support for Google Docs and Notion APIs.

---

# Next Build Will Have Modern UI Framework, with New AI Features, Stay Connected
