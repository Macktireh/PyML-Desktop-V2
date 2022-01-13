import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk


class LabelEntry:
    def __init__(self, root, label_text, textvar, show, x, y, width):
        self.root = root
        self.label_text = label_text
        self.textvar = textvar
        self.show = show
        self.x = x
        self.y = y
        self.width = width
        
        self.label = tk.Label(
            self.root, text=self.label_text, font=("Helvetica", 10)
        ).place(relx=0.07, rely=0.2)
        self.VarEntry = tk.StringVar()
        self.VarEntry.set(self.textvar)
        self.entry = tk.Entry(
            self.root, textvariable=self.VarEntry, width=40, show=self.show
        )
        self.entry.place(relx=self.x, rely=self.y)
        
    def get_value_entry(self):
        return self.entry.get()

    def set_value_entry(self, value):
        self.VarEntry.set(value)
