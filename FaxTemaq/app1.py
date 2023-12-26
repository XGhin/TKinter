import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from datetime import datetime

class HourTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hour Tracker")

        self.style = Style(theme="superhero")  # Escolha o tema desejado

        self.services = {}  # Dicionário para armazenar informações dos serviços

        self.create_widgets()

    def create_widgets(self):
        # Frame para adicionar um novo serviço
        add_service_frame = ttk.Frame(self.root, padding="10")
        add_service_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(add_service_frame, text="Novo Serviço:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(add_service_frame, text="Nome do Serviço:").grid(row=1, column=0, pady=5)
        service_name_entry = ttk.Entry(add_service_frame)
        service_name_entry.grid(row=1, column=1, pady=5)

        ttk.Button(add_service_frame, text="Criar Serviço", command=lambda: self.create_service(service_name_entry.get())).grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para lançar horas
        log_hours_frame = ttk.Frame(self.root, padding="10")
        log_hours_frame.grid(row=1, column=0, padx=10, pady=10)

        ttk.Label(log_hours_frame, text="Lançar Horas:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(log_hours_frame, text="Serviço:").grid(row=1, column=0, pady=5)
        service_combobox = ttk.Combobox(log_hours_frame, values=list(self.services.keys()))
        service_combobox.grid(row=1, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Horas Trabalhadas:").grid(row=2, column=0, pady=5)
        hours_entry = ttk.Entry(log_hours_frame)
        hours_entry.grid(row=2, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Custo por Hora:").grid(row=3, column=0, pady=5)
        rate_entry = ttk.Entry(log_hours_frame)
        rate_entry.grid(row=3, column=1, pady=5)

        ttk.Button(log_hours_frame, text="Registrar Horas", command=lambda: self.log_hours(service_combobox.get(), hours_entry.get(), rate_entry.get())).grid(row=4, column=0, columnspan=2, pady=10)

    def create_service(self, service_name):
        # Cria um novo serviço
        if service_name not in self.services:
            self.services[service_name] = {"hours": [], "rate": 0}
            print(f"Serviço criado: {service_name}")
        else:
            print("Este serviço já existe.")

    def log_hours(self, service_name, hours, rate):
        # Registra as horas trabalhadas para um serviço
        if service_name in self.services:
            try:
                hours = float(hours)
                rate = float(rate)
                total_cost = hours * rate
                log_entry = {"date": datetime.now(), "hours": hours, "rate": rate, "total_cost": total_cost}
                self.services[service_name]["hours"].append(log_entry)
                print(f"Horas registradas para o serviço {service_name}: {hours}h, Custo total: R${total_cost}")
            except ValueError:
                print("Por favor, insira valores válidos para horas e custo por hora.")
        else:
            print("Este serviço não existe.")

# Inicializa o aplicativo
root = tk.Tk()
app = HourTrackerApp(root)
root.mainloop()