import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self, obj):
        super().__init__()

        # Counter that we increment with each new entry
        self.currIid = 1

        # Show the user where they are in the tree
        self.breadcrumbs = tk.Label(self, text=">")
        self.breadcrumbs.pack(anchor=tk.W)

        self.tree = ttk.Treeview(self, columns=('#0', '#1', '#2'), height=30)
        self.tree.pack(fill=tk.BOTH)
        self.tree.insert('', tk.END, values=[str(type(obj)), ""], iid=0, open=True)
        
        # Compute breadcrumbs on button release
        self.tree.bind('<ButtonRelease-1>', self.computeBreadcrumbs)

        # Populate the treeview
        self.populate(0, obj)

    def computeBreadcrumbs(self, ev):
        items = []

        iid = int(self.tree.focus())

        while iid != 0:
            print(iid)
            print(self.tree.item(iid))
            items.insert(0, str(self.tree.item(iid)["values"][0]))

            iid = int(self.tree.parent(iid))

        self.breadcrumbs.config(text="> " + " > ".join(items))

    def insert(self, parent, values):
        """
        Insert an entry into the tree under a parent entry
        """

        # Insert at the end of the Treeview
        self.tree.insert('', tk.END, values=values, iid=self.currIid, open=False)
        # Move it under its parent
        self.tree.move(self.currIid, parent, tk.END)

        self.currIid += 1

        return self.currIid - 1

    def populate(self, parentIid, object):
        """
        Recursively populate the tree with a python object
        """

        if type(object) == dict:
            for key in object:
                valString = str(type(object[key])) if type(object[key]) in [dict, list] else str(object[key])

                i = self.insert(parentIid, [key, valString])
                self.populate(i, object[key])

        elif type(object) == list:
            for index, i in enumerate(object):
                valString = str(type(i)) if type(i) in [dict, list] else str(i)

                iid = self.insert(parentIid, [index, valString])
                self.populate(iid, i)
