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
            CREATE OR REPLACE VIEW multi_table_view AS
            SELECT 
                e.full_name,
                e.position,
                e.department,
                eh.start_date AS employment_start_date,
                eh.end_date AS employment_end_date,
                eh.salary,
                p.start_date AS project_start_date,
                p.end_date AS project_end_date,
                t.name AS task_name,
                t.description AS task_description
            FROM 
                employees e
            JOIN 
                employment_history eh ON e.id = eh.employee_id
            JOIN 
                projects p ON e.id = p.employee_id
            JOIN 
                tasks t ON p.task_id = t.id;
        '''
        self.execute_query(create_view_query)

    def create_refresh_trigger(self):
        create_trigger_query = '''
            CREATE OR REPLACE FUNCTION refresh_multi_table_view()
            RETURNS TRIGGER AS
            $$
            BEGIN
                REFRESH MATERIALIZED VIEW multi_table_view;
                RETURN NULL;
            END;
            $$
            LANGUAGE plpgsql;

            CREATE TRIGGER refresh_multi_table_view_trigger
            AFTER INSERT OR UPDATE OR DELETE
            ON employees
            FOR EACH STATEMENT
            EXECUTE FUNCTION refresh_multi_table_view();
        '''
        self.execute_query(create_trigger_query)

    def setup_multi_table_view(self):
        self.create_multi_table_view()
        self.create_refresh_trigger()

    def get_multi_table_view(self):
        return self.execute_query('SELECT * FROM multi_table_view')

    def materialized_view(self):
        create_materialized_view_query = '''
            CREATE MATERIALIZED VIEW IF NOT EXISTS multi_table_materialized_view AS
            SELECT 
                e.full_name,
                e.position,
                e.department,
                eh.start_date AS employment_start_date,
                eh.end_date AS employment_end_date,
                eh.salary,
                p.start_date AS project_start_date,
                p.end_date AS project_end_date,
                t.name AS task_name,
                t.description AS task_description
            FROM 
                employees e
            JOIN 
                employment_history eh ON e.id = eh.employee_id
            JOIN 
                projects p ON e.id = p.employee_id
            JOIN 
                tasks t ON p.task_id = t.id;
        '''
        self.execute_query(create_materialized_view_query)

        refresh_materialized_view_query = 'REFRESH MATERIALIZED VIEW multi_table_materialized_view'
        self.execute_query(refresh_materialized_view_query)

    def get_materialized_view(self):
        return self.execute_query('SELECT * FROM multi_table_materialized_view')

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