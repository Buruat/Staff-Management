import tkinter as tk
from tkinter import messagebox, ttk
from config import host, user, password, db_name, port
from request import Request  # Adjust the import according to your file structure
from window.employee.add_employee_window import AddEmployeeWindow
from window.employee.update_employee_window import UpdateEmployeeWindow
from window.employee.delete_employee_window import DeleteEmployeeWindow

from window.employee_history.add_employee_history_window import AddEmploymentHistoryWindow
from window.employee_history.update_employee_history_window import UpdateEmploymentHistoryWindow
from window.employee_history.delete_employee_history_window import DeleteEmploymentHistoryWindow

from window.task.add_task_window import AddTaskWindow

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Query Interface")

        self.request = Request()
        self.request.setup_multi_table_view()

        self.create_widgets()


    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Create buttons for each query
        tk.Button(self.root, text="Composite Query with Case", command=self.display_composite_query).pack(pady=5,
                                                                                                          anchor='e')
        tk.Button(self.root, text="Multi Table View", command=self.display_multi_table_view).pack(pady=5, anchor='e')
        tk.Button(self.root, text="Materialized View", command=self.display_materialized_view).pack(pady=5, anchor='e')
        tk.Button(self.root, text="Project with Overdailing Tasks",
                  command=self.display_project_with_overdailing_tasks).pack(pady=5, anchor='e')
        tk.Button(self.root, text="Employee Average Salary", command=self.display_employee_avg_salary).pack(pady=5,
                                                                                                            anchor='e')
        tk.Button(self.root, text="Employee Max Salary", command=self.display_employee_max_salary).pack(pady=5,
                                                                                                        anchor='e')
        tk.Button(self.root, text="Employee Projects Count", command=self.display_employee_projects_count).pack(pady=5,
                                                                                                                anchor='e')
        tk.Button(self.root, text="Employee Avg Duration", command=self.display_employee_avg_duration).pack(pady=5,
                                                                                                            anchor='e')
        tk.Button(self.root, text="Avg Department Salary", command=self.display_avg_department_salary).pack(pady=5,
                                                                                                            anchor='e')
        tk.Button(self.root, text="Projects with Highest Task Priority",
                  command=self.display_projects_with_highest_task_priority).pack(pady=5, anchor='e')
        tk.Button(self.root, text="Projects Ending in Current Year",
                  command=self.display_projects_with_ending_in_current_year).pack(pady=5, anchor='e')

        # Buttons to open new windows for employee management
        tk.Button(button_frame, text="Add Employee", command=self.open_add_employee_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Update Employee", command=self.open_update_employee_window).pack(pady=5,anchor='w')
        tk.Button(button_frame, text="Delete Employee", command=self.open_delete_employee_window).pack(pady=5,anchor='w')

        tk.Button(button_frame, text="Add Employment History", command=self.open_add_employment_history_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Update Employment History", command=self.open_update_employment_history_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Delete Employment History", command=self.open_delete_employment_history_window).pack(pady=5, anchor='w')

        tk.Button(button_frame, text="Add Task", command=self.open_add_task_window).pack(pady=5, anchor='w')

        # Create a text widget to display query results
        self.result_text = tk.Text(self.root, wrap=tk.WORD, width=100, height=20)
        self.result_text.pack(pady=20, padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

    def display_composite_query(self):
        self.display_results(self.request.composite_query_with_case())

    def display_multi_table_view(self):
        self.display_results(self.request.get_multi_table_view())

    def display_materialized_view(self):
        self.request.materialized_view()
        self.display_results(self.request.get_materialized_view())

    def display_project_with_overdailing_tasks(self):
        self.display_results(self.request.project_with_overdailing_tasks())

    def display_employee_avg_salary(self):
        self.display_results(self.request.employee_avg_salary())

    def display_employee_max_salary(self):
        self.display_results(self.request.employee_max_salary())

    def display_employee_projects_count(self):
        self.display_results(self.request.employee_projects_count())

    def display_employee_avg_duration(self):
        self.display_results(self.request.employee_avg_duration())

    def display_avg_department_salary(self):
        self.display_results(self.request.avg_department_salary())

    def display_projects_with_highest_task_priority(self):
        self.display_results(self.request.projects_with_highest_task_priority())

    def display_projects_with_ending_in_current_year(self):
        self.display_results(self.request.projects_with_ending_in_current_year())

    def display_results(self, results):
        self.result_text.delete(1.0, tk.END)
        if results:
            for row in results:
                self.result_text.insert(tk.END, str(row) + '\n')
        else:
            self.result_text.insert(tk.END, "No results found.")

    def open_add_employee_window(self):
        AddEmployeeWindow(self.root, self.request)

    def open_update_employee_window(self):
        UpdateEmployeeWindow(self.root, self.request)

    def open_delete_employee_window(self):
        DeleteEmployeeWindow(self.root, self.request)

    def open_add_employment_history_window(self):
        AddEmploymentHistoryWindow(self.root, self.request)

    def open_update_employment_history_window(self):
        UpdateEmploymentHistoryWindow(self.root, self.request)

    def open_delete_employment_history_window(self):
        DeleteEmploymentHistoryWindow(self.root, self.request)

    def open_add_task_window(self):
        AddTaskWindow(self.root, self.request)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()