import tkinter as tk
from tkinter import messagebox, ttk

class AddEmploymentHistoryWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Добавить историю сотрудника")

        tk.Label(self, text="Имя сотрудника:").grid(row=0, column=0, sticky='e')
        self.employee_name_entry = tk.Entry(self)
        self.employee_name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self, text="Дата начала (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Дата конца (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="ЗП:").grid(row=3, column=0, sticky='e')
        self.salary_entry = tk.Entry(self)
        self.salary_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Добавить историю сотрудника", command=self.add_employment_history).grid(row=4, column=1, pady=5)

    def add_employment_history(self):
        employee_name = self.employee_name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        salary = self.salary_entry.get()

        try:
            self.request.cursor.execute("SELECT id FROM employees WHERE full_name = %s", (employee_name,))
            employee_id = self.request.cursor.fetchone()
            if employee_id:
                employee_id = employee_id[0]
                self.request.cursor.execute(
                    "CALL add_employment_history(%s, %s, %s, %s)",
                    (employee_id, start_date, end_date, salary)
                )
                self.request.connection.commit()
                messagebox.showinfo("Успех", "История сотрудника успешно добавлена")
            else:
                messagebox.showerror("Ошибка", "Сотрудник не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))