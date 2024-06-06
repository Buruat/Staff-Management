import tkinter as tk
from tkinter import messagebox, ttk

class UpdateTaskWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Обновить задачу")

        tk.Label(self, text="Имя задачи:").grid(row=0, column=0, sticky='e')

        self.task_name_combobox = ttk.Combobox(self, state="readonly")
        self.task_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_task_names()

        tk.Label(self, text="Новое имя задачи:").grid(row=1, column=0, sticky='e')
        self.new_task_name_entry = tk.Entry(self)
        self.new_task_name_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Описание:").grid(row=2, column=0, sticky='e')
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="Время (HH:MM:SS):").grid(row=3, column=0, sticky='e')
        self.time_entry = tk.Entry(self)
        self.time_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(self, text="Преоритет:").grid(row=4, column=0, sticky='e')
        self.priority_entry = tk.Entry(self)
        self.priority_entry.grid(row=4, column=1, pady=5, padx=5)

        tk.Button(self, text="Обновить задачу", command=self.update_task).grid(row=5, column=1, pady=5)

    def fill_task_names(self):
        try:
            self.request.cursor.execute("SELECT name FROM tasks")
            task_names = [row[0] for row in self.request.cursor.fetchall()]
            self.task_name_combobox["values"] = task_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_task(self):
        task_name = self.task_name_combobox.get()
        new_task_name = self.new_task_name_entry.get().strip()
        description = self.description_entry.get().strip()
        time = self.time_entry.get().strip()
        priority = self.priority_entry.get().strip()

        update_values = []

        update_query_parts = []

        if new_task_name:
            update_values.append(new_task_name)
            update_query_parts.append("name = %s")
        if description:
            update_values.append(description)
            update_query_parts.append("description = %s")
        if time:
            update_values.append(time)
            update_query_parts.append("time = %s")
        if priority:
            update_values.append(priority)
            update_query_parts.append("priority = %s")


        if update_values:
            try:
                self.request.cursor.execute("SELECT id FROM tasks WHERE name = %s", (task_name,))
                task_id = self.request.cursor.fetchone()
                if task_id:
                    task_id = task_id[0]

                    update_query = "UPDATE tasks SET " + ", ".join(
                        update_query_parts) + ", updated_at = CURRENT_TIMESTAMP WHERE id = %s"

                    update_values.append(task_id)

                    self.request.cursor.execute(update_query, tuple(update_values))
                    self.request.connection.commit()
                    messagebox.showinfo("Успех", "Задача успешно обновлена")
                else:
                    messagebox.showerror("Ошибка", "Задача не найдена")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        else:
            messagebox.showerror("Ошибка", "Поля пусты")