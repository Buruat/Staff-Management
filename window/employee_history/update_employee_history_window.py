import tkinter as tk
from tkinter import messagebox, ttk

class UpdateEmploymentHistoryWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Обновить историю сотрудника")

        tk.Label(self, text="Имя сотрудника:").grid(row=0, column=0, sticky='e')

        self.employee_name_combobox = ttk.Combobox(self, state="readonly")
        self.employee_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        tk.Label(self, text="Дата начала (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Дата конца (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="ЗП:").grid(row=3, column=0, sticky='e')
        self.salary_entry = tk.Entry(self)
        self.salary_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Обновить историю сотрудника", command=self.update_employment_history).grid(row=4, column=1, pady=5)

    def fill_employee_names(self):
        try:
            self.request.cursor.execute("SELECT full_name FROM employees")
            employee_names = [row[0] for row in self.request.cursor.fetchall()]
            self.employee_name_combobox["values"] = employee_names
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_employment_history(self):
        employee_name = self.employee_name_combobox.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        salary = self.salary_entry.get().strip()

        update_values = []

        update_query_parts = []

        if start_date:
            update_values.append(start_date)
            update_query_parts.append("start_date = %s")
        if end_date:
            update_values.append(end_date)
            update_query_parts.append("end_date = %s")
        if salary:
            update_values.append(salary)
            update_query_parts.append("salary = %s")

        if update_values:
            try:
                self.request.cursor.execute("SELECT id FROM employees WHERE full_name = %s", (employee_name,))
                employee_id = self.request.cursor.fetchone()
                if employee_id:
                    employee_id = employee_id[0]

                    update_query = "UPDATE employment_history SET " + ", ".join(
                        update_query_parts) + " WHERE employee_id = %s"

                    update_values.append(employee_id)

                    self.request.cursor.execute(update_query, tuple(update_values))
                    self.request.connection.commit()
                    messagebox.showinfo("Успех", "История сотрудника успешно обновлена")
                else:
                    messagebox.showerror("Ошибка", "Сотрудник не найден")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        else:
            messagebox.showerror("Ошибка", "Поля не заполнены")