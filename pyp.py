import tkinter as tk
from tkinter import ttk
import theming

def obj_summary(obj):
    if type(obj) == dict:
        return "{}"
    elif type(obj) == list:
        return "[]"
    
    return str(obj)

class Window(tk.Tk):
    def __init__(self, obj):
        super().__init__()

        # Counter that we increment with each new entry
        self.currIid = 1

        theming.setup()

        # Show the user where they are in the tree
        self.breadcrumbs = ttk.Label(self, text=">", style="dark.Label")
        self.breadcrumbs.pack(fill=tk.X)

        self.tree = ttk.Treeview(self, style="dark.Treeview", columns=('#0', '#1', '#2'), height=30)
        #self.tree.tag_configure('row', background='#202945', foreground="white")
        self.tree.pack(fill=tk.BOTH)
        self.tree.insert('', tk.END, values=[str(type(obj)), ""], iid=0, open=True)
        
        # Compute breadcrumbs on button release
        self.tree.bind('<ButtonRelease-1>', self.computeBreadcrumbs)
        self.tree.bind('<KeyRelease>', self.computeBreadcrumbs)

        # Populate the treeview
        self.populate(0, obj)

    def computeBreadcrumbs(self, ev):
        if not self.tree.focus():
            return

        items = []

        # Get the selected entry
        iid = int(self.tree.focus())
      
        # Travel up the tree until we reach the root
        while iid != 0:
            key = self.tree.item(iid)["values"][0]
            items.insert(0, str(key))
            iid = int(self.tree.parent(iid))

        # Place the breadcrumbs in the label
        self.breadcrumbs.config(text="> " + " > ".join(items))

    def insert(self, parent, values):
        """
        Insert an entry into the tree under a parent entry
        """

        # Insert at the end of the Treeview
        self.tree.insert('', tk.END, values=values, iid=self.currIid, open=False,
                        tags=("row",))
        # Move it under its parent
        self.tree.move(self.currIid, parent, tk.END)

        self.currIid += 1

        return self.currIid - 1

    def populate(self, parentIid, object):
        """
        Recursively populate the tree with a python object
        """
        
        if type(object) in [dict, list]:
            indices = object.keys() if type(object) == dict else range(len(object))
            
            for index in indices:
                summary = obj_summary(object[index])
                iid = self.insert(parentIid, [index, summary])
                self.populate(iid, object[index])
