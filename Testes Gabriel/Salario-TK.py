import tkinter as tk 
import ttkbootstrap as ttk 

# defs
def Salario():
    total_horas = int(horas.get())
    total_horas = int(total_horas) * 60
    total_minutos = int(minutos.get())
    total_minutos = int(total_minutos) + int(total_horas)
    salario_total = total_minutos * 0.3333333333333333
    salario_total = format(salario_total, '.2f')
    resultado_string.set(salario_total)

# Window 
window = tk.Tk()

# linha 1
linha1 = ttk.Frame(master = window)
saudacao = ttk.Label(master = linha1, text='Bem-vindo!')
saudacao.pack()
linha1.pack()

# linha 2
linha2 = ttk.Frame(master=window)
Thoras = ttk.Label(master=linha2, text="Horas")
Thoras.pack(side='left', padx=60)
Tminutos = ttk.Label(master=linha2, text="Minutos")
Tminutos.pack(side='right', padx=60)
linha2.pack()

# linha 3
linha3 = ttk.Frame(master = window)
horas = ttk.Entry(master = linha3)
horas.pack(side='left', padx=10)
minutos = ttk.Entry(master = linha3)
minutos.pack(side='right', padx=10)
linha3.pack()

# linha 4
linha4 = ttk.Frame(master=window)
calcular = ttk.Button(master=linha4, text="Cmalcular Salario", command=Salario)
calcular.pack()
linha4.pack(pady=10)

# linha 5
linha5 = ttk.Frame(master = window)
resultado_string = tk.StringVar()
resultado = ttk.Label(master=linha5, text="", textvariable=resultado_string, font='Calibri 16 bold')
resultado.pack()
linha5.pack(pady=2)


# run 
window.mainloop()