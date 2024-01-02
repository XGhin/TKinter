# Buttons - Video time = 01:06:10

import tkinter as tk 
from tkinter import ttk

# window
window = tk.Tk()
window.title('Buttons')
window.geometry('400x300')

    # widgets
# button
def button1_func():
    button_string.set('button 1 clicked')

button_string = tk.StringVar(value = 'string var button')
button1 = ttk.Button(window, text = 'Button 1', command = button1_func, textvariable= button_string)
button1.pack()

# checkbutton
check_var = tk.IntVar()
check = ttk.Checkbutton(window, 
                        text = 'Checkbox 1',
                        command=lambda: print(check_var.get()),
                        onvalue=10,
                        offvalue=20,
                        variable=check_var)
check.pack()

check2 = ttk.Checkbutton(window,
                         text='Checkbox 2',
                         command=lambda: print('test'))
check2.pack()
# radio buttons
radio_var = tk.StringVar()
radio1 = ttk.Radiobutton(window, 
                         text='Radio 1', 
                         value='radio 1',
                         variable=radio_var, 
                         command=lambda: print(radio_var.get()))
radio1.pack()
radio2 = ttk.Radiobutton(window, 
                         text='Radio 2', 
                         value=2,
                         variable=radio_var,
                         command=lambda: print(radio_var.get()))
radio2.pack()


vazio = ttk.Label(window, text='')
vazio.pack()
#exercise 
# radio buttons
radio_var = tk.StringVar()
radioA = ttk.Radiobutton(window, text='A', value='A', variable=radio_var, command=lambda: radio_var.set('A'))
radioA.pack()

radioB = ttk.Radiobutton(window, text='B', value='B', variable=radio_var, command=lambda: radio_var.set('B'))
radioB.pack()

# checkbox
def Checkbox_exercise_func():
    radio_var.set(10)
    print(radioA.get())
checkex_var = tk.BooleanVar()
checkbox_ex = ttk.Checkbutton(window,
                              onvalue=10,
                              text="Checkbox",
                              variable=radio_var,
                              command=Checkbox_exercise_func)
checkbox_ex.pack()

# run
window.mainloop()