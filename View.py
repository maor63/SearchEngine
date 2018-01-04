import pickle
# from tkinter import filedialog
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfilename
from tkinter.ttk import Treeview, Progressbar

import os

import time

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
        self.query_entry = Entry(self.root)
        self.query_entry['width'] = 50
        self.file_query_entry = Entry(self.root)
        self.file_query_entry['width'] = 50
        self.to_stem = False
        self.stem_checkbutton = Checkbutton(self.root, text="stemming", command=self.change_stem_state)
        self.extension_checkbutton = Checkbutton(self.root, text="Extension of query")
        self.summarize_checkbutton = Checkbutton(self.root, text="Summarize document")
        self.progress_bar = Progressbar(self.root, orient=HORIZONTAL, length=200, mode='determinate')
        self.start_btn = Button(text="Start", fg="blue", command=self.start_indexing)
        self.run_query = Button(text="Run", fg="blue", command=self.search_query)
        self.reset_btn = Button(text="Reset process", fg="red", command=self.reset_data)
        self.reset_result = Button(text="Reset result")
        self.dictionary_btn = Button(text="Show dictionary", fg="red", command=self.display_dictionary)
        self.cache_btn = Button(text="Show cache", fg="red", command=self.display_cache)
        self.save_btn = Button(text="Save dictionary and cache", command=self.save_dictionary_cache)
        self.upload_btn = Button(text="Upload dictionary and cache", command=self.upload_dictionary_cache)
        self.show_summary = Button(text="Show summary", command=self.display_summary)
        self.status_bar = Label(self.root)
        self.status_bar_text = StringVar()
        self.status_bar['textvariable'] = self.status_bar_text
        self.status_bar_text.set('Status:')
        self.summary = {}
        self.create_view()

    def start(self):
        '''
        start the user interface
        '''
        self.root.mainloop()

    def create_view(self):
        '''
        create the view window
        '''
        theme_label = Label(self.root, text="Search Engine", bg="blue", fg="white")
        theme_label.grid(row=0, column=1)
        doc_label = Label(self.root, text="Documents and Stop-Words:")
        docs_btn = Button(self.root, text="browse", command=self.docs_browse_location)
        posting_label = Label(self.root, text="Posting and Dictionary:")
        posting_btn = Button(self.root, text="browse", command=self.posting_browse_location)
        query_label = Label(self.root, text="query:")
        file_query_label = Label(self.root, text="file query:")
        file_run_query = Button(self.root, text="browse", command=self.query_file_browse_location)
        doc_label.grid(row=1, sticky=E)
        posting_label.grid(row=2, sticky=E)
        query_label.grid(row=10, sticky=E)
        self.run_query.grid(row=14, column=1)
        file_query_label.grid(row=13, sticky=E)
        file_run_query.grid(row=13, column=2)
        self.docs_entry.grid(row=1, column=1)
        self.posting_entry.grid(row=2, column=1)
        self.query_entry.grid(row=10, column=1)
        self.file_query_entry.grid(row=13, column=1)
        docs_btn.grid(row=1, column=2)
        posting_btn.grid(row=2, column=2)
        self.start_btn.grid(row=5, column=1)
        self.reset_btn.grid(row=6, column=0)
        self.reset_result.grid(row=15, column=0)
        self.reset_btn['state'] = 'disabled'
        self.cache_btn.grid(row=6, column=1)
        self.dictionary_btn.grid(row=6, column=2)
        self.show_summary.grid(row=7, column=0)
        self.show_summary['state'] = 'disabled'
        self.save_btn.grid(row=7, column=1)
        self.upload_btn.grid(row=7, column=2)
        self.stem_checkbutton.grid(row=5, column=0)
        self.extension_checkbutton.grid(row=10, column=2)
        self.summarize_checkbutton.grid(row=11, column=2)
        self.status_bar.grid(row=8, column=0, columnspan=3, sticky=W)
        self.progress_bar.grid(row=9, column=0, columnspan=3, sticky=(W, E))

    def display_dictionary(self):
        '''
        display the dictionary
        '''
        term_dict = self.controller.get_dictionary().term_dict
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
        '''
        display the cache
        '''
        cache = self.controller.get_cache()
        dictionary_display_window = Toplevel(self.root)
        term_table = Treeview(dictionary_display_window, columns=('term', 'file_pos', 'docs'))
        scroll_bar_y = Scrollbar(dictionary_display_window, orient=VERTICAL, command=term_table.yview)
        term_table['yscrollcommand'] = scroll_bar_y.set
        term_table.heading('term', text='Term')
        term_table.column('term', width=100)
        term_table.heading('file_pos', text='File_pos')
        term_table.column('file_pos', width=100)
        term_table.heading('docs', text='Docs')
        term_table.column('docs', width=800)
        i = 1
        for term in cache:
            term_table.insert('', 'end', text=str(i), values=(term, str(cache[term]['row']), cache[term]['docs']))
            i += 1

        term_table.grid(column=0, row=0, sticky=(N, W, E, S))
        scroll_bar_y.grid(column=1, row=0, sticky=(N, S))

    def docs_browse_location(self):
        '''
        ask the carpus and stopwords directory path
        '''
        dir_path = filedialog.askdirectory()
        self.docs_entry.delete(0, len(self.docs_entry.get()))
        self.docs_entry.insert(0, dir_path)

    def posting_browse_location(self):
        '''
        ask the posting directory
        '''
        dir_path = filedialog.askdirectory()
        self.posting_entry.delete(0, len(self.posting_entry.get()))
        self.posting_entry.insert(0, dir_path)


    def query_file_browse_location(self):
        '''
        ask the posting directory
        '''
        dir_path = filedialog.askdirectory()
        self.file_query_entry.delete(0, len(self.file_query_entry.get()))
        self.file_query_entry.insert(0, dir_path)

    def search_query(self):
        self.controller.search_query(self.query_entry.get())

    def start_indexing(self):
        '''
        change the display to disabled mode
        '''
        self.start_btn['state'] = 'disabled'
        self.dictionary_btn['state'] = 'disabled'
        self.cache_btn['state'] = 'disabled'
        self.reset_btn['state'] = 'disabled'
        self.save_btn['state'] = 'disabled'
        self.upload_btn['state'] = 'disabled'
        self.stem_checkbutton['state'] = 'disabled'
        self.show_summary['state'] = 'disabled'
        self.progress_bar['value'] = 0
        self.controller.start_indexing(self.docs_entry.get(), self.posting_entry.get(), self.to_stem)

    def update(self, **kwargs):
        '''
        change the display to normal mode
        '''
        if 'status' in kwargs and 'progress' in kwargs:
            self.status_bar_text.set("Status: " + kwargs['status'])
            self.progress_bar.step(kwargs['progress'])
        if "fail" in kwargs:
            self.start_btn['state'] = 'normal'
            self.stem_checkbutton['state'] = 'normal'
        elif kwargs['done']:
            self.progress_bar['value'] = 100
            self.start_btn['state'] = 'normal'
            self.reset_btn['state'] = 'normal'
            self.save_btn['state'] = 'normal'
            self.upload_btn['state'] = 'normal'
            self.dictionary_btn['state'] = 'normal'
            self.cache_btn['state'] = 'normal'
            self.stem_checkbutton['state'] = 'normal'
            self.summary = kwargs['summary']
            self.show_summary['state'] = 'normal'
            self.display_summary()

    def change_stem_state(self):
        '''
        change the process to stemming mode
        '''
        if self.to_stem is False:
            self.to_stem = True
        else:
            self.to_stem = False

    def reset_data(self):
        '''
        delete cch dic and posting files
        '''
        self.reset_btn['state'] = 'disabled'
        self.controller.clean_postings()

    def display_summary(self):
        '''
        display information about posting and cache files and runtime
        :param details about the process
        '''
        summary = self.summary
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

    def save_dictionary_cache(self):
        '''
        save the dictionary and the cache to the memory
        '''
        file_dictionary = asksaveasfile(mode='bw', defaultextension=".dic", title='Save Dictionary')
        if file_dictionary is None:
            return
        pickle.dump(self.controller.get_dictionary(), file_dictionary)
        file_dictionary.close()

        file_cache = asksaveasfile(mode='bw', defaultextension=".cch", title='Save Cache')
        if file_cache is None:
            return
        pickle.dump(self.controller.get_cache(), file_cache)
        file_cache.close()



    def upload_dictionary_cache(self):
        '''
        upload the dictionary and the cache from the memory
        '''
        file_dictionary = askopenfilename(filetypes=(("dictionary files", "*.dic"), ("dic", "*.*")),
                                          title='Upload Dictionary')
        if file_dictionary is '':
            return
        f = open(file_dictionary, "br")
        self.controller.set_dictionary(pickle.load(f))
        f.close()

        file_cache = askopenfilename(filetypes=(("dictionary files", "*.cch"), ("cch", "*.*")), title='Upload Cache')
        if file_cache is '':
            return
        f = open(file_cache, "br")
        self.controller.set_cache(pickle.load(f))
        f.close()
