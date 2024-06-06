import tkinter as tk
from tkinter import messagebox, ttk

class AddEmployeeWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Add Employee")

        tk.Label(self, text="Full Name:").grid(row=0, column=0, sticky='e')
        self.full_name_entry = tk.Entry(self)
        self.full_name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(self, text="Position:").grid(row=1, column=0, sticky='e')
        self.position_entry = tk.Entry(self)
        self.position_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Department:").grid(row=2, column=0, sticky='e')
        self.department_entry = tk.Entry(self)
        self.department_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self, text="Add Employee", command=self.add_employee).grid(row=3, column=1, pady=5)

    def add_employee(self):
        full_name = self.full_name_entry.get()
        position = self.position_entry.get()
        department = self.department_entry.get()
        try:
            self.request.cursor.execute(
                "CALL add_employee(%s, %s, %s)", (full_name, position, department))
            self.request.connection.commit()
            messagebox.showinfo("Success", "Employee added successfully:" + full_name + ', ' + position + ', ' + department)
        except Exception as e:
            messagebox.showerror("Error", str(e))