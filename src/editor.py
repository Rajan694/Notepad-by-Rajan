import os

class EditorEngine:
    def __init__(self):
        self.current_file = None
        self.is_modified = False

    def load_file(self, filepath: str) -> str:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        self.current_file = filepath
        self.is_modified = False
        return content

    def save_file(self, filepath: str, content: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        self.current_file = filepath
        self.is_modified = False

    def get_stats(self, content: str) -> tuple[int, int, int]:
        lines = content.count("\n") + 1 if content else 0
        words = len(content.split()) if content.strip() else 0
        chars = len(content)
        return lines, words, chars

    @property
    def filename(self) -> str:
        if self.current_file:
            return os.path.basename(self.current_file)
        return "Untitled"
