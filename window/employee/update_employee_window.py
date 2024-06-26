import tkinter as tk
from tkinter import messagebox, ttk


class UpdateEmployeeWindow(tk.Toplevel):
    def __init__(self, parent, request):
        super().__init__(parent)
        self.request = request
        self.title("Обновить сотрудника")

        tk.Label(self, text="Полное имя:").grid(row=0, column=0, sticky='e')

        self.search_full_name_combobox = ttk.Combobox(self, state="readonly")
        self.search_full_name_combobox.grid(row=0, column=1, pady=5, padx=5)
        self.fill_employee_names()

        tk.Label(self, text="Новое полное имя:").grid(row=1, column=0, sticky='e')
        self.new_full_name_entry = tk.Entry(self)
        self.new_full_name_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self, text="Новая должность:").grid(row=2, column=0, sticky='e')
        self.new_position_entry = tk.Entry(self)
        self.new_position_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self, text="Новый департамент:").grid(row=3, column=0, sticky='e')
        self.new_department_entry = tk.Entry(self)
        self.new_department_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Button(self, text="Обновить сотрудника", command=self.update_employee).grid(row=4, column=1, pady=5)

    def fill_employee_names(self):
        try:
            self.request.cursor.execute("SELECT full_name FROM employees")
            employee_names = [row[0] for row in self.request.cursor.fetchall()]
            self.search_full_name_combobox["values"] = employee_names
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def update_employee(self):
        search_full_name = self.search_full_name_combobox.get()
        new_full_name = self.new_full_name_entry.get().strip()
        new_position = self.new_position_entry.get().strip()
        new_department = self.new_department_entry.get().strip()

        if not new_full_name:
            new_full_name = search_full_name
        if not new_position:
            new_position = self.request.cursor.execute("SELECT position FROM employees WHERE full_name = %s",
                                                       (search_full_name,))
        if not new_department:
            new_department = self.request.cursor.execute("SELECT department FROM employees WHERE full_name = %s",
                                                         (search_full_name,))

        try:
            self.request.cursor.execute(
                "UPDATE employees SET full_name = %s, position = %s, department = %s WHERE full_name = %s",
                (new_full_name, new_position, new_department, search_full_name))
            self.request.connection.commit()

            self.request.cursor.execute("SELECT * FROM employees WHERE full_name = %s", (new_full_name,))
            updated_employee = self.request.cursor.fetchone()

            updated_employee_data = f"ID: {updated_employee[0]}\nПолное имя: {updated_employee[1]}\nДолжность: {updated_employee[2]}\nДепартамент: {updated_employee[3]}\nСоздан: {updated_employee[4]}\nОбновлен: {updated_employee[5]}"

            messagebox.showinfo("Успех", f"Сотрудник был успешно обновлен.\nНовые данные:\n{updated_employee_data}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))