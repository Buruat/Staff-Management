import tkinter as tk
from tkinter import messagebox, ttk

class DeleteTaskWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Удалить задачу")

        tk.Label(self, text="Имя задачи:").grid(row=0, column=0, sticky='e')

        # Создаем выпадающий список с именами задач
        self.task_name_combobox = ttk.Combobox(self, state="readonly")
        self.task_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_task_names()

        tk.Button(self, text="Удалить задачу", command=self.delete_task).grid(row=1, column=1, pady=5)

    def fill_task_names(self):
        try:
            self.request.cursor.execute("SELECT name FROM tasks")
            task_names = [row[0] for row in self.request.cursor.fetchall()]
            self.task_name_combobox["values"] = task_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_task(self):
        task_name = self.task_name_combobox.get()

        try:
            self.request.cursor.execute("SELECT id FROM tasks WHERE name = %s", (task_name,))
            task_id = self.request.cursor.fetchone()
            if task_id:
                task_id = task_id[0]

                self.request.cursor.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,)
                )
                self.request.connection.commit()
                messagebox.showinfo("Успех", "Задача успешно удалена")
            else:
                messagebox.showerror("Ошибка", "задача не найдена")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))