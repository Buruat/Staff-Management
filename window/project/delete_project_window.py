import tkinter as tk
from tkinter import messagebox, ttk

class DeleteProjectWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Удалить проект")

        tk.Label(self, text="Имя сотрудника:").grid(row=0, column=0, sticky='e')

        self.employee_name_combobox = ttk.Combobox(self, state="readonly")
        self.employee_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        tk.Label(self, text="Имя задачи:").grid(row=1, column=0, sticky='e')

        self.task_name_combobox = ttk.Combobox(self, state="readonly")
        self.task_name_combobox.grid(row=1, column=1, pady=5, padx=5)
        self.fill_task_names()

        tk.Button(self, text="Удалить проект", command=self.delete_project).grid(row=2, column=1, pady=5)

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

    def delete_project(self):
        employee_name = self.employee_name_combobox.get()
        task_name = self.task_name_combobox.get()

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
                        "DELETE FROM projects WHERE employee_id = %s AND task_id = %s",
                        (employee_id, task_id)
                    )
                    rows_deleted = self.request.cursor.rowcount
                    if rows_deleted > 0:
                        self.request.connection.commit()
                        messagebox.showinfo("Success", "Проект успешно удален")
                    else:
                        messagebox.showerror("Ошибка", "Проект не найден")
                else:
                    messagebox.showerror("Ошибка", "Задание не найдено")
            else:
                messagebox.showerror("Ошибка", "Сотрудник не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))