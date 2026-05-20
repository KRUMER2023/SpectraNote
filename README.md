# SpectraNote Project Documentation

## 1. Project Overview

**SpectraNote** is a Python-based desktop productivity application designed to streamline the process of taking notes and managing content directly into Microsoft Word documents. It provides a non-intrusive, floating toolbar interface that allows users to capture screenshots, extract text, and apply formatting on the fly without navigating away from their current work.

### Key Features
- **Floating Toolbar**: A "SpectraToolbar" that floats over other windows for quick access.
- **Smart Text Appending**: Extract text and append it to a Word document with specific styles (Headings, Bold, Italic, Bullets, etc.).
- **Integrated Snipping Tool**: A custom-built screenshot tool supporting Rectangular, Circular, and Freehand selections. Screenshots are automatically saved and appended to the active Word document.
- **System Tray Integration**: Minimized footprint with system tray support for background operation.
- **YouTube Integration**: Dedicated handling for YouTube content (via `yt_handler`).

---

## 2. File Structure

The project is organized into modular directories, each responsible for a specific aspect of the application.

```
SpectraNote/
├── runner.py                 # Main Entry Point
├── appdata.py                # Configuration and State Management
├── requirements              # Project Dependencies
├── gui/                      # Graphical User Interface Modules
│   ├── gui_runner.py         # Main Toolbar Class (SpectraToolbar)
│   ├── gui_loader.py         # Image/Asset Loader
│   ├── gui_layout.py         # Toolbar Layout Configuration
│   ├── gui_destination_selector.py # File/Folder Selection Dialog
│   └── yt_handler.py         # YouTube Content Handler
├── SnapShot_task/            # Screenshot & Image Logic
│   ├── SS_auto_doc_appending.py # ModernSnippingTool Implementation
│   ├── image_appender.py     # Logic to append images to Word
│   └── assets/               # UI Assets for Snipping Tool
├── doc_task/                 # Document Operations
│   ├── operation.py          # Text Styles & Appending Logic
│   ├── text_extractor.py     # Text Extraction Utility
│   └── doc_manager.py        # Word Document Management
└── task_bar_menu/            # System Integration
    └── tray_icon.py          # System Tray Icon Logic
├── Test/                     # Development Testing
│   └── app.py                # Standalone GUI Test Harness
└── chatbot/                  # (Empty Directory - Reserved for future use)
```

---

## 3. Component Analysis

### 3.1 Main Application (`runner.py`)
This is the core driver of the application.
- **Startup**: Initializes `AppData`, prompts user for the target Word document using `gui_destination_selector`.
- **Resource Loading**: Preloads UI assets via `gui_loader` to ensure responsiveness.
- **Event Loop**: Runs the `SpectraToolbar` in a loop. It listens for state changes returned by the toolbar (e.g., 'snapshot', 'h1', 'bold', 'YT').
- **Delegation**: Based on the returned state, it delegates tasks:
    - `"snapshot"` -> Launches `ModernSnippingTool`.
    - `"YT"` -> Calls `handle_yt_from_text`.
    - Text Styling -> Calls `apply_operation` from `doc_task`.

### 3.2 Graphical User Interface (`gui/`)
- **`gui_runner.py`**: Implements `SpectraToolbar`, the primary interface users interact with. It manages buttons and returns "states" to `runner.py` when actions are triggered.
- **`gui_destination_selector.py`**: A dialog ensuring the user selects a valid folder and filename for the notes document before the app starts.

### 3.3 Snapshot Module (`SnapShot_task/`)
- **`SS_auto_doc_appending.py`**: A sophisticated Tkinter-based snipping tool.
    - **Modes**: supports `rect` (Rectangle), `circle` (Circle), and `free` (Freehand) selections.
    - **Overlay**: Uses a transparent full-screen overlay for drawing selections.
    - **Processing**: Captures the screen, applies masking (for non-rectangular shapes), saves the image to a `temp/` folder, and automatically triggers `image_appender` to put it in the Word doc.

### 3.4 Document Task (`doc_task/`)
- **`operation.py`**: The bridge between the app and the Word document. It contains a dispatcher `STYLE_FUNCTIONS` that maps commands (e.g., "bold", "h1") to specific `python-docx` operations.
- **`doc_manager.py`**: Likely handles opening/closing of the `.docx` file safely.

### 3.5 System Integration (`task_bar_menu/`)
- **`tray_icon.py`**: Manages the system tray icon using `pystray`. It runs in a separate thread and allows minimizing the app to the tray, with a menu to Exit.

### 3.6 Development Utilities (`Test/`)
- **`app.py`**: A standalone script to test the GUI layout and responsiveness without running the full application logic. It mocks button actions with print statements.

---

## 4. Installation & Requirements

### Dependencies
The project relies on several external Python libraries, listed in the `requirements` file:

- **GUI & System**: `tkinter` (Standard Lib), `pystray` (System Tray), `pyautogui` (Automation), `screeninfo` (Display metrics).
- **Document Handling**: `python-docx` (Word manipulation).
- **Image Processing**: `Pillow` (PIL fork).
- **Utilities**: `pyperclip` (Clipboard access), `requests` (Network calls).

### Setup
1. Ensure Python 3.x is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements
   ```
   *(Note: The file is named `requirements` without the .txt extension in the root directory)*

---

## 5. Usage Flow

1. **Launch**: Run `python runner.py`.
2. **Setup**: Select the destination folder and filename for your notes when prompted.
3. **Toolbar**: The SpectraToolbar will appear.
4. **Operations**:
    - **Text**: Highlight text or copy it to clipboard, then click a style button (e.g., H1, Bold) on the toolbar to append it to your document.
    - **Snapshot**: Click the snapshot icon to enter snipping mode. Draw your selection; it will be automatically saved and added to the Word file.
    - **Exit**: Close the toolbar or use the system tray icon to exit the application.
