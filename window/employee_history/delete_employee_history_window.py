import tkinter as tk
from tkinter import messagebox, ttk

class DeleteEmploymentHistoryWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Удалить историю сотрудника")

        tk.Label(self, text="Имя сотрудника:").grid(row=0, column=0, sticky='e')

        self.employee_name_combobox = ttk.Combobox(self, state="readonly")
        self.employee_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        tk.Button(self, text="Удалить историю сотрудника", command=self.delete_employment_history).grid(row=1, column=1, pady=5)

    def fill_employee_names(self):
        try:
            self.request.cursor.execute("SELECT full_name FROM employees")
            employee_names = [row[0] for row in self.request.cursor.fetchall()]
            self.employee_name_combobox["values"] = employee_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_employment_history(self):
        employee_name = self.employee_name_combobox.get()

        try:
            self.request.cursor.execute("SELECT id FROM employees WHERE full_name = %s", (employee_name,))
            employee_id = self.request.cursor.fetchone()
            if employee_id:
                employee_id = employee_id[0]

                self.request.cursor.execute(
                    "DELETE FROM employment_history WHERE employee_id = %s",
                    (employee_id,)
                )
                self.request.connection.commit()
                messagebox.showinfo("Успех", "История сотрудника удалена")
            else:
                messagebox.showerror("Ошибка", "Сотрудник не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))