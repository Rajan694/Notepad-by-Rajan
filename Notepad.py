import tkinter as tk
from src import NotepadUI

def main():
    root = tk.Tk()
    NotepadUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
