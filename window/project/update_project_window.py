import tkinter as tk
from tkinter import messagebox, ttk

class UpdateProjectWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Обновить проект")

        tk.Label(self, text="Имя сотрудника:").grid(row=0, column=0, sticky='e')
        self.employee_name_combobox = ttk.Combobox(self, state="readonly")
        self.employee_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        tk.Label(self, text="Имя задачи:").grid(row=1, column=0, sticky='e')
        self.task_name_combobox = ttk.Combobox(self, state="readonly")
        self.task_name_combobox.grid(row=1, column=1, pady=5, padx=5)
        self.fill_task_names()

        tk.Label(self, text="Дата начала (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="Дата конца (YYYY-MM-DD):").grid(row=3, column=0, sticky='e')
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Обновить проект", command=self.update_project).grid(row=4, column=1, pady=5)

    def fill_employee_names(self):
        try:
            self.request.cursor.execute("SELECT full_name FROM employees")
            employee_names = [row[0] for row in self.request.cursor.fetchall()]
            self.employee_name_combobox["values"] = employee_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def fill_task_names(self):
        try:
            self.request.cursor.execute("SELECT name FROM tasks")
            task_names = [row[0] for row in self.request.cursor.fetchall()]
            self.task_name_combobox["values"] = task_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_project(self):
        employee_name = self.employee_name_combobox.get()
        task_name = self.task_name_combobox.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        update_values = []
        update_query_parts = []

        if start_date:
            update_values.append(start_date)
            update_query_parts.append("start_date = %s")
        if end_date:
            update_values.append(end_date)
            update_query_parts.append("end_date = %s")

        if update_values:
            try:
                self.request.cursor.execute("SELECT id FROM tasks WHERE name = %s", (task_name,))
                task_id = self.request.cursor.fetchone()

                self.request.cursor.execute("SELECT id FROM employees WHERE full_name = %s", (employee_name,))
                employee_id = self.request.cursor.fetchone()

                if task_id and employee_id:
                    task_id = task_id[0]
                    employee_id = employee_id[0]

                    update_query = "UPDATE projects SET " + ", ".join(update_query_parts) + " WHERE task_id = %s AND employee_id = %s"

                    update_values.extend([task_id, employee_id])

                    self.request.cursor.execute(update_query, tuple(update_values))
                    self.request.connection.commit()
                    messagebox.showinfo("Успех", "Проект успешно обновлен")
                else:
                    messagebox.showerror("Ошибка", "Не найдены задача и соответствующий сотрудник")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        else:
            messagebox.showerror("Ошибка", "Поля пусты")