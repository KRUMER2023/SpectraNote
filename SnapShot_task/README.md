# Auto-Append Screenshot to Word Tool

## Overview
This tool allows users to take screenshots (Rectangle, Circle, or Freehand) which are automatically saved to a local temp directory and appended to a `test.docx` Microsoft Word document.

## Features
- **Capture Modes**: detailed selection modes (Rectangle, Circle, Free-form).
- **Auto-Save**: Screenshots are saved with timestamps in a `temp` folder.
- **Auto-Append**: Images are immediately added to `test.docx`.
- **Auto-Scale**: Images larger than 6 inches in width are automatically resized to fit standard document margins.
- **Fail-Safe**: Handles missing or corrupt Word documents by creating a new one.

## Technical Architecture

### 1. `SS_auto_doc_appending.py`
The main entry point. 
- Handles the GUI (Tkinter).
- Manages the overlay and screenshot capture (Pillow).
- Workflow: `Capture` -> `Save to Disk` -> `Append to Doc` -> `Exit`.

### 2. `image_appender.py`
A helper module for handling Word document operations.
- **Function**: `append_image_to_doc(image_path, doc_path)`
- Checks for `doc_path` existence.
- Creates a new `Document` if needed.
- Appends the image, enforcing a maximum width of 6 inches.
- Returns `(success, message)`.

## Usage
1. Run `SS_auto_doc_appending.py`.
2. Select a snip mode from the toolbar.
3. Select the area on screen.
4. The tool will close, and the image will be added to the Word document in the script's directory.
