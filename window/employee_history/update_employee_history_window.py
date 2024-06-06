import tkinter as tk
from tkinter import messagebox, ttk

class UpdateEmploymentHistoryWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Update Employment History")

        tk.Label(self, text="Employee Name:").grid(row=0, column=0, sticky='e')

        # Создание выпадающего списка с именами сотрудников
        self.employee_name_combobox = ttk.Combobox(self, state="readonly")
        self.employee_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        tk.Label(self, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="Salary:").grid(row=3, column=0, sticky='e')
        self.salary_entry = tk.Entry(self)
        self.salary_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Update Employment History", command=self.update_employment_history).grid(row=4, column=1, pady=5)

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

        # Создаем список для хранения значений, которые будут использованы в запросе
        update_values = []

        # Создаем список для хранения частей SQL-запроса
        update_query_parts = []

        # Проверяем, какие поля заполнены, и добавляем их в список update_values
        if start_date:
            update_values.append(start_date)
            update_query_parts.append("start_date = %s")
        if end_date:
            update_values.append(end_date)
            update_query_parts.append("end_date = %s")
        if salary:
            update_values.append(salary)
            update_query_parts.append("salary = %s")

        # Проверяем, было ли хотя бы одно поле заполнено
        if update_values:
            try:
                # Получаем ID сотрудника по его имени
                self.request.cursor.execute("SELECT id FROM employees WHERE full_name = %s", (employee_name,))
                employee_id = self.request.cursor.fetchone()
                if employee_id:
                    employee_id = employee_id[0]

                    # Формируем SQL-запрос с использованием динамических частей
                    update_query = "UPDATE employment_history SET " + ", ".join(
                        update_query_parts) + " WHERE employee_id = %s"

                    # Добавляем employee_id в список update_values
                    update_values.append(employee_id)

                    # Выполняем SQL-запрос с динамическими значениями
                    self.request.cursor.execute(update_query, tuple(update_values))
                    self.request.connection.commit()
                    messagebox.showinfo("Success", "Employment history updated successfully")
                else:
                    messagebox.showerror("Error", "Employee not found")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "No fields were provided for update")