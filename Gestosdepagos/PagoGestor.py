import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta

class SubscriptionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Suscripciones - COP")
        self.root.geometry("1000x700")
        

        self.current_account = None
        self.accounts = {}
        self.subscriptions = []
        self.filtered_subs = []
        
  
        self.setup_styles()
        

        self.load_data()
        

        self.create_widgets()
        

        self.update_subscriptions_list()
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure('TButton', padding=5, font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Total.TLabel', font=('Arial', 12, 'bold'), foreground='#2E86C1')
    
    def create_widgets(self):

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        

        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_panel, text="Cuentas", style='Header.TLabel').pack(pady=(0, 10))
        
        self.accounts_listbox = tk.Listbox(left_panel, font=('Arial', 10), selectbackground='#3498DB')
        self.accounts_listbox.pack(fill=tk.BOTH, expand=True)
        self.accounts_listbox.bind('<<ListboxSelect>>', self.select_account)
        
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Nueva Cuenta", command=self.create_account).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="Eliminar Cuenta", command=self.delete_account).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(left_panel, text="Filtros", style='Header.TLabel').pack(pady=(20, 10))
        
        ttk.Label(left_panel, text="Mes:").pack(anchor=tk.W)
        self.month_filter = ttk.Combobox(left_panel, values=["Todos"] + [f"{i:02d}" for i in range(1, 13)])
        self.month_filter.pack(fill=tk.X)
        self.month_filter.set("Todos")
        self.month_filter.bind("<<ComboboxSelected>>", self.update_subscriptions_list)
        
        ttk.Label(left_panel, text="Año:").pack(anchor=tk.W, pady=(5, 0))
        current_year = datetime.now().year
        self.year_filter = ttk.Combobox(left_panel, values=["Todos"] + [str(year) for year in range(current_year-2, current_year+3)])
        self.year_filter.pack(fill=tk.X)
        self.year_filter.set("Todos")
        self.year_filter.bind("<<ComboboxSelected>>", self.update_subscriptions_list)
        
        top_frame = ttk.Frame(right_panel)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top_frame, text="Suscripciones", style='Header.TLabel').pack(side=tk.LEFT)
        
        btn_frame_right = ttk.Frame(top_frame)
        btn_frame_right.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame_right, text="Agregar", command=self.add_subscription).pack(side=tk.LEFT)
        ttk.Button(btn_frame_right, text="Editar", command=self.edit_subscription).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame_right, text="Eliminar", command=self.delete_subscription).pack(side=tk.LEFT)
        
        self.tree = ttk.Treeview(right_panel, columns=('Nombre', 'Monto', 'Fecha Pago', 'Próximo Pago', 'Categoría'), show='headings')
        
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Monto', text='Monto (COP)')
        self.tree.heading('Fecha Pago', text='Fecha Pago')
        self.tree.heading('Próximo Pago', text='Próximo Pago')
        self.tree.heading('Categoría', text='Categoría')
        
        self.tree.column('Nombre', width=150)
        self.tree.column('Monto', width=100, anchor=tk.E)
        self.tree.column('Fecha Pago', width=100, anchor=tk.CENTER)
        self.tree.column('Próximo Pago', width=100, anchor=tk.CENTER)
        self.tree.column('Categoría', width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.total_frame = ttk.Frame(right_panel)
        self.total_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.total_label = ttk.Label(self.total_frame, text="Total este mes: $0 COP", style='Total.TLabel')
        self.total_label.pack(side=tk.RIGHT)
        
        self.update_accounts_list()
    
    def format_currency(self, amount):
        """Formatea el monto como moneda colombiana"""
        return "${:,.0f} COP".format(amount).replace(",", ".")
    
    def load_data(self):
        """Carga los datos guardados desde el archivo JSON"""
        if os.path.exists('subscriptions.json'):
            with open('subscriptions.json', 'r') as f:
                data = json.load(f)
                self.accounts = data.get('accounts', {})
                
                for account, subs in self.accounts.items():
                    for sub in subs:
                        sub['payment_date'] = datetime.strptime(sub['payment_date'], '%Y-%m-%d').date()
                        if sub.get('next_payment'):
                            sub['next_payment'] = datetime.strptime(sub['next_payment'], '%Y-%m-%d').date()
    
    def save_data(self):
        """Guarda los datos en un archivo JSON"""
        data_to_save = {'accounts': {}}
        for account, subs in self.accounts.items():
            data_to_save['accounts'][account] = []
            for sub in subs:
                sub_copy = sub.copy()
                sub_copy['payment_date'] = sub['payment_date'].strftime('%Y-%m-%d')
                if sub.get('next_payment'):
                    sub_copy['next_payment'] = sub['next_payment'].strftime('%Y-%m-%d')
                data_to_save['accounts'][account].append(sub_copy)
        
        with open('subscriptions.json', 'w') as f:
            json.dump(data_to_save, f, indent=2)
    
    def update_accounts_list(self):
        """Actualiza la lista de cuentas en el Listbox"""
        self.accounts_listbox.delete(0, tk.END)
        for account in sorted(self.accounts.keys()):
            self.accounts_listbox.insert(tk.END, account)
        
        if self.accounts and not self.current_account:
            self.accounts_listbox.selection_set(0)
            self.select_account(None)
    
    def select_account(self, event):
        """Selecciona una cuenta y carga sus suscripciones"""
        selection = self.accounts_listbox.curselection()
        if selection:
            self.current_account = self.accounts_listbox.get(selection[0])
            self.subscriptions = self.accounts.get(self.current_account, [])
            self.update_subscriptions_list()
    
    def create_account(self):
        """Crea una nueva cuenta"""
        account_name = simpledialog.askstring("Nueva Cuenta", "Nombre de la cuenta:")
        if account_name and account_name not in self.accounts:
            self.accounts[account_name] = []
            self.update_accounts_list()
            self.save_data()
        elif account_name in self.accounts:
            messagebox.showerror("Error", "Ya existe una cuenta con ese nombre")
    
    def delete_account(self):
        """Elimina la cuenta seleccionada"""
        if not self.current_account:
            return
            
        if messagebox.askyesno("Confirmar", f"¿Eliminar la cuenta '{self.current_account}' y todas sus suscripciones?"):
            del self.accounts[self.current_account]
            self.current_account = None
            self.subscriptions = []
            self.update_accounts_list()
            self.update_subscriptions_list()
            self.save_data()
    
    def update_subscriptions_list(self, event=None):
        """Actualiza la lista de suscripciones según los filtros"""
        self.filtered_subs = []
        
        if not self.current_account:
            self.tree.delete(*self.tree.get_children())
            self.total_label.config(text="Total este mes: $0 COP")
            return
            
        month_filter = self.month_filter.get()
        year_filter = self.year_filter.get()
        
        current_month = datetime.now().strftime('%m')
        current_year = datetime.now().strftime('%Y')
        
        total = 0
        
        for sub in self.subscriptions:
            payment_date = sub['payment_date']
            sub_month = payment_date.strftime('%m')
            sub_year = payment_date.strftime('%Y')
            
            if (month_filter == "Todos" or sub_month == month_filter) and \
               (year_filter == "Todos" or sub_year == year_filter):
                self.filtered_subs.append(sub)
                
                if sub_month == current_month and sub_year == current_year:
                    total += sub['amount']
        
        self.tree.delete(*self.tree.get_children())
        
        for sub in sorted(self.filtered_subs, key=lambda x: x['payment_date']):
            next_payment = sub.get('next_payment', '')
            next_payment_str = next_payment.strftime('%d/%m/%Y') if next_payment else ''
            
            self.tree.insert('', tk.END, values=(
                sub['name'],
                self.format_currency(sub['amount']),
                sub['payment_date'].strftime('%d/%m/%Y'),
                next_payment_str,
                sub.get('category', '')
            ))
        
        self.total_label.config(text=f"Total este mes: {self.format_currency(total)}")
    
    def add_subscription(self):
        """Agrega una nueva suscripción"""
        if not self.current_account:
            messagebox.showerror("Error", "Selecciona una cuenta primero")
            return
            
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Suscripción")
        add_window.geometry("400x400")
        
        name_var = tk.StringVar()
        amount_var = tk.DoubleVar()
        day_var = tk.IntVar(value=datetime.now().day)
        month_var = tk.IntVar(value=datetime.now().month)
        year_var = tk.IntVar(value=datetime.now().year)
        category_var = tk.StringVar()
        frequency_var = tk.StringVar(value="Mensual")
        
        ttk.Label(add_window, text="Nombre:").pack(pady=(10, 0))
        ttk.Entry(add_window, textvariable=name_var).pack(fill=tk.X, padx=10)
        
        ttk.Label(add_window, text="Monto (COP):").pack(pady=(10, 0))
        ttk.Entry(add_window, textvariable=amount_var).pack(fill=tk.X, padx=10)
        
        ttk.Label(add_window, text="Fecha de Pago:").pack(pady=(10, 0))
        date_frame = ttk.Frame(add_window)
        date_frame.pack(fill=tk.X, padx=10)
        
        ttk.Entry(date_frame, textvariable=day_var, width=3).pack(side=tk.LEFT)
        ttk.Label(date_frame, text="/").pack(side=tk.LEFT)
        ttk.Entry(date_frame, textvariable=month_var, width=3).pack(side=tk.LEFT)
        ttk.Label(date_frame, text="/").pack(side=tk.LEFT)
        ttk.Entry(date_frame, textvariable=year_var, width=5).pack(side=tk.LEFT)
        
        ttk.Label(add_window, text="Frecuencia:").pack(pady=(10, 0))
        ttk.Combobox(add_window, textvariable=frequency_var, 
                     values=["Mensual", "Anual", "Trimestral", "Semestral"]).pack(fill=tk.X, padx=10)
        
        ttk.Label(add_window, text="Categoría:").pack(pady=(10, 0))
        ttk.Combobox(add_window, textvariable=category_var, 
                     values=["Entretenimiento", "Software", "Educación", "Servicios", "Otros"]).pack(fill=tk.X, padx=10)
        
        def save_subscription():
            try:
                payment_date = datetime(
                    year=year_var.get(),
                    month=month_var.get(),
                    day=day_var.get()
                ).date()
                
                next_payment = self.calculate_next_payment(payment_date, frequency_var.get())
                
                new_sub = {
                    'name': name_var.get(),
                    'amount': amount_var.get(),
                    'payment_date': payment_date,
                    'next_payment': next_payment,
                    'frequency': frequency_var.get(),
                    'category': category_var.get()
                }
                
                self.subscriptions.append(new_sub)
                self.accounts[self.current_account] = self.subscriptions
                self.update_subscriptions_list()
                self.save_data()
                add_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Fecha inválida: {e}")
        
        ttk.Button(add_window, text="Guardar", command=save_subscription).pack(pady=20)
    
    def calculate_next_payment(self, payment_date, frequency):
        """Calcula la próxima fecha de pago según la frecuencia"""
        if frequency == "Mensual":
            months = 1
        elif frequency == "Trimestral":
            months = 3
        elif frequency == "Semestral":
            months = 6
        elif frequency == "Anual":
            months = 12
        else:
            return None
        
        year = payment_date.year
        month = payment_date.month + months
        
        if month > 12:
            year += month // 12
            month = month % 12
            if month == 0:
                month = 12
        
        day = payment_date.day
        last_day_of_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day
        day = min(day, last_day_of_month)
        
        return datetime(year, month, day).date()
    
    def edit_subscription(self):
        """Edita la suscripción seleccionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una suscripción para editar")
            return
            
        index = self.tree.index(selected[0])
        sub = self.filtered_subs[index]
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Suscripción")
        edit_window.geometry("400x400")
        
        name_var = tk.StringVar(value=sub['name'])
        amount_var = tk.DoubleVar(value=sub['amount'])
        day_var = tk.IntVar(value=sub['payment_date'].day)
        month_var = tk.IntVar(value=sub['payment_date'].month)
        year_var = tk.IntVar(value=sub['payment_date'].year)
        category_var = tk.StringVar(value=sub.get('category', ''))
        frequency_var = tk.StringVar(value=sub.get('frequency', 'Mensual'))
        
        ttk.Label(edit_window, text="Nombre:").pack(pady=(10, 0))
        ttk.Entry(edit_window, textvariable=name_var).pack(fill=tk.X, padx=10)
        
        ttk.Label(edit_window, text="Monto (COP):").pack(pady=(10, 0))
        ttk.Entry(edit_window, textvariable=amount_var).pack(fill=tk.X, padx=10)
        
        ttk.Label(edit_window, text="Fecha de Pago:").pack(pady=(10, 0))
        date_frame = ttk.Frame(edit_window)
        date_frame.pack(fill=tk.X, padx=10)
        
        ttk.Entry(date_frame, textvariable=day_var, width=3).pack(side=tk.LEFT)
        ttk.Label(date_frame, text="/").pack(side=tk.LEFT)
        ttk.Entry(date_frame, textvariable=month_var, width=3).pack(side=tk.LEFT)
        ttk.Label(date_frame, text="/").pack(side=tk.LEFT)
        ttk.Entry(date_frame, textvariable=year_var, width=5).pack(side=tk.LEFT)
        
        ttk.Label(edit_window, text="Frecuencia:").pack(pady=(10, 0))
        ttk.Combobox(edit_window, textvariable=frequency_var, 
                     values=["Mensual", "Anual", "Trimestral", "Semestral"]).pack(fill=tk.X, padx=10)
        
        ttk.Label(edit_window, text="Categoría:").pack(pady=(10, 0))
        ttk.Combobox(edit_window, textvariable=category_var, 
                     values=["Entretenimiento", "Software", "Educación", "Servicios", "Otros"]).pack(fill=tk.X, padx=10)
        
        def save_changes():
            try:
                payment_date = datetime(
                    year=year_var.get(),
                    month=month_var.get(),
                    day=day_var.get()
                ).date()
                
                next_payment = self.calculate_next_payment(payment_date, frequency_var.get())
                
                original_index = self.subscriptions.index(sub)
                
                self.subscriptions[original_index] = {
                    'name': name_var.get(),
                    'amount': amount_var.get(),
                    'payment_date': payment_date,
                    'next_payment': next_payment,
                    'frequency': frequency_var.get(),
                    'category': category_var.get()
                }
                
                self.accounts[self.current_account] = self.subscriptions
                self.update_subscriptions_list()
                self.save_data()
                edit_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Fecha inválida: {e}")
        
        ttk.Button(edit_window, text="Guardar Cambios", command=save_changes).pack(pady=20)
    
    def delete_subscription(self):
        """Elimina la suscripción seleccionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una suscripción para eliminar")
            return
            
        index = self.tree.index(selected[0])
        sub = self.filtered_subs[index]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar la suscripción '{sub['name']}'?"):
            self.subscriptions.remove(sub)
            self.accounts[self.current_account] = self.subscriptions
            self.update_subscriptions_list()
            self.save_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = SubscriptionManager(root)
    root.mainloop()