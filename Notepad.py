import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
import sys


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def newfile():
    global file
    root.title("Notepad - Untitled")
    file = None
    text.delete(1.0, END)


def openfile():
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title("Notepad - " + os.path.basename(file))
        text.delete(1.0, END)
        f = open(file, "r")
        text.insert(1.0, f.read())
        f.close()


def savefile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                 filetypes=[("All Files", "*.*"),
                                            ("Text Documents", "*.txt")])
        if file == "":
            file = None

        else:
            try:
                f = open(file, "w")
                f.write(text.get(1.0, END))
                f.close()
            except Exception as e:
                messagebox.showerror("Notepad", "Select a file!!!")

            root.title("Notepad - " + os.path.basename(file))

    else:
        f = open(file, "w")
        f.write(text.get(1.0, END))
        f.close()


def exi():
    root.destroy()


def cut():
    text.event_generate(("<<Cut>>"))


def copy():
    text.event_generate(("<<Copy>>"))


def paste():
    text.event_generate(("<<Paste>>"))


def about():
    showinfo("Notepad", "Notepad by Rajan Kumar")


if __name__ == '__main__':
    root = Tk()
    root.title("Notepad")
    raj = resource_path("note.ico")
    root.wm_iconbitmap(raj)
    root.geometry("644x600")

    text = Text(root, font="lucida 13")
    file = None
    text.pack(expand=True, fill=BOTH)

    mbar = Menu(root)

    fmenu = Menu(mbar, tearoff=0)
    fmenu.add_command(label="New", command=newfile)
    fmenu.add_command(label="Open", command=openfile)
    fmenu.add_command(label="Save", command=savefile)
    fmenu.add_separator()
    fmenu.add_command(label="Exit", command=exi)
    mbar.add_cascade(label="File", menu=fmenu)

    emenu = Menu(mbar, tearoff=0)
    emenu.add_command(label="Cut", command=cut)
    emenu.add_command(label="Copy", command=copy)
    emenu.add_command(label="Paste", command=paste)
    mbar.add_cascade(label="Edit", menu=emenu)

    hmenu = Menu(mbar, tearoff=0)
    hmenu.add_command(label="About Notepad", command=about)
    mbar.add_cascade(label="Help", menu=hmenu)

    root.config(menu=mbar)

    scroll1 = Scrollbar(text)
    scroll1.pack(side=RIGHT, fill=Y)
    scroll1.config(command=text.yview,cursor="arrow")
    text.config(yscrollcommand=scroll1.set)

    root.mainloop()
