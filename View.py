from tkinter import filedialog
from tkinter import *


class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = Tk()
        self.root.title("Search Engine")
        self.docs_entry = Entry(self.root)
        self.posting_entry = Entry(self.root)

        self.create_view()

    def start(self):
        self.root.mainloop()

    def create_view(self):
        theme_label = Label(self.root, text="Search Engine", bg="blue", fg="white")
        theme_label.grid(row=0, column=1)
        doc_label = Label(self.root, text="Documents and Stop-Words:")
        docs_btn = Button(self.root, text="browse")
        docs_btn.bind("<Button-1>", self.docs_browse_location)
        posting_label = Label(self.root, text="Posting and Dictionary:")
        posting_btn = Button(self.root, text="browse")
        posting_btn.bind("<Button-1>", self.posting_browse_location)
        doc_label.grid(row=1, sticky=E)
        posting_label.grid(row=2, sticky=E)
        self.docs_entry.grid(row=1, column=1)
        self.posting_entry.grid(row=2, column=1)
        docs_btn.grid(row=1, column=2)
        posting_btn.grid(row=2, column=2)
        start_btn = Button(text="Start", fg="blue", command=self.start_indexing)
        start_btn.grid(row=5, column=1)
        reset_btn = Button(text="Reset process", fg="red")
        reset_btn.grid(row=6, column=0)
        cache_btn = Button(text="Show cache", fg="red")
        cache_btn.grid(row=6, column=1)
        dictionary_btn = Button(text="Show dictionary", fg="red")
        dictionary_btn.grid(row=6, column=2)
        c = Checkbutton(self.root, text="stemming")
        c.grid(row=5, column=0)

    def docs_browse_location(self, event):
        dir_path = filedialog.askdirectory()
        self.docs_entry.delete(0, len(self.docs_entry.get()))
        self.docs_entry.insert(0, dir_path)

    def posting_browse_location(self, event):
        dir_path = filedialog.askdirectory()
        self.posting_entry.delete(0, len(self.posting_entry.get()))
        self.posting_entry.insert(0, dir_path)

    def start_indexing(self):
        self.controller.start_indexing(self.docs_entry.get(), self.posting_entry.get())

    def update(self):
        pass
