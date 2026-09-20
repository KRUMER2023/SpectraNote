<div align="center">

  <img src="public_images/logo.png" alt="SpectraNote Logo" />

  # SpectraNote
  ### *The Invisible Bridge Between Your Active Workspace and Notes*

  <p align="center">
    <strong>A high-performance, non-intrusive floating HUD designed for researchers, students, and engineers to capture, format, and organize content into Word documents in real time.</strong>
  </p>

  <p align="center">
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"></a>
    <a href="https://microsoft.com/word"><img src="https://img.shields.io/badge/Output-Microsoft%20Word%20(.docx)-2B579A?style=for-the-badge&logo=microsoftword&logoColor=white" alt="Word DOCX"></a>
    <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%20x64-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"></a>
    <a href="#"><img src="https://img.shields.io/badge/UI-Custom%20Tkinter%20HUD-FF6F00?style=for-the-badge" alt="Tkinter HUD"></a>
    <a href="#"><img src="https://img.shields.io/badge/Architecture-State--Return%20Loop-00C853?style=for-the-badge" alt="Architecture"></a>
  </p>

  <br />

  <img src="public_images/Expanded_UI.png" alt="SpectraNote Expanded Floating Toolbar" width="850" />
  
  <p><sub><i>Fig 1.0: SpectraNote Full Floating Interface (Left Utilities • Center Drag/Toggle • Right Formatting)</i></sub></p>

  <img src="public_images/Collapsed_UI.png" alt="SpectraNote Collapsed Ghost Mode" width="140" />
  
  <p><sub><i>Fig 1.1: Collapsed Minimalist Pill — zero distraction, ready on demand</i></sub></p>

</div>

---

## 🧭 Table of Contents

