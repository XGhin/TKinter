import tkinter as tk
import customtkinter as ctk

# Defs
def baixar_video():
    print('vai tomar no cu renan')

# system config 
ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

# create a window 
window = ctk.CTk()

# linha 1 
linha1 = ctk.CTkFrame(master=window)
titulo = ctk.CTkLabel(linha1, text='Insert a YouTube link')
titulo.pack()
linha1.pack(padx = 10, pady = 5)

# linha 2
linha2 = ctk.CTkFrame(master=window)
entrada = ctk.CTkEntry(linha2, width=350)
entrada.pack()
linha2.pack(padx = 10, pady = 5)

# linha 3 
linha3 = ctk.CTkFrame(master=window)
botao = ctk.CTkButton(linha3, text="Download", command=baixar_video)
botao.pack()
linha3.pack(padx = 10, pady = 5)


# run 
window.mainloop()