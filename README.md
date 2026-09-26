# Notepad-by-Rajan

A modern, fast, and feature-rich text editor built with Python and Tkinter. Includes dark/light themes, live status bar statistics, zoom controls, find search dialog, and unsaved changes protection.

## Features

- **Dark & Light Themes:** Toggle seamlessly between dark and light editor themes.
- **Live Statistics:** Status bar shows active cursor position (line & column), total words, characters, and UTF-8 encoding.
- **Find Search:** Search text occurrences with highlighting.
- **Zoom In/Out:** Dynamic text zoom (`Ctrl++`, `Ctrl+-`, `Ctrl+0`).
- **Unsaved Changes Prompt:** Safety confirmation prevents accidental data loss.
- **Cross-Platform Builds:** Ready-to-use build scripts for Linux and Windows executables via PyInstaller.

## Project Structure

```text
Notepad-by-Rajan/
├── note.ico           # Application icon
├── Notepad.py         # Main entry point launcher
├── build.sh           # Linux/Bash build script
├── build.ps1          # Windows/PowerShell build script
└── src/
    ├── __init__.py    # Exports
    ├── config.py      # App constants, themes, typography
    ├── editor.py      # File I/O and text analytics engine
    ├── ui.py          # Tkinter interface, menus, shortcuts
    └── utils.py       # Resource path resolution helper
```

## Running Locally

Requires Python 3.8+:

```bash
python Notepad.py
```

## Building Executables

### Linux (Bash)
```bash
chmod +x build.sh
./build.sh linux
```
Output: `dist/Notepad`

### Windows (PowerShell)
```powershell
.\build.ps1 -Target windows
```
Output: `dist/Notepad.exe`
