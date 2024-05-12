import psycopg2
from models.employee import Employee
from models.employment_history import EmploymentHistory
from models.task import Task
from models.project import Project
from config import host, user, password, db_name, port

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        port=port
    )

    with connection.cursor() as cursor:
        cursor.execute('''
                            CREATE OR REPLACE FUNCTION update_created_at()
                            RETURNS TRIGGER AS $$
                            BEGIN
                                NEW.created_at = CURRENT_TIMESTAMP;
                                RETURN NEW;
                            END;
                            $$ LANGUAGE plpgsql;
                        ''')

        cursor.execute('''
                            CREATE OR REPLACE FUNCTION update_updated_at()
                            RETURNS TRIGGER AS $$
                            BEGIN
                                NEW.updated_at = CURRENT_TIMESTAMP;
                                RETURN NEW;
                            END;
                            $$ LANGUAGE plpgsql;
                        ''')

        # Создаем таблицу employees
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(100),
                position VARCHAR(100),
                department VARCHAR(100),
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
            '''
        )

        cursor.execute('''
                    CREATE TRIGGER update_created_at_trigger
                    BEFORE INSERT ON employees
                    FOR EACH ROW
                    EXECUTE FUNCTION update_created_at();
                ''')
        cursor.execute('''
                    CREATE TRIGGER update_updated_at_trigger
                    BEFORE UPDATE ON employees
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at();
                ''')

        # Создаем таблицу employment_history
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employment_history (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id),
                start_date DATE,
                end_date DATE,
                salary NUMERIC(10, 2),
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
            '''
        )

        cursor.execute('''
                    CREATE TRIGGER update_created_at_employment_history_trigger
                    BEFORE INSERT ON employment_history
                    FOR EACH ROW
                    EXECUTE FUNCTION update_created_at();
                ''')
        cursor.execute('''
                    CREATE TRIGGER update_updated_at_employment_history_trigger
                    BEFORE UPDATE ON employment_history
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at();
                ''')

        # Создаем таблицу tasks
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                description TEXT,
                time TIME,
                priority NUMERIC(10, 2),
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
            '''
        )

        cursor.execute('''
                    CREATE TRIGGER update_created_at_tasks_trigger
                    BEFORE INSERT ON tasks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_created_at();
                ''')
        cursor.execute('''
                    CREATE TRIGGER update_updated_at_tasks_trigger
                    BEFORE UPDATE ON tasks
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at();
                ''')

        # Создаем таблицу projects
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id),
                task_id INTEGER REFERENCES tasks(id),
                start_date DATE,
                end_date DATE,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                CONSTRAINT fk_employee_project FOREIGN KEY (employee_id) REFERENCES employees(id),
                CONSTRAINT fk_task_project FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
            '''
        )

        cursor.execute('''
                    CREATE TRIGGER update_created_at_projects_trigger
                    BEFORE INSERT ON projects
                    FOR EACH ROW
                    EXECUTE FUNCTION update_created_at();
                ''')
        cursor.execute('''
                    CREATE TRIGGER update_updated_at_projects_trigger
                    BEFORE UPDATE ON projects
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at();
                ''')

        Employee.add_procedure(cursor)
        EmploymentHistory.add_procedure(cursor)
        Task.add_procedure(cursor)
        Project.add_procedure(cursor)

        cursor.execute('''
            CREATE OR REPLACE PROCEDURE process_employee_for_internship(employee_name VARCHAR(100), department VARCHAR(100))
            LANGUAGE plpgsql
            AS $$
            DECLARE
                employee_id INT;
                history_id INT;
            BEGIN
                -- Начало транзакции
                BEGIN
                    -- Операция добавления нового сотрудника
                    CALL add_employee(employee_name, 'Intern', department) INTO employee_id;

                    -- Операция добавления записи в историю занятости
                    CALL add_employment_history(employee_id, CURRENT_DATE, CURRENT_DATE + INTERVAL '3 month', 25000);

                    -- Если операции выполнены успешно, фиксируем транзакцию
                    COMMIT;
                EXCEPTION
                    -- Если возникла ошибка, откатываем транзакцию
                    WHEN OTHERS THEN
                        ROLLBACK;
                        RAISE;
                END;
            END;
            $$;
        ''')

        cursor.execute('''
                    CREATE OR REPLACE FUNCTION double_value(x INTEGER) RETURNS INTEGER AS $$
                    DECLARE
                        result INTEGER;
                    BEGIN
                        result := x * 2;
                        RETURN result;
                    END;
                    $$ LANGUAGE plpgsql;
                ''')

        cursor.execute('''
                    CREATE OR REPLACE FUNCTION double_values(values INTEGER[]) RETURNS SETOF INTEGER AS $$
                    DECLARE
                        i INTEGER;
                    BEGIN
                        FOR i IN array_lower(values, 1)..array_upper(values, 1) LOOP
                            RETURN NEXT values[i] * 2;
                        END LOOP;
                        RETURN;
                    END;
                    $$ LANGUAGE plpgsql;
                ''')

        cursor.execute('SELECT * FROM employees')

        if not cursor.fetchall():
            # Заполняем таблицу employees
            cursor.execute(
                '''
                INSERT INTO employees (full_name, position, department)
                VALUES
                ('John Doe', 'Manager', 'HR'),
                ('Jane Smith', 'Developer', 'Engineering'),
                ('Alice Johnson', 'Analyst', 'Finance')
                '''
            )

            # Заполняем таблицу employment_history
            cursor.execute(
                '''
                INSERT INTO employment_history (employee_id, start_date, end_date, salary) 
                VALUES 
                (1, '2022-01-01', '2022-12-31', 50000),
                (2, '2022-02-01', '2022-12-31', 60000),
                (3, '2022-03-01', '2022-12-31', 70000)
                '''
            )

            # Заполняем таблицу tasks
            cursor.execute(
                '''
                INSERT INTO tasks (name, description, time, priority) 
                VALUES 
                ('Task 1', 'Description 1', '10:00:00', 1),
                ('Task 2', 'Description 2', '11:00:00', 2),
                ('Task 3', 'Description 3', '18:00:00', 3)
                '''
            )

            # Заполняем таблицу projects
            cursor.execute(
                '''
                INSERT INTO projects (employee_id, task_id, start_date, end_date) 
                VALUES 
                (1, 1, '2022-01-01', '2022-12-31'),
                (2, 2, '2022-02-01', '2022-12-31'),
                (3, 3, '2022-03-01', '2022-12-31')
                '''
            )

        connection.commit()
        cursor.close()
        connection.close()

except Exception as ex:
    print(ex)
