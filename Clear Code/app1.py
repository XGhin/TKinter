import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk

def convert():
    mile_input = entryInt.get()
    km_output = mile_input * 1.60934
    output_string.set(km_output)
    


#window 
window = tk.Tk()
window.title("App-1")
window.geometry("300x150")

# tittle
tittle_label = ttk.Label(master = window, text= "Miles to Kilometers", font="Calibri 24 bold")
tittle_label.pack()

# input field
input_frame = ttk.Frame(master = window, )
entryInt = tk.IntVar()
entry = ttk.Entry(master = input_frame, textvariable = entryInt)
entry.pack(side = "left", padx = 5)
button = ttk.Button(master = input_frame, text = "Convert", command= convert, )
button.pack(side = "left")
input_frame.pack(pady = 10)

# output
output_string = tk.StringVar()
output_label = ttk.Label(master = window, 
                        text = "Output",
                        font = "Calibri 24",
                        textvariable = output_string)
output_label.pack(pady=10)


# run
window.mainloop()