import tkinter as tk
import ttkbootstrap as ttk

# Window
window = tk.Tk()
window.title('Salario_TK_V2')
style = ttk.Style(theme='yeti')

horas_var = tk.IntVar()
minutos_var = tk.IntVar()
valor_var = tk.IntVar()
salario_var = tk.IntVar()

# Widgets em Def
class Widgets():
        
    def Label_Horas():
        horas_label = ttk.Label(linha1, text='Horas')
        horas_label.pack(side='left', padx= 5, pady= 5)

    def Label_Minutos():
        minutos_label = ttk.Label(linha1, text='Minutos')
        minutos_label.pack(side='left', padx= 5, pady= 5)

    def Entry_Horas():
        horas = ttk.Entry(linha1, width=10, justify='center', textvariable=horas_var)
        horas.selection_clear()
        horas.focus()
        horas.pack(side='left', padx= 5, pady= 5)


    def Entry_Minutos():
        minutos = ttk.Entry(linha1, width=10, justify='center', textvariable=minutos_var)
        minutos.pack(side='left', padx= 5, pady= 5)
        

    def Label_Valor():
        valor_label = ttk.Label(linha2, text='Valor por Hora')
        valor_label.pack(padx= 5, pady= 5)

    def Entry_Valor():
        valor = ttk.Entry(linha2, width=10, justify='center', textvariable=valor_var)
        valor.pack(padx= 5, pady= 5)
        

    def Button_Calcular():
        calcular = ttk.Button(linha3, text='Calcular', command=calcular_salario)
        calcular.pack(padx= 5, pady= 5)

    def Label_Salario():
        salario_label = ttk.Label(linha3, text='Seu Salario', textvariable=salario_var)
        salario_label.pack(padx= 5, pady= 5)

# Defs
def calcular_salario():
    horas = horas_var.get()
    minutos = minutos_var.get()
    valor = valor_var.get()
    salario = ((horas * 60) + minutos) * (valor / 60)
    salario_var.set(f'R$ {salario:.2f}')

# só pra manter o R$ na label_salario
calcular_salario()



# ADD Widgets na Tela
linha1 = ttk.Frame(window, padding=0)
linha1.pack(padx=5, pady=5)
Widgets.Label_Horas()
Widgets.Entry_Horas()
Widgets.Label_Minutos()
Widgets.Entry_Minutos()

linha2 = ttk.Frame(window, padding=0)
linha2.pack(padx=5, pady=5)
Widgets.Label_Valor()
Widgets.Entry_Valor()

linha3 = ttk.Frame(window, padding=0)
linha3.pack(padx=5, pady=5)
Widgets.Button_Calcular()
Widgets.Label_Salario()


# Run
window.mainloop()