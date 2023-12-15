import tkinter as tk
from tkinter import ttk

# funções 
def botao_teste():
    print("Hello")

# create a window
window = tk.Tk()
window.geometry("600x300")
window.title("Window and Widgets")

# ttk Widgets
label = ttk.Label(master = window, text = "This is a Test")
label.pack()

# create Widgets
text = tk.Text(master = window) 
text.pack()

# ttk Entry
entry = ttk.Entry(master = window)
entry.pack()

# label exercise 
exercise1 = ttk.Label(master = window, text = "My label")
exercise1.pack()

# ttk Button
button = ttk.Button(master= window, text = "Press me",command = botao_teste)
button.pack()




# run 
window.mainloop()