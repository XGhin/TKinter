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
                    name TEXT NOT NULL UNIQUE,
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
        service_name = service_name.upper().strip()
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO services (name, rate) VALUES (?, ?)", (service_name, rate))
            print(f"Serviço criado: {service_name}")
        except sqlite3.IntegrityError:
            print(f"Este serviço já existe: {service_name}")

    def log_hours(self, service_name, hours, minutes, rate):
        # Registra as horas trabalhadas para um serviço e insere no banco de dados
        service_name = service_name.upper().strip()
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, rate FROM services WHERE name=?", (service_name,))
            result = cursor.fetchone()
            if result:
                service_id, service_rate = result
                try:
                    hours = float(hours) + float(minutes) / 60
                    rate = float(rate)
                    total_cost = hours * rate
                    cursor.execute("INSERT INTO logs (service_id, date, hours, rate, total_cost) VALUES (?, ?, ?, ?, ?)",
                                   (service_id, datetime.now(), hours, rate, total_cost))
                    print(f"Horas registradas para o serviço {service_name}: {hours:.2f}h, Custo total: R${total_cost:.2f}")
                except ValueError:
                    print("Por favor, insira valores válidos para horas e custo por hora.")
            else:
                print("Este serviço não existe.")

    def get_service_info(self, service_name):
        # Obtém informações sobre um serviço, incluindo horas e custos totais
        service_name = service_name.upper().strip()
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
                return None  # Retorna None se o serviço não existe

    def delete_log(self, log_id):
        # Exclui um lançamento específico do banco de dados
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM logs WHERE id=?", (log_id,))

    def get_all_logs(self):
        # Obtém todas as informações sobre os lançamentos (ordenados por ordem decrescente)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT logs.id, services.name, logs.total_cost, logs.date FROM logs JOIN services ON logs.service_id = services.id ORDER BY logs.date DESC")
            return cursor.fetchall()

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
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, rowspan=6, columnspan=2, padx=10, pady=10)

        # Frame para adicionar um novo serviço
        add_service_frame = ttk.Frame(main_frame, padding="10")
        add_service_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(add_service_frame, text="Novo Serviço:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(add_service_frame, text="Nome do Serviço:").grid(row=1, column=0, pady=5)
        service_name_entry = ttk.Entry(add_service_frame)
        service_name_entry.grid(row=1, column=1, pady=5)

        ttk.Button(add_service_frame, text="Criar Serviço", command=lambda: self.create_service(service_name_entry.get())).grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para lançar horas
        log_hours_frame = ttk.Frame(main_frame, padding="10")
        log_hours_frame.grid(row=1, column=0, padx=10, pady=10)

        ttk.Label(log_hours_frame, text="Lançar Horas:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(log_hours_frame, text="Serviço:").grid(row=1, column=0, pady=5)
        service_combobox = ttk.Combobox(log_hours_frame, values=self.service_manager.services)
        service_combobox.grid(row=1, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Horas Trabalhadas:").grid(row=2, column=0, pady=5)
        hours_entry = ttk.Entry(log_hours_frame)
        hours_entry.grid(row=2, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Minutos Trabalhados:").grid(row=3, column=0, pady=5)
        minutes_entry = ttk.Entry(log_hours_frame)
        minutes_entry.grid(row=3, column=1, pady=5)

        ttk.Label(log_hours_frame, text="Custo por Hora:").grid(row=4, column=0, pady=5)
        rate_entry = ttk.Entry(log_hours_frame)
        rate_entry.grid(row=4, column=1, pady=5)

        ttk.Button(log_hours_frame, text="Registrar Horas", command=lambda: self.log_hours(service_combobox.get(), hours_entry.get(), minutes_entry.get(), rate_entry.get())).grid(row=5, column=0, columnspan=2, pady=5)

        # Frame para excluir um lançamento
        delete_log_frame = ttk.Frame(main_frame, padding="10")
        delete_log_frame.grid(row=2, column=0, padx=10, pady=10)

        ttk.Label(delete_log_frame, text="Excluir Lançamento:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(delete_log_frame, text="ID do Lançamento:").grid(row=1, column=0, pady=5)
        log_id_entry = ttk.Entry(delete_log_frame)
        log_id_entry.grid(row=1, column=1, pady=5)

        ttk.Button(delete_log_frame, text="Excluir Lançamento", command=lambda: self.delete_log(log_id_entry.get())).grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para mostrar o resultado final
        result_frame = ttk.Frame(main_frame, padding="10")
        result_frame.grid(row=4, column=0, padx=10, pady=10)

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

        # Frame para visualizar todos os lançamentos
        view_logs_frame = ttk.Frame(main_frame, padding="10")
        view_logs_frame.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(view_logs_frame, text="Visualizar Lançamentos:").grid(row=0, column=0, columnspan=2, pady=5)

        logs_listbox = tk.Listbox(view_logs_frame, selectmode=tk.SINGLE, width=50)
        logs_listbox.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(view_logs_frame, text="Atualizar Lançamentos", command=lambda: self.update_logs_list(logs_listbox)).grid(row=2, column=0, columnspan=2, pady=10)

    def create_service(self, service_name):
        rate = 0
        self.service_manager.create_service(service_name.upper().strip(), rate)

    def log_hours(self, service_name, hours, minutes, rate):
        self.service_manager.log_hours(service_name.upper().strip(), hours.strip(), minutes.strip(), rate.strip())
        # Adiciona esta linha para atualizar a lista de lançamentos imediatamente após o registro
        self.update_logs_list(logs_listbox)

    def delete_log(self, log_id):
        try:
            log_id = int(log_id)
            self.service_manager.delete_log(log_id)
            print(f"Lançamento excluído com sucesso: ID {log_id}")
            # Adiciona esta linha para atualizar a lista de lançamentos imediatamente após a exclusão
            self.update_logs_list(logs_listbox)
        except ValueError:
            print("Por favor, insira um ID de lançamento válido.")

    def update_logs_list(self, logs_listbox):
        logs_listbox.delete(0, tk.END)
        logs = self.service_manager.get_all_logs()
        for log in logs:
            log_id, log_service, log_cost, log_date = log
            logs_listbox.insert(tk.END, f"ID: {log_id}, Serviço: {log_service}, Custo: R${log_cost:.2f}, Data e Hora: {log_date}")

    def update_result(self, service_name, total_hours_label, total_cost_label):
        result = self.service_manager.get_service_info(service_name.upper().strip())
        if result is not None:
            total_hours, total_cost = result
            # Formata as horas e minutos separadamente
            formatted_hours = int(total_hours)
            formatted_minutes = int((total_hours - formatted_hours) * 60)
            total_hours_label.config(text=f"{formatted_hours:02d}:{formatted_minutes:02d}")
            total_cost_label.config(text=f"R${total_cost:.2f}")
        else:
            total_hours_label.config(text="Este serviço não existe.")
            total_cost_label.config(text="")

    def update_last_service_result(self, total_hours_label, total_cost_label):
        # Obtém o último serviço registrado automaticamente
        last_service = self.service_manager.services[-1]
        self.update_result(last_service, total_hours_label, total_cost_label)

# Inicializa o serviço manager e o aplicativo
service_manager = ServiceManager()
root = tk.Tk()
app = HourTrackerApp(root, service_manager)
root.mainloop()