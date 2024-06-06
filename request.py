import psycopg2
from config import host, user, password, db_name, port

class Request:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query):
        self.cursor.execute(query)
        if self.cursor.rowcount > 0:
            return self.cursor.fetchall()
        else:
            return None

    def composite_query_with_case(self):
        query = '''
            SELECT 
                e.full_name,
                e.position,
                e.department,
                eh.salary,
                CASE
                    WHEN eh.salary > 70000 THEN 'Высокая ЗП'
                    WHEN eh.salary > 60000 THEN 'Средняя ЗП'
                    ELSE 'Низкая ЗП'
                END AS salary_category
            FROM 
                employees e
            JOIN 
                employment_history eh ON e.id = eh.employee_id
            '''
        return self.execute_query(query)

    def create_multi_table_view(self):
        create_view_query = '''
            CREATE OR REPLACE VIEW employee_projects_view AS
            SELECT 
                e.id AS employee_id,
                e.full_name,
                e.position,
                e.department,
                eh.start_date AS employment_start_date,
                eh.end_date AS employment_end_date,
                eh.salary,
                p.id AS project_id,
                p.start_date AS project_start_date,
                p.end_date AS project_end_date,
                t.name AS task_name,
                t.description AS task_description
            FROM employees e
            JOIN employment_history eh ON e.id = eh.employee_id
            JOIN projects p ON e.id = p.employee_id
            JOIN tasks t ON p.task_id = t.id;
        '''
        self.execute_query(create_view_query)

    def create_rules_for_multitable_view(self):
        create_insert_rule = '''
            CREATE OR REPLACE RULE employee_projects_view_insert AS
            ON INSERT TO employee_projects_view DO INSTEAD (
                INSERT INTO employees (full_name, position, department) 
                VALUES (NEW.full_name, NEW.position, NEW.department);

                INSERT INTO employment_history (employee_id, start_date, end_date, salary) 
                VALUES ((SELECT id FROM employees WHERE full_name = NEW.full_name), NEW.employment_start_date, NEW.employment_end_date, NEW.salary);

                INSERT INTO tasks (name, description) 
                VALUES (NEW.task_name, NEW.task_description);

                INSERT INTO projects (employee_id, task_id, start_date, end_date) 
                VALUES ((SELECT id FROM employees WHERE full_name = NEW.full_name), (SELECT id FROM tasks WHERE name = NEW.task_name), NEW.project_start_date, NEW.project_end_date);
            );
        '''
        self.execute_query(create_insert_rule)

        create_update_rule = '''
            CREATE OR REPLACE RULE employee_projects_view_update AS
            ON UPDATE TO employee_projects_view DO INSTEAD (
                UPDATE employees SET 
                    full_name = NEW.full_name, 
                    position = NEW.position, 
                    department = NEW.department 
                WHERE id = OLD.employee_id;

                UPDATE employment_history SET 
                    start_date = NEW.employment_start_date, 
                    end_date = NEW.employment_end_date, 
                    salary = NEW.salary 
                WHERE employee_id = OLD.employee_id;

                UPDATE tasks SET 
                    name = NEW.task_name, 
                    description = NEW.task_description 
                WHERE id = (SELECT task_id FROM projects WHERE id = OLD.project_id);

                UPDATE projects SET 
                    start_date = NEW.project_start_date, 
                    end_date = NEW.project_end_date 
                WHERE id = OLD.project_id;
            );
        '''
        self.execute_query(create_update_rule)

        create_delete_rule = '''
            CREATE OR REPLACE RULE employee_projects_view_delete AS
            ON DELETE TO employee_projects_view DO INSTEAD (
                DELETE FROM projects WHERE id = OLD.project_id;
                DELETE FROM tasks WHERE id = (SELECT task_id FROM projects WHERE id = OLD.project_id);
                DELETE FROM employment_history WHERE employee_id = OLD.employee_id;
                DELETE FROM employees WHERE id = OLD.employee_id;
            );
        '''
        self.execute_query(create_delete_rule)

    def setup_multi_table_view(self):
        self.create_multi_table_view()
        self.create_rules_for_multitable_view()

    def get_multi_table_view(self):
        return self.execute_query('SELECT * FROM employee_projects_view')

    def materialized_view(self):
        create_materialized_view_query = '''
            CREATE MATERIALIZED VIEW IF NOT EXISTS department_salaries AS
            SELECT department, SUM(salary) AS total_salary
            FROM employees e
            JOIN employment_history eh ON e.id = eh.employee_id
            GROUP BY department;
        '''
        self.execute_query(create_materialized_view_query)

        refresh_materialized_view_query = 'REFRESH MATERIALIZED VIEW department_salaries'
        self.execute_query(refresh_materialized_view_query)

    def get_materialized_view(self):
        return self.execute_query('SELECT * FROM department_salaries')

    def project_with_overdailing_tasks(self):
        project_with_overdailing_tasks = '''
            SELECT 
                p.id,
                p.employee_id,
                p.task_id,
                p.start_date,
                p.end_date
            FROM 
                projects p
            JOIN 
                (SELECT id FROM tasks WHERE time > INTERVAL '8 hours') AS t ON p.task_id = t.id;
        '''

        return self.execute_query(project_with_overdailing_tasks)

    def employee_avg_salary(self):
        avg_salary = '''
            SELECT 
                full_name, 
                (SELECT ROUND(AVG(salary), 2) FROM employment_history WHERE employee_id = employees.id) AS avg_salary
            FROM 
                employees;
        '''

        return self.execute_query(avg_salary)

    def employee_max_salary(self):
        max_salary = '''
                SELECT 
                    e.full_name, 
                    (SELECT MAX(eh.salary) FROM employment_history eh WHERE eh.employee_id = e.id) AS max_salary
                FROM employees e;
        '''

        return self.execute_query(max_salary)


    def employee_projects_count(self):
        projects_count = '''
                SELECT 
                    e.full_name,
                    (SELECT COUNT(*) FROM projects p WHERE p.employee_id = e.id) AS project_count
                FROM employees e;
        '''

        return self.execute_query(projects_count)

    def employee_avg_duration(self):
        avg_employment = '''
                    SELECT 
                        e.full_name,
                        (SELECT ROUND(AVG(EXTRACT(DAY FROM (p.end_date::TIMESTAMP - p.start_date::TIMESTAMP))))
                         FROM projects p 
                         WHERE p.employee_id = e.id) AS avg_project_duration
                    FROM 
                        employees e;
        '''

        return self.execute_query(avg_employment)

    def avg_department_salary(self):
        avg_department_salary = '''
            SELECT 
                e.department,
                ROUND(AVG(eh.salary)) AS avg_salary
            FROM 
                employees e
            JOIN 
                employment_history eh ON e.id = eh.employee_id
            GROUP BY 
                e.department
            HAVING 
                AVG(eh.salary) >= 60000;
        '''

        return self.execute_query(avg_department_salary)

    def projects_with_highest_task_priority(self):
        projects_with_highest_task_priority = '''
            SELECT *
            FROM projects
            WHERE task_id = ANY (
                SELECT id
                FROM tasks
                WHERE priority = 1
            );
        '''

        return self.execute_query(projects_with_highest_task_priority)

    def projects_with_ending_in_current_year(self):
        projects_with_ending_in_current_year = '''
            SELECT *
            FROM projects
            WHERE end_date <= ALL (
                SELECT date_trunc('year', CURRENT_DATE) + INTERVAL '1 year' - INTERVAL '1 day'
            );
        '''

        return self.execute_query(projects_with_ending_in_current_year)

    def get_table_data(self, table_name):
        query = 'SELECT * FROM {}'.format(table_name)
        rows = self.execute_query(query)
        for row in rows:
            print(row)