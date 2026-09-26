import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from . import config
from .editor import EditorEngine
from .utils import resource_path

class NotepadUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = EditorEngine()
        self.current_theme = "dark"
        self.font_size = config.FONT_SIZE

        self._setup_window()
        self._create_widgets()
        self._create_menu()
        self._apply_theme()
        self._bind_events()
        self._update_title()

    def _setup_window(self):
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(500, 400)
        self.root.protocol("WM_DELETE_WINDOW", self._on_exit)

        icon_path = resource_path(config.ICON_FILE)
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    def _create_widgets(self):
        # Editor & Scrollbar Container
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        self.scrollbar = tk.Scrollbar(main_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            main_frame,
            font=(config.FONT_FAMILY, self.font_size),
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            undo=True,
            wrap="word",
            yscrollcommand=self.scrollbar.set
        )
        self.text_area.pack(side="left", expand=True, fill="both")
        self.scrollbar.config(command=self.text_area.yview)

        # Status Bar
        self.status_bar = tk.Frame(self.root, height=26)
        self.status_bar.pack(side="bottom", fill="x")

        self.status_pos = tk.Label(
            self.status_bar,
            text="Ln 1, Col 1",
            font=("Segoe UI", 9),
            anchor="w",
            padx=10
        )
        self.status_pos.pack(side="left")

        self.status_info = tk.Label(
            self.status_bar,
            text="0 words | 0 chars | UTF-8",
            font=("Segoe UI", 9),
            anchor="e",
            padx=10
        )
        self.status_info.pack(side="right")

    def _create_menu(self):
        self.menu_bar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self._new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self._open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self._save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self._save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4", command=self._on_exit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.text_area.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", accelerator="Ctrl+F", command=self._find_text)
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self._select_all)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Zoom In", accelerator="Ctrl++", command=self._zoom_in)
        view_menu.add_command(label="Zoom Out", accelerator="Ctrl+-", command=self._zoom_out)
        view_menu.add_command(label="Reset Zoom", accelerator="Ctrl+0", command=self._reset_zoom)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Theme (Dark/Light)", command=self._toggle_theme)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About Modern Notepad", command=self._about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=self.menu_bar)

    def _apply_theme(self):
        theme = config.DARK_THEME if self.current_theme == "dark" else config.LIGHT_THEME
        self.text_area.config(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["cursor"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"]
        )
        self.status_bar.config(bg=theme["status_bg"])
        self.status_pos.config(bg=theme["status_bg"], fg=theme["status_fg"])
        self.status_info.config(bg=theme["status_bg"], fg=theme["status_fg"])

    def _toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme()

    def _bind_events(self):
        self.text_area.bind("<KeyRelease>", self._on_text_change)
        self.text_area.bind("<ButtonRelease-1>", self._on_cursor_move)

        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind("<Control-S>", lambda e: self._save_as_file())
        self.root.bind("<Control-f>", lambda e: self._find_text())
        self.root.bind("<Control-plus>", lambda e: self._zoom_in())
        self.root.bind("<Control-equal>", lambda e: self._zoom_in())
        self.root.bind("<Control-minus>", lambda e: self._zoom_out())
        self.root.bind("<Control-0>", lambda e: self._reset_zoom())

    def _on_text_change(self, event=None):
        self.engine.is_modified = True
        self._update_title()
        self._on_cursor_move()

    def _on_cursor_move(self, event=None):
        pos = self.text_area.index(tk.INSERT)
        row, col = pos.split(".")
        self.status_pos.config(text=f"Ln {row}, Col {int(col) + 1}")

        content = self.text_area.get("1.0", "end-1c")
        _, words, chars = self.engine.get_stats(content)
        self.status_info.config(text=f"{words} words | {chars} chars | UTF-8")

    def _update_title(self):
        mod = "*" if self.engine.is_modified else ""
        self.root.title(f"{mod}{self.engine.filename} - {config.APP_NAME}")

    def _confirm_save(self) -> bool:
        if not self.engine.is_modified:
            return True
        resp = messagebox.askyesnocancel(
            "Save Changes?",
            f"Do you want to save changes to {self.engine.filename}?"
        )
        if resp is True:
            return self._save_file()
        elif resp is False:
            return True
        return False

    def _new_file(self):
        if self._confirm_save():
            self.text_area.delete("1.0", tk.END)
            self.engine.current_file = None
            self.engine.is_modified = False
            self._update_title()
            self._on_cursor_move()

    def _open_file(self):
        if self._confirm_save():
            path = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Documents (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")]
            )
            if path:
                content = self.engine.load_file(path)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self._update_title()
                self._on_cursor_move()

    def _save_file(self) -> bool:
        if not self.engine.current_file:
            return self._save_as_file()
        try:
            content = self.text_area.get("1.0", "end-1c")
            self.engine.save_file(self.engine.current_file, content)
            self._update_title()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")
            return False

    def _save_as_file(self) -> bool:
        path = filedialog.asksaveasfilename(
            initialfile=self.engine.filename,
            defaultextension=".txt",
            filetypes=[("Text Documents (*.txt)", "*.txt"), ("All Files (*.*)", "*.*")]
        )
        if path:
            try:
                content = self.text_area.get("1.0", "end-1c")
                self.engine.save_file(path, content)
                self._update_title()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
                return False
        return False

    def _select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)

    def _find_text(self):
        search_query = simpledialog.askstring("Find Text", "Enter text to search:")
        if not search_query:
            return

        self.text_area.tag_remove("match", "1.0", tk.END)
        matches = 0
        start = "1.0"
        while True:
            start = self.text_area.search(search_query, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(search_query)}c"
            self.text_area.tag_add("match", start, end)
            start = end
            matches += 1

        self.text_area.tag_config("match", background="#EAB308", foreground="#000000")
        if matches == 0:
            messagebox.showinfo("Find", f"No occurrences of '{search_query}' found.")

    def _zoom_in(self):
        self.font_size = min(36, self.font_size + 2)
        self.text_area.config(font=(config.FONT_FAMILY, self.font_size))

    def _zoom_out(self):
        self.font_size = max(8, self.font_size - 2)
        self.text_area.config(font=(config.FONT_FAMILY, self.font_size))

    def _reset_zoom(self):
        self.font_size = config.FONT_SIZE
        self.text_area.config(font=(config.FONT_FAMILY, self.font_size))

    def _about(self):
        messagebox.showinfo(
            "About",
            f"{config.APP_NAME}\nA modern, lightweight text editor built with Python & Tkinter."
        )

    def _on_exit(self):
        if self._confirm_save():
            self.root.destroy()
