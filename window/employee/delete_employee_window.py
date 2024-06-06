import tkinter as tk
from tkinter import messagebox, ttk

class DeleteEmployeeWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Delete Employee")

        tk.Label(self, text="Select Full Name:").grid(row=0, column=0, sticky='e')

        # Создание и заполнение выпадающего списка с именами сотрудников
        self.full_name_combobox = ttk.Combobox(self, state="readonly")
        self.full_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        # Пустая ячейка для создания отступа
        tk.Label(self, text="").grid(row=0, column=2)

        tk.Button(self, text="Delete Employee", command=self.delete_employee).grid(row=0, column=3, pady=5)

    def fill_employee_names(self):
        try:
            self.request.cursor.execute("SELECT full_name FROM employees")
            employee_names = [row[0] for row in self.request.cursor.fetchall()]
            self.full_name_combobox["values"] = employee_names
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_employee(self):
        selected_full_name = self.full_name_combobox.get()
        try:
            self.request.cursor.execute(
                "DELETE FROM employees WHERE full_name = %s", (selected_full_name,))
            self.request.connection.commit()
            messagebox.showinfo("Success", "Employee: " + selected_full_name + " deleted successfully")
            # После удаления обновляем список с именами сотрудников
            self.fill_employee_names()
        except Exception as e:
            messagebox.showerror("Error", str(e))