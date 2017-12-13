from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Treeview, Progressbar

import os

from Observer import Observer


class View(Observer):
    def __init__(self, controller):
        self.controller = controller
        self.controller.set_observer(self)
        self.root = Tk()
        self.root.title("Search Engine By: Alon and Maor")
        self.docs_entry = Entry(self.root)
        self.docs_entry['width'] = 50
        self.posting_entry = Entry(self.root)
        self.posting_entry['width'] = 50
        self.to_stem = False
        self.stem_checkbutton = Checkbutton(self.root, text="stemming", command=self.change_stem_state)
        self.progress_bar = Progressbar(self.root, orient=HORIZONTAL, length=200, mode='determinate')
        self.start_btn = Button(text="Start", fg="blue", command=self.start_indexing)
        self.reset_btn = Button(text="Reset process", fg="red", command=self.reset_data)
        self.dictionary_btn = Button(text="Show dictionary", fg="red", command=self.display_dictionary)
        self.cache_btn = Button(text="Show cache", fg="red", command=self.display_cache)
        self.status_bar = Label(self.root)
        self.status_bar_text = StringVar()
        self.status_bar['textvariable'] = self.status_bar_text
        self.status_bar_text.set('Status:')
        self.create_view()

    def start(self):
        self.root.mainloop()

    def create_view(self):
        theme_label = Label(self.root, text="Search Engine", bg="blue", fg="white")
        theme_label.grid(row=0, column=1)
        doc_label = Label(self.root, text="Documents and Stop-Words:")
        docs_btn = Button(self.root, text="browse", command=self.docs_browse_location)
        posting_label = Label(self.root, text="Posting and Dictionary:")
        posting_btn = Button(self.root, text="browse", command=self.posting_browse_location)
        doc_label.grid(row=1, sticky=E)
        posting_label.grid(row=2, sticky=E)
        self.docs_entry.grid(row=1, column=1)
        self.posting_entry.grid(row=2, column=1)
        docs_btn.grid(row=1, column=2)
        posting_btn.grid(row=2, column=2)
        self.start_btn.grid(row=5, column=1)
        self.reset_btn.grid(row=6, column=0)
        self.reset_btn['state'] = 'disabled'
        self.cache_btn.grid(row=6, column=1)
        self.dictionary_btn.grid(row=6, column=2)
        reset_btn = Button(text="Save dictionary and cache")
        reset_btn.grid(row=7, column=1)
        cache_btn = Button(text="Upload dictionary and cache")
        cache_btn.grid(row=7, column=2)
        self.stem_checkbutton.grid(row=5, column=0)
        self.status_bar.grid(row=8, column=0, columnspan=3, sticky=W)
        self.progress_bar.grid(row=9, column=0, columnspan=3, sticky=(W, E))

    def display_dictionary(self):
        term_dict = self.controller.get_dictionary()
        dictionary_display_window = Toplevel(self.root)
        term_table = Treeview(dictionary_display_window, columns=('term', 'sum_tf'))
        scroll_bar = Scrollbar(dictionary_display_window, orient=VERTICAL, command=term_table.yview)
        term_table['yscrollcommand'] = scroll_bar.set
        term_table.heading('term', text='Term')
        term_table.heading('sum_tf', text='Sum_tf')
        i = 1
        for term in term_dict:
            term_table.insert('', 'end', text=str(i), values=(term, str(term_dict[term]['sum_tf'])))
            i += 1

        term_table.grid(column=0, row=0, sticky=(N, W, E, S))
        scroll_bar.grid(column=1, row=0, sticky=(N, S))

    def display_cache(self):
        cache = self.controller.get_cache()
        dictionary_display_window = Toplevel(self.root)
        term_table = Treeview(dictionary_display_window, columns=('key', 'data'))
        scroll_bar = Scrollbar(dictionary_display_window, orient=VERTICAL, command=term_table.yview)
        term_table['yscrollcommand'] = scroll_bar.set
        term_table.heading('key', text='Key')
        term_table.heading('data', text='Data')
        i = 1
        for key in cache:
            term_table.insert('', 'end', text=str(i), values=(key, str(cache[key])))
            i += 1

        term_table.grid(column=0, row=0, sticky=(N, W, E, S))
        scroll_bar.grid(column=1, row=0, sticky=(N, S))

    def docs_browse_location(self):
        dir_path = filedialog.askdirectory()
        self.docs_entry.delete(0, len(self.docs_entry.get()))
        self.docs_entry.insert(0, dir_path)

    def posting_browse_location(self):
        dir_path = filedialog.askdirectory()
        self.posting_entry.delete(0, len(self.posting_entry.get()))
        self.posting_entry.insert(0, dir_path)

    def start_indexing(self):
        self.start_btn['state'] = 'disabled'
        self.dictionary_btn['state'] = 'disabled'
        self.cache_btn['state'] = 'disabled'
        self.reset_btn['state'] = 'disabled'
        self.stem_checkbutton['state'] = 'disabled'
        self.progress_bar['value'] = 0
        self.controller.start_indexing(self.docs_entry.get(), self.posting_entry.get(), self.to_stem)

    def update(self, **kwargs):
        self.status_bar_text.set("Status: " + kwargs['status'])
        self.progress_bar.step(kwargs['progress'])
        if kwargs['done']:
            self.progress_bar['value'] = 100
            self.start_btn['state'] = 'normal'
            self.reset_btn['state'] = 'normal'
            self.dictionary_btn['state'] = 'normal'
            self.cache_btn['state'] = 'normal'
            self.stem_checkbutton['state'] = 'normal'
            self.display_summary(kwargs['summary'])

    def change_stem_state(self):
        if self.to_stem is False:
            self.to_stem = True
        else:
            self.to_stem = False

    def reset_data(self):
        self.controller.clean_postings()

    def display_summary(self, summary):
        display_window = Toplevel(self.root)
        message = "The number of terms indexed: {0:,} terms\n\n" \
                  "The number of Docs that were indexed: {1:,} Docs\n\n" \
                  "The size of the cache: {2:,} bytes\n\n" \
                  "The size of the terms postings: {3:,} bytes\n\n" \
                  "The size of the docs postings: {4:,} bytes\n\n" \
                  "The total time of the process: {5:,} seconds" \
                  "".format(summary['term_indexed'], summary['doc_indexed'], summary['cache_size'],
                            summary['terms_size'], summary['docs_size'], summary['total_time'])
        display_window.title("Information")
        display_window.geometry("300x300")
        w = Label(display_window, text=message)
        w.pack()
