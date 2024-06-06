import tkinter as tk
from tkinter import ttk, messagebox

class AddTaskWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Add Task")

        tk.Label(self, text="Name:").grid(row=0, column=0, sticky='e')
        self.task_name_entry = tk.Entry(self)
        self.task_name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self, text="Description:").grid(row=0, column=0, sticky='e')
        self.task_description_entry = tk.Entry(self)
        self.task_description_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Time:").grid(row=0, column=0, sticky='e')
        self.task_time_entry = tk.Entry(self)
        self.task_time_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="Priority:").grid(row=0, column=0, sticky='e')
        self.task_priority_entry = tk.Entry(self)
        self.task_priority_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Add Task", command=self.add_task).grid(row=4, column=1, pady=5)

    def add_task(self):
        task_name = self.task_name_entry.get()
        description = self.task_description_entry.get()
        time = self.task_time_entry.get()
        priority = self.task_priority_entry.get()

        try:
            self.request.cursor.execute(
                "CALL add_task(%s, %s, %s)", (task_name, description, time, priority))
            self.request.connection.commit()
            messagebox.showinfo("Success", "Task added successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))