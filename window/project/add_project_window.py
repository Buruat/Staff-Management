import tkinter as tk
from tkinter import messagebox, ttk

class AddProjectWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Добавить проект")

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

        tk.Label(self, text="дата конца (YYYY-MM-DD):").grid(row=3, column=0, sticky='e')
        self.end_date_entry = tk.Entry(self)
        self.end_date_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Добавить проект", command=self.add_project).grid(row=4, column=1, pady=5)

    def fill_employee_names(self):
        try:
            self.request.cursor.execute("SELECT full_name FROM employees")
            employee_names = [row[0] for row in self.request.cursor.fetchall()]
            self.employee_name_combobox["values"] = employee_names
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fill_task_names(self):
        try:
            self.request.cursor.execute("SELECT name FROM tasks")
            task_names = [row[0] for row in self.request.cursor.fetchall()]
            self.task_name_combobox["values"] = task_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_project(self):
        employee_name = self.employee_name_combobox.get()
        task_name = self.task_name_combobox.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            self.request.cursor.execute("SELECT id FROM employees WHERE full_name = %s", (employee_name,))
            employee_id = self.request.cursor.fetchone()
            if employee_id:
                employee_id = employee_id[0]

                self.request.cursor.execute("SELECT id FROM tasks WHERE name = %s", (task_name,))
                task_id = self.request.cursor.fetchone()
                if task_id:
                    task_id = task_id[0]

                    self.request.cursor.execute(
                        "INSERT INTO projects (employee_id, task_id, start_date, end_date) VALUES (%s, %s, %s, %s)",
                        (employee_id, task_id, start_date, end_date)
                    )
                    self.request.connection.commit()
                    messagebox.showinfo("Успех", "Проект успешно добавлен")
                else:
                    messagebox.showerror("Ошибка", "Задание не найдено")
            else:
                messagebox.showerror("Ошибка", "Сотрудник не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))