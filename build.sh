#!/usr/bin/env bash
set -e

TARGET="${1:-linux}"
TARGET=$(echo "$TARGET" | tr '[:upper:]' '[:lower:]')

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Building Notepad for target: $TARGET ==="

# Use a local virtual environment (system Python is externally managed)
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

ICON_FLAG=""
if [ -f "note.ico" ]; then
    ICON_FLAG="--icon=note.ico --add-data=note.ico:."
fi

case "$TARGET" in
    linux)
        echo "Building Linux executable..."
        pyinstaller --noconfirm --onefile --windowed --name "Notepad" $ICON_FLAG Notepad.py
        echo "Build complete: dist/Notepad"
        ;;
    windows)
        echo "Building Windows executable..."
        if command -v wine &> /dev/null; then
            wine pyinstaller --noconfirm --onefile --windowed --name "Notepad" --icon=note.ico --add-data="note.ico;." Notepad.py
            echo "Build complete via Wine: dist/Notepad.exe"
        else
            pyinstaller --noconfirm --onefile --windowed --name "Notepad.exe" $ICON_FLAG Notepad.py
            echo "Build finished: dist/Notepad.exe"
        fi
        ;;
    *)
        echo "Unknown target: $TARGET. Allowed: linux, windows"
        exit 1
        ;;
esac
