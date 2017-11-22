from tkinter import filedialog
from tkinter import *
root = Tk()
root.title("Search Engine")


def openfile(event):
    root.fileName = filedialog.askopenfilename(filetypes=(("Python Stuff", ".PY"), ("All files", "*.*")))


theLabel = Label(root, text="Search Engine", bg="blue", fg="white")
theLabel.grid(row=0, column=1)

label_1 = Label(root, text="Documents and Stop-Words:")
button1 = Button(root, text="browse", bg="gray", fg="white")
button1.bind("<Button-1>", openfile)
label_2 = Label(root, text="Posting and Dictionary:")
button2 = Button(root, text="browse", bg="gray", fg="white")
button2.bind("<Button-1>", openfile)
entry_1 = Entry(root)
entry_2 = Entry(root)


label_1.grid(row=1, sticky=E)
label_2.grid(row=2, sticky=E)

entry_1.grid(row=1, column=1)
entry_2.grid(row=2, column=1)

button1.grid(row=1, column=2)
button2.grid(row=2, column=2)

button3 = Button(text="Start", fg="blue")
button3.grid(row=5, column=1)

button4 = Button(text="Reset process", fg="red")
button4.grid(row=6, column=0)

button5 = Button(text="Show cache", fg="red")
button5.grid(row=6, column=1)

button6 = Button(text="Show dictionary", fg="red")
button6.grid(row=6, column=2)

c = Checkbutton(root, text="stemming")
c.grid(row=5, column=0)

root.mainloop()
