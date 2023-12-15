# getting data from widgets
import tkinter as tk 
from tkinter import ttk

def button_func() :
    # get the content of the entry
    entry_text = entry.get()
    # update the label
    # label.configure(text = 'some other text')
    label['text'] = entry_text
    entry['state'] = 'disable'

    #lista as possiveis configs
    print(label.configure())

# window
window = tk.Tk()
window.title('Getting and setting widgets')

# widgets
label = ttk.Label(master = window, text = 'Some text')
label. pack()

entry = ttk.Entry(master = window)
entry. pack()

button = ttk.Button(master = window, text = 'The button', command = button_func)
button. pack()

# run
window.mainloop()
