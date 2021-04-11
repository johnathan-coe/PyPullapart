from tkinter import ttk
import tkinter as tk

FONT = ("Jetbrains Mono", 11)

def setup():
    s = ttk.Style()

    s.configure("dark.Treeview", foreground="white", background="#2a2a2a", fieldbackground="#2a2a2a", font=FONT)
    s.configure("dark.Label", foreground="white", background='#121212', anchor=tk.W, font=FONT)