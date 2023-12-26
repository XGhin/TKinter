import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from datetime import datetime
import sqlite3

class ServiceManager:
    def __init__(self):
        # Conectar ao banco de dados SQLite (criará o arquivo se não existir)
        self.conn = sqlite3.connect('hour_tracker.db')
        self.create_tables()
        self.services = self.load_services()

    def create_tables(self):
        # Criar tabelas se não existirem
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,  -- Adicionando a restrição UNIQUE para evitar nomes duplicados
                    rate REAL NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY,
                    service_id INTEGER,
                    date TEXT NOT NULL,
                    hours REAL NOT NULL,
                    rate REAL NOT NULL,
                    total_cost REAL NOT NULL,
                    FOREIGN KEY (service_id) REFERENCES services (id)
                )
            ''')

    def load_services(self):
        # Carregar serviços existentes do banco de dados
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM services")
            services = cursor.fetchall()
            service_names = [service[0] for service in services]
            for service_name in service_names:
                print(f"Serviço carregado: {service_name}")
            return service_names

    def create_service(self, service_name, rate):
        # Cria um novo serviço e insere no banco de dados
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO services (name, rate) VALUES (?, ?)", (service_name, rate))
            print(f"Serviço criado: {service_name}")
        except sqlite3.IntegrityError:
            print(f"Este serviço já existe: {service_name}")

    def log_hours(self, service_name, hours, rate):
        # Registra as horas trabalhadas para um serviço e insere no banco de dados
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, rate FROM services WHERE name=?", (service_name,))
            result = cursor.fetchone()
            if result:
                service_id, service_rate = result
                try:
                    hours = float(hours)
                    rate = float(rate)
                    total_cost = hours * rate
                    cursor.execute("INSERT INTO logs (service_id, date, hours, rate, total_cost) VALUES (?, ?, ?, ?, ?)",
                                   (service_id, datetime.now(), hours, rate, total_cost))
                    print(f"Horas registradas para o serviço {service_name}: {hours}h, Custo total: R${total_cost}")
                except ValueError:
                    print("Por favor, insira valores válidos para horas e custo por hora.")
            else:
                print("Este serviço não existe.")

    def get_service_info(self, service_name):
        # Obtém informações sobre um serviço, incluindo horas e custos totais
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM services WHERE name=?", (service_name,))
            result = cursor.fetchone()
            if result:
                service_id = result[0]
                cursor.execute("SELECT SUM(hours), SUM(total_cost) FROM logs WHERE service_id=?", (service_id,))
                result = cursor.fetchone()
                total_hours, total_cost = result if result else (0, 0)
                return total_hours, total_cost
            else:
                return 0, 0

    def __del__(self):
        # Fechar a conexão com o banco de dados quando a instância é destruída
        self.conn.close()

class HourTrackerApp:
    def __init__(self, root, service_manager):
        self.root = root
        self.root.title("Hour Tracker")
        self.service_manager = service_manager

        self.style = Style(theme="darkly")  # Escolha o tema desejado

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
        service_combobox = ttk.Combobox(log_hours_frame, values=self.service_manager.services)
        service_combobox.grid(row=1, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Horas Trabalhadas:").grid(row=2, column=0, pady=5)
        hours_entry = ttk.Entry(log_hours_frame)
        hours_entry.grid(row=2, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Custo por Hora:").grid(row=3, column=0, pady=5)
        rate_entry = ttk.Entry(log_hours_frame)
        rate_entry.grid(row=3, column=1, pady=5)

        ttk.Button(log_hours_frame, text="Registrar Horas", command=lambda: self.log_hours(service_combobox.get(), hours_entry.get(), rate_entry.get())).grid(row=4, column=0, columnspan=2, pady=10)

        # Frame para mostrar o resultado final
        result_frame = ttk.Frame(self.root, padding="10")
        result_frame.grid(row=2, column=0, padx=10, pady=10)

        ttk.Label(result_frame, text="Resultado Final:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(result_frame, text="Serviço:").grid(row=1, column=0, pady=5)
        result_service_combobox = ttk.Combobox(result_frame, values=self.service_manager.services)
        result_service_combobox.grid(row=1, column=1, pady=5)

        ttk.Label(result_frame, text="Total de Horas:").grid(row=2, column=0, pady=5)
        total_hours_label = ttk.Label(result_frame, text="")
        total_hours_label.grid(row=2, column=1, pady=5)

        ttk.Label(result_frame, text="Custo Total:").grid(row=3, column=0, pady=5)
        total_cost_label = ttk.Label(result_frame, text="")
        total_cost_label.grid(row=3, column=1, pady=5)

        ttk.Button(result_frame, text="Atualizar Resultado", command=lambda: self.update_result(result_service_combobox.get(), total_hours_label, total_cost_label)).grid(row=4, column=0, columnspan=2, pady=10)

    def create_service(self, service_name):
        # Chamar o método atualizado com a taxa (rate)
        rate = 0  # Defina um valor padrão para a taxa; você pode modificá-lo conforme necessário
        self.service_manager.create_service(service_name, rate)

    def log_hours(self, service_name, hours, rate):
        self.service_manager.log_hours(service_name, hours, rate)

    def update_result(self, service_name, total_hours_label, total_cost_label):
        total_hours, total_cost = self.service_manager.get_service_info(service_name)
        total_hours_label.config(text=f"{total_hours} horas")
        total_cost_label.config(text=f"R${total_cost}")

# Inicializa o serviço manager e o aplicativo
service_manager = ServiceManager()
root = tk.Tk()
app = HourTrackerApp(root, service_manager)
root.mainloop()
