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
                    minutes REAL NOT NULL,
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
                    hours = float(hours)
                    minutes = float(minutes)
                    rate = float(rate)
                    total_hours = hours + minutes / 60
                    total_cost = total_hours * rate
                    cursor.execute("INSERT INTO logs (service_id, date, hours, minutes, rate, total_cost) VALUES (?, ?, ?, ?, ?, ?)",
                                   (service_id, datetime.now(), hours, minutes, rate, total_cost))
                    print(f"Horas registradas para o serviço {service_name}: {total_hours:.2f}h, Custo total: R${total_cost:.2f}")
                except ValueError:
                    print("Por favor, insira valores válidos para horas, minutos e custo por hora.")
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
                cursor.execute("SELECT SUM(hours) + SUM(minutes / 60), SUM(total_cost) FROM logs WHERE service_id=?", (service_id,))
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

        self.style = Style(theme="yeti")  # Escolha o tema desejado

        # Inicializa o atributo logs_listbox como None
        self.logs_listbox = None

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, rowspan=6, columnspan=2, padx=10, pady=5, sticky='nsew')

        # Frame para adicionar um novo serviço
        add_service_frame = ttk.Frame(main_frame, padding="5")
        add_service_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        ttk.Label(add_service_frame, text="Novo Serviço:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(add_service_frame, text="Nome do Serviço:").grid(row=1, column=0, pady=5)
        service_name_entry = ttk.Entry(add_service_frame)
        service_name_entry.grid(row=1, column=1, pady=5)

        ttk.Button(add_service_frame, text="Criar Serviço", command=lambda: self.create_service(service_name_entry.get())).grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para lançar horas
        log_hours_frame = ttk.Frame(main_frame, padding="5")
        log_hours_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

        ttk.Label(log_hours_frame, text="Lançar Horas:").grid(row=0, column=0, columnspan=4, pady=5)

        ttk.Label(log_hours_frame, text="Serviço:").grid(row=1, column=0, pady=5)
        service_combobox = ttk.Combobox(log_hours_frame, values=self.service_manager.services)
        service_combobox.grid(row=1, column=1, pady=5, padx=(0, 5))

        ttk.Label(log_hours_frame, text="Horas Trabalhadas:").grid(row=2, column=0, pady=5, sticky='e')
        hours_entry = ttk.Entry(log_hours_frame)
        hours_entry.grid(row=2, column=1, pady=5, padx=(0, 5))

        ttk.Label(log_hours_frame, text="Minutos Trabalhados:").grid(row=3, column=0, pady=5, sticky='e')
        minutes_entry = ttk.Entry(log_hours_frame)
        minutes_entry.grid(row=3, column=1, pady=5, padx=(0, 5))

        ttk.Label(log_hours_frame, text="Custo por Hora:").grid(row=4, column=0, pady=5, sticky='e')
        rate_entry = ttk.Entry(log_hours_frame)
        rate_entry.grid(row=4, column=1, pady=5, padx=(0, 5))

        ttk.Button(log_hours_frame, text="Registrar Horas", command=lambda: self.log_hours(
            service_combobox.get(), hours_entry.get(), minutes_entry.get(), rate_entry.get())
        ).grid(row=5, column=0, columnspan=4, pady=5)
        # Frame para excluir um lançamento
        delete_log_frame = ttk.Frame(main_frame, padding="5")
        delete_log_frame.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

        ttk.Label(delete_log_frame, text="Excluir Lançamento:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(delete_log_frame, text="ID do Lançamento:").grid(row=1, column=0, pady=5)
        log_id_entry = ttk.Entry(delete_log_frame)
        log_id_entry.grid(row=1, column=1, pady=5)

        ttk.Button(delete_log_frame, text="Excluir Lançamento", command=lambda: self.delete_log(log_id_entry.get())).grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para mostrar o resultado final
        result_frame = ttk.Frame(main_frame, padding="5")
        result_frame.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')

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

        ttk.Button(result_frame, text="Atualizar Resultado", command=lambda: self.update_result(result_service_combobox.get(), total_hours_label, total_cost_label)).grid(row=4, column=0, columnspan=2, pady=5)

        # Frame para visualizar todos os lançamentos
        view_logs_frame = ttk.Frame(main_frame, padding="5")
        view_logs_frame.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')

        ttk.Label(view_logs_frame, text="Visualizar Lançamentos:").grid(row=0, column=0, columnspan=2, pady=5)

        # Aqui definimos logs_listbox como um atributo da classe
        self.logs_listbox = tk.Listbox(view_logs_frame, selectmode=tk.SINGLE, width=50)
        self.logs_listbox.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(view_logs_frame, text="Atualizar Lançamentos", command=lambda: self.update_logs_list(self.logs_listbox)).grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para pesquisar lançamentos por serviço
        search_logs_frame = ttk.Frame(main_frame, padding="5")
        search_logs_frame.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')

        ttk.Label(search_logs_frame, text="Pesquisar Lançamentos por Serviço:").grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Label(search_logs_frame, text="Serviço:").grid(row=1, column=0, pady=5)
        search_service_combobox = ttk.Combobox(search_logs_frame, values=self.service_manager.services)
        search_service_combobox.grid(row=1, column=1, pady=5)

        ttk.Button(search_logs_frame, text="Pesquisar", command=lambda: self.search_logs(search_service_combobox.get(), self.logs_listbox)).grid(row=2, column=0, columnspan=2, pady=5)

        # Configurar o grid para expandir as células
        for i in range(6):
            main_frame.rowconfigure(i, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def search_logs(self, service_name):
        logs = self.service_manager.get_all_logs()
        filtered_logs = [log for log in logs if log[1] == service_name]
        self.search_logs_listbox.delete(0, tk.END)
        for log in filtered_logs:
            log_entry = f"ID: {log[0]}, Serviço: {log[1]}, Custo: R${log[2]:.2f}, Data: {log[3]}"
            self.search_logs_listbox.insert(tk.END, log_entry)

    def create_service(self, service_name):
        rate = 0
        self.service_manager.create_service(service_name.upper().strip(), rate)

    def log_hours(self, service_name, hours, minutes, rate):
        self.service_manager.log_hours(service_name, hours, minutes, rate)
        # Atualiza a lista de lançamentos usando o atributo da classe
        self.update_logs_list(self.logs_listbox)

    def delete_log(self, log_id):
        self.service_manager.delete_log(log_id)
        # Atualiza a lista de lançamentos usando o atributo da classe
        self.update_logs_list(self.logs_listbox)

    def update_result(self, service_name, total_hours_label, total_cost_label):
        total_hours, total_cost = self.service_manager.get_service_info(service_name)
        formatted_hours = int(total_hours)
        formatted_minutes = (total_hours - formatted_hours) * 60
        total_hours_label.config(text=f"{formatted_hours:02d}:{int(formatted_minutes):02d}h")
        total_cost_label.config(text=f"R${total_cost:.2f}")

    def update_logs_list(self, logs_listbox):
        logs = self.service_manager.get_all_logs()
        logs_listbox.delete(0, tk.END)
        for log in logs:
            log_entry = f"ID: {log[0]}, Serviço: {log[1]}, Custo: R${log[2]:.2f}, Data: {log[3]}"
            logs_listbox.insert(tk.END, log_entry)


if __name__ == "__main__":
    root = tk.Tk()
    service_manager = ServiceManager()
    app = HourTrackerApp(root, service_manager)
    root.mainloop()