import tkinter as tk
from tkinter import messagebox, ttk

class AddTaskWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Добавить задачу")

        tk.Label(self, text="Имя задачи:").grid(row=0, column=0, sticky='e')
        self.task_name_entry = tk.Entry(self)
        self.task_name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self, text="Описание:").grid(row=1, column=0, sticky='e')
        self.description_entry = tk.Entry(self)
        self.description_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Время (HH:MM:SS):").grid(row=2, column=0, sticky='e')
        self.time_entry = tk.Entry(self)
        self.time_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="преоритет:").grid(row=3, column=0, sticky='e')
        self.priority_entry = tk.Entry(self)
        self.priority_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Добавить", command=self.add_task).grid(row=4, column=1, pady=5)

    def add_task(self):
        task_name = self.task_name_entry.get()
        description = self.description_entry.get()
        time = self.time_entry.get()
        priority = self.priority_entry.get()

        try:
            self.request.cursor.execute(
                "INSERT INTO tasks (name, description, time, priority) VALUES (%s, %s, %s, %s)",
                (task_name, description, time, priority)
            )
            self.request.connection.commit()
            messagebox.showinfo("Успех", "Задача успешно добавлена")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))