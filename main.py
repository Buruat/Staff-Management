import tkinter as tk

from request import Request
from window.employee.add_employee_window import AddEmployeeWindow
from window.employee.update_employee_window import UpdateEmployeeWindow
from window.employee.delete_employee_window import DeleteEmployeeWindow

from window.employee_history.add_employee_history_window import AddEmploymentHistoryWindow
from window.employee_history.update_employee_history_window import UpdateEmploymentHistoryWindow
from window.employee_history.delete_employee_history_window import DeleteEmploymentHistoryWindow

from window.task.add_task_window import AddTaskWindow
from window.task.delete_task_window import DeleteTaskWindow
from window.task.update_task_window import UpdateTaskWindow

from window.project.add_project_window import AddProjectWindow
from window.project.delete_project_window import DeleteProjectWindow
from window.project.update_project_window import UpdateProjectWindow

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

        tk.Button(self.root, text="Общая ЗП по департаментам", command=self.display_materialized_view).pack(pady=5, anchor='e')

        tk.Button(self.root, text="Средняя зарплата сотрудников", command=self.display_employee_avg_salary).pack(pady=5,
                                                                                                            anchor='e')
        tk.Button(self.root, text="Максимальная зарплата сотрудников", command=self.display_employee_max_salary).pack(pady=5,
                                                                                                        anchor='e')
        tk.Button(self.root, text="Количество проектов у сотрудников", command=self.display_employee_projects_count).pack(pady=5,
                                                                                                                anchor='e')
        tk.Button(self.root, text="Средняя длительность работы сотрудников", command=self.display_employee_avg_duration).pack(pady=5,
                                                                                                            anchor='e')
        tk.Button(self.root, text="Средняя зарплата по отделам", command=self.display_avg_department_salary).pack(pady=5,
                                                                                                            anchor='e')

        tk.Button(button_frame, text="Добавить сотрудника", command=self.open_add_employee_window).pack(pady=5,
                                                                                                        anchor='w')
        tk.Button(button_frame, text="Обновить данные о сотруднике", command=self.open_update_employee_window).pack(
            pady=5, anchor='w')
        tk.Button(button_frame, text="Удалить сотрудника", command=self.open_delete_employee_window).pack(pady=5,
                                                                                                          anchor='w')

        tk.Button(button_frame, text="Добавить историю занятости",
                  command=self.open_add_employment_history_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Обновить историю занятости",
                  command=self.open_update_employment_history_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Удалить историю занятости",
                  command=self.open_delete_employment_history_window).pack(pady=5, anchor='w')

        tk.Button(button_frame, text="Добавить задачу", command=self.open_add_task_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Обновить задачу", command=self.open_update_task_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Удалить задачу", command=self.open_delete_task_window).pack(pady=5, anchor='w')

        tk.Button(button_frame, text="Добавить проект", command=self.open_add_project_window).pack(pady=5, anchor='w')
        tk.Button(button_frame, text="Обновить проект", command=self.open_update_project_window).pack(pady=5,
                                                                                                      anchor='w')
        tk.Button(button_frame, text="Удалить проект", command=self.open_delete_project_window).pack(pady=5, anchor='w')

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

    def open_delete_task_window(self):
        DeleteTaskWindow(self.root, self.request)

    def open_update_task_window(self):
        UpdateTaskWindow(self.root, self.request)

    def open_add_project_window(self):
        AddProjectWindow(self.root, self.request)

    def open_delete_project_window(self):
        DeleteProjectWindow(self.root, self.request)

    def open_update_project_window(self):
        UpdateProjectWindow(self.root, self.request)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()