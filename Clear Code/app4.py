#Tkinter Variables Video Start at 00:54:26 
import tkinter as tk
from tkinter import ttk

# defs

def button_func():
    print(string_var.get())
    string_var.set('some other text')

# window 
window = tk.Tk()
window.title('Tkinter Variables')

# Tkinter Variables
string_var = tk.StringVar()

# widgets
label = ttk.Label(master = window, text = 'Some text', textvariable=string_var)
label.pack(padx=10, pady=1)

entry = ttk.Entry(master = window, textvariable=string_var)
entry.pack(padx=10, pady=1)

button = ttk.Button(master = window, text = 'Button', command=button_func)
button.pack(padx=10, pady=1)

# run
window.mainloop()