- [💡 The Problem & The Solution](#-the-problem--the-solution)
- [✨ Key Features](#-key-features)
- [🧩 Architecture & Design Decisions](#-architecture--design-decisions)
- [🛠️ Technical Challenges & Creative Solutions](#-technical-challenges--creative-solutions)
- [📁 Project Directory Structure](#-project-directory-structure)
- [🎮 Toolbar Controls & Cheatsheet](#-toolbar-controls--cheatsheet)
- [🚀 Quickstart & Installation](#-quickstart--installation)
- [🔮 Roadmap](#-roadmap)

---

## 💡 The Problem & The Solution

### The Friction of Traditional Research
```
[ Read Article ] ──> [ Select Text ] ──> [ Ctrl+C ] ──> [ Alt+Tab to Word ]
                           ▲                                      │
                           │                                      ▼
                   [ Context Loss ] <── [ Style/Fix Format ] <─── [ Ctrl+V ]
```
Every time you switch between browsers, PDF viewers, video streams, and Microsoft Word:
1. **Focus breaks** due to repeated window context switching.
2. **Clipboard history gets polluted** and formatting gets lost.
3. **Pasted text requires manual styling** (H1, bold, list bullet indents).
4. **Snipping and embedding images** requires saving temp files or tedious manual paste/resize loops.

---

### The SpectraNote Experience
```
[ Highlight Text / Area ] ──> [ Click SpectraNote Floating Button ] ──> [ Instantly Formatted in DOCX ]
                                      (Zero Window Switching)
```
SpectraNote floats silently above your open windows. You simply highlight text or an on-screen visual anywhere, tap a single HUD button, and SpectraNote extracts, formats, and writes the structured block directly into your active Microsoft Word `.docx` file **without ever deselecting your active window**.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 👻 **Ghost HUD Window (`WS_EX_NOACTIVATE`)** | Borderless, transparent floating toolbar built with low-level Win32 hooks that **never steals focus** from your browser or PDF reader. |
| ✍️ **1-Click Semantic Word Formatting** | Instantly appends selected text as `Normal`, `Heading 1`, `Heading 2`, `Bold`, `Italic`, `Underline`, or `List Bullet` into your document. |
| ✂️ **Multi-Shape Snipping Tool** | Built-in high-resolution screen capture supporting **Rectangular**, **Circular**, and **Freehand Lasso** selections with automatic alpha-masking and Word insertion. |
| 📺 **YouTube Research Injector** | Pulls real-time video suggestions with **zero API keys** via direct Innertube querying. Features a responsive preview modal with live browser preview (`↗`) and structured `- Title \|\| Channel` document formatting. |
| 🌐 **Instant Web Search** | Automatically captures highlighted terms and launches focused web search queries in your default browser. |
| 🔄 **In-Flight Note Switching (`new_note`)** | Switch destination documents or generate a fresh note file mid-session without restarting the engine. |
| 🖥️ **Adaptive Multi-Monitor Scaling** | Automatically reads monitor bounds via `screeninfo` and clamps drag boundaries seamlessly across displays. |
| 🔕 **System Tray Background Daemon** | Runs unobtrusively in the Windows system tray with quick-launch and graceful shutdown triggers. |

---

## 🧩 Architecture & Design Decisions

SpectraNote is engineered around a **Decoupled 3-Layer Modular Architecture** combined with a **State-Return Loop Engine**.

<div align="center">
  <img src="public_images/SpectraNote%20Architecture.png" alt="SpectraNote Architecture Diagram" width="850" />
</div>

---

## 🛠️ Technical Challenges & Creative Solutions

### 1. The Active Focus Hijacking Challenge
* **The Problem**: Standard GUI windows in Python (Tkinter, PyQt) automatically request OS focus upon creation or user interaction. Clicking a floating toolbar would deselect text in the browser/PDF, causing clipboard extraction to fail.
* **The Solution**: We tapped directly into the Windows User32 Subsystem using `ctypes`:
  ```python
  # Apply WS_EX_NOACTIVATE style so window never steals window focus
  GWL_EXSTYLE = -20
  WS_EX_NOACTIVATE = 0x08000000
  style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
  ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_NOACTIVATE)
  ```

---

### 2. Tkinter Event-Loop Blocking & State-Return Engine
* **The Problem**: Long document I/O operations, image rendering, or network requests inside Tkinter's `mainloop()` cause the dreaded Windows *"Not Responding"* UI freeze.
* **The Solution**: SpectraNote uses a **State-Return Execution Cycle**:
  1. The toolbar renders on a lightweight `Toplevel` and enters a non-blocking wait.
  2. On user action, it updates `AppData.style` and immediately tears down the local widget tree.
  3. Control falls back to `runner.py` to execute document writes, screen captures, or API queries.
  4. Once complete, the toolbar cleanly re-instantiates in milliseconds.

---

### 3. OpenXML Native Hyperlink Injection
* **The Problem**: `python-docx` lacks out-of-the-box support for generating interactive, styled hyperlinks in document paragraphs without raw XML.
* **The Solution**: We built a custom OpenXML injection utility (`doc_task/hyperlink_helper.py`) that binds document relationships directly:
  ```python
  # Formats run with clean modern blue (#1D4ED8) and single underline
  r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
  hyperlink = OxmlElement('w:hyperlink')
  hyperlink.set(qn('r:id'), r_id)
  ```

---

### 4. Zero-Key YouTube Encapsulation & Rich Formatter
* **The Problem**: Requiring users to configure a Google Cloud Console account and generate API keys creates massive onboarding friction. Furthermore, raw URLs appended to documents lacked context (titles, channels).
* **The Solution**: 
  1. We encapsulated the search engine using YouTube's direct public Innertube endpoint (`/youtubei/v1/search`), achieving keyless suggestions with thumbnail and channel metadata.
  2. Built a responsive, mouse-resizable preview dialog with an instant `↗` browser launcher.
  3. Structured Word output to include bold title headers, author channels, and cleanly indented hyperlinks:
     ```text
     YouTube Suggestions for 'QUERY':
     - VIDEO_TITLE   ||  CHANNEL_NAME
         https://www.youtube.com/watch?v=...
     ```

---

### 5. In-Flight Workspace Switcher (`new_note`)
* **The Problem**: Switching target documents mid-session without restarting background daemons or crashing Tkinter with duplicate root instances.
* **The Solution**: Parameterized `start_folder_selection(app_data, parent=root, is_startup=False)`. During runtime, it launches as a transient modal with `grab_set()` and `wait_window()`. If the user closes `[X]`, it safely cancels without modifying `AppData` or triggering `sys.exit`.

---

## 📁 Project Directory Structure

```text
SpectraNote/
├── 📜 runner.py                    # Main Lifecycle & State-Return Engine
├── 🚀 app.bat                      # Silent launcher for SpectraNote
├── 🐛 app_with_log_window.bat      # Debug launcher (shows terminal logs)
├── 📦 appdata.py                   # Central State Management & Path Config
├── 📋 requirements                 # Project Dependency Declarations
├── 🔒 .env.example                 # Environment Variable Template
│
├── 🧠 handlers/                    # Action & Business Logic Handlers
│   ├── __init__.py
│   ├── yt_handler.py               # YouTube Search & Link Injection Orchestrator
│   ├── summary_handler.py          # On-Device T5 Abstractive Summarization Orchestrator
│   └── web_search_handler.py       # Instant Web Search Dispatcher
│
├── 🎨 gui/                         # Pure Presentation & UI Components
│   ├── gui_runner.py               # Floating SpectraToolbar Controller
│   ├── gui_layout.py               # Responsive Screen Measurements & Anchor Map
│   ├── gui_loader.py               # Transparent PNG Asset & Icon Loader
│   ├── gui_destination_selector.py # Startup & In-Flight Workspace Selector
│   ├── gui_yt_selector.py          # YouTube Suggestions Modal Selector
│   └── assets/                     # High-DPI UI Asset Library
│
├── 📸 SnapShot_task/               # Vision & Screen Capture Suite
│   ├── SS_auto_doc_appending.py    # Multi-Shape Snipping Tool (Rect, Circle, Freehand)
│   ├── image_appender.py           # Auto-Scaling Image Importer for Word
│   └── assets/                     # Snipping Tool HUD Controls
│
├── 📄 doc_task/                    # Document Manipulation & OpenXML Suite
│   ├── doc_manager.py              # Word File Creation & Validation
│   ├── operation.py                # Paragraph Styler (H1, H2, Bold, Italic, Bullet)
│   ├── summary_helper.py           # Word Summary Paragraph Generator
│   ├── hyperlink_helper.py         # OpenXML Hyperlink & URL Appender
│   └── text_extractor.py           # Native Clipboard Extraction Driver
│
├── 🔕 task_bar_menu/               # System Integration & Daemons
│   ├── tray_icon.py                # Windows System Tray Daemon (pystray)
│   └── icon.png                    # Tray Icon Asset
│
└── 🖼️ public_images/               # Documentation & Showcase Media
```

---

## 🎮 Toolbar Controls & Cheatsheet

<div align="center">
  <img src="public_images/Expanded_UI.png" width="800" alt="Toolbar Guide" />
</div>

<br>

### 🔹 Left Panel — Utilities & Actions
| Icon | Action | Description |
| :---: | :--- | :--- |
| 📁 | **Open Folder** | Opens the folder containing your active `.docx` file in Windows Explorer. |
| 📄 | **Open File** | Instantly launches the active `.docx` file in Microsoft Word. |
| 📝 | **New Note** | Opens the workspace selector to switch or create another document. |
| ⚡ | **Summary** | Generates an on-device abstractive summary of highlighted text and injects it into your document. |
| 🌐 | **Web Search** | Encodes highlighted text and triggers a browser web search. |
| ✂️ | **Snapshot** | Launches the multi-shape snipping tool to capture and embed images. |
| ▶️ | **YouTube** | Searches YouTube for highlighted text and embeds chosen video links. |

### 🔹 Center Panel — Navigation & Controls
| Icon | Action | Description |
| :---: | :--- | :--- |
| ◀️ / ▶️ | **Toggle Panels** | Collapses left/right toolbars into a micro pill HUD. |
| ✥ | **Drag Anchor** | Smooth drag handle with multi-monitor boundary clamping. |

### 🔹 Right Panel — Semantic Text Formats
| Icon | Format | Word Style Output |
| :---: | :--- | :--- |
| **P** | **Normal** | Inserts text as clean standard paragraph (`Normal`). |
| **I** | **Italic** | Inserts text with italic emphasis. |
| **B** | **Bold** | Inserts text with strong bold weighting. |
| **H1** | **Heading 1** | Formats text with major section header styling. |
| **H2** | **Heading 2** | Formats text with sub-section header styling. |
| **•** | **Bullet** | Formats text as an indented list item (`List Bullet`). |
| **✕** | **Exit** | Gracefully closes the toolbar and stops tray daemons. |

---

## 🚀 Quickstart & Installation

### Prerequisites
* **Operating System**: Windows 10 or Windows 11
* **Python**: `3.8+` (Recommended: Python 3.10 / 3.11)
* **Office Suite**: Microsoft Word or any `.docx`-compatible viewer

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/SpectraNote.git
cd SpectraNote
```

### 2. Set Up a Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements
```

### 4. Launch SpectraNote
You can launch the app directly using Python:
```bash
python runner.py
```
**Alternatively, use the provided batch launchers (Windows):**
- **`app.bat`**: Launches SpectraNote silently in the background (no terminal window).
- **`app_with_log_window.bat`**: Launches SpectraNote with a visible terminal for debugging and viewing logs.

---

## 🔮 Roadmap

- [x] **Modular 3-Tier Layering (`handlers/`, `gui/`, `doc_task/`)**
- [x] **In-Flight Document Switching (`new_note`)**
- [x] **Multi-Shape Screen Capture with Alpha Masks**
- [x] **Native OpenXML Hyperlink Generation**
- [x] **On-Device T5 Abstractive Summarization**
- [ ] **Next-Gen Modern Web UI Framework Transition**
- [ ] **Live side by side word file editing as currently `doc_task` not work when word file is open** 
- [ ] **Real-Time Text Translation before Document Injection**
- [ ] **Context-Aware AI Assistant (Sidebar Copilot)**
- [ ] **Cloud Workspace Sync (Google Docs & Notion API Integration)**

