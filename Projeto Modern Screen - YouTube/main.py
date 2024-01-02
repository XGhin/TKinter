import tkinter
import customtkinter as ctk

#defs 
def download_func():
    pass

# system config
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# create a window
window = ctk.CTk()
window.geometry("720x480")
window.title('Youtube Downloader')

#linha 1 
title = ctk.CTkLabel(window, text='Insert a youtube link')
title.pack(padx=10, pady=10)

#link
url_var = tkinter.StringVar()
link = ctk.CTkEntry(window, width=350, height=40, textvariable=url_var)
link.pack()

# Download Button
button = ctk.CTkButton(window, text="Download", command=download_func)
button.pack(pady=10, padx=10)

# RUN
window.mainloop()
