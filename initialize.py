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

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employment_history (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
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


        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
                task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
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

        cursor.execute('CREATE INDEX idx_employees_full_name ON employees USING btree (full_name);')
        cursor.execute('CREATE INDEX idx_employment_history_employee_id ON employment_history USING hash (start_date);')
        cursor.execute('CREATE INDEX idx_tasks_description_spgist ON tasks USING spgist (description);')

        cursor.execute('''
                    CREATE OR REPLACE PROCEDURE update_task_priorities()
                    LANGUAGE plpgsql
                    AS $$
                    DECLARE
                        task_record RECORD;
                        new_priority NUMERIC(10, 2);
                        task_cursor CURSOR FOR SELECT id, time FROM tasks;
                    BEGIN
                        OPEN task_cursor;
                        LOOP
                            FETCH task_cursor INTO task_record;
                            EXIT WHEN NOT FOUND;

                            -- Пример вычисления нового значения priority
                            IF task_record.time < '12:00:00' THEN
                                new_priority := 1;
                            ELSE
                                new_priority := 2;
                            END IF;

                            -- Обновление записи
                            UPDATE tasks
                            SET priority = new_priority
                            WHERE id = task_record.id;
                        END LOOP;
                        CLOSE task_cursor;
                    END;
                    $$;
                ''')


        cursor.execute('''
                    CREATE OR REPLACE FUNCTION calculate_total_salary(employee_id INTEGER) RETURNS NUMERIC AS $$
                    DECLARE
                        total_salary NUMERIC := 0;
                    BEGIN
                        SELECT SUM(salary) INTO total_salary FROM employment_history WHERE employee_id = employee_id;
                        RETURN total_salary;
                    END;
                    $$ LANGUAGE plpgsql;
                ''')

        cursor.execute('''
                    CREATE OR REPLACE FUNCTION get_employee_projects(employee_id INTEGER) 
                    RETURNS TABLE (project_id INTEGER, task_id INTEGER, start_date DATE, end_date DATE) AS $$
                    BEGIN
                        RETURN QUERY SELECT id, task_id, start_date, end_date FROM projects WHERE employee_id = employee_id;
                    END;
                    $$ LANGUAGE plpgsql;
                ''')

        cursor.execute('''
                    CREATE OR REPLACE FUNCTION transactional_procedure()
                    RETURNS VOID AS $$
                    BEGIN
                        SELECT * FROM employees;

                        INSERT INTO employment_history (employee_id, start_date, end_date, salary) 
                        VALUES (1, '2024-01-01', '2024-12-31', 80000);

                        DELETE FROM projects 
                        WHERE id = 1;

                        COMMIT;
                    EXCEPTION
                        WHEN OTHERS THEN
                            RAISE NOTICE 'An error occurred: %', SQLERRM;
                            ROLLBACK;
                    END;
                    $$ LANGUAGE plpgsql;
                ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_performance (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
                task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
                completion_date DATE,
                completion_time TIME,
                performance_metric NUMERIC(10, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        cursor.execute('SELECT * FROM employees')

        if not cursor.fetchall():
            cursor.execute('''
                        DO $$
                        BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'read_only_role') THEN
                                CREATE ROLE read_only_role;
                            END IF;
                        END
                        $$;
                        DO $$
                        BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'write_role') THEN
                                CREATE ROLE write_role;
                            END IF;
                        END
                        $$;
                        DO $$
                        BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'read_only_user') THEN
                                CREATE USER read_only_user WITH PASSWORD 'password1';
                            END IF;
                        END
                        $$;
                        DO $$
                        BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'write_user') THEN
                                CREATE USER write_user WITH PASSWORD 'password2';
                            END IF;
                        END
                        $$;
                        GRANT CONNECT ON DATABASE postgres TO read_only_role, write_role;
                        GRANT USAGE ON SCHEMA public TO read_only_role, write_role;
                        
                        GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_role;
                        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_only_role;
                        
                        GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO write_role;
                        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO write_role;
                        
                        GRANT read_only_role TO read_only_user;
                        GRANT write_role TO write_user;
                    ''')

            for i in range(1, 100000):
                cursor.execute(
                    '''
                    INSERT INTO employees (full_name, position, department)
                    VALUES ('Sample', 'Manager', 'HR')
                    '''
                )
                cursor.execute(
                    '''
                    INSERT INTO employment_history (employee_id, start_date, end_date, salary) 
                    VALUES 
                    (1, '2022-01-02', '2022-12-31', 50000)
                    '''
                )
                cursor.execute(
                    '''
                    INSERT INTO tasks (name, description, time, priority) 
                    VALUES 
                    ('Task 1', 'Description 2', '10:00:00', 1)
                    '''
                )


            cursor.execute(
                '''
                INSERT INTO employees (full_name, position, department)
                VALUES
                ('John Doe', 'Manager', 'HR'),
                ('Jane Smith', 'Developer', 'Engineering'),
                ('Alice Johnson', 'Analyst', 'Finance')
                '''
            )

            cursor.execute(
                '''
                INSERT INTO employment_history (employee_id, start_date, end_date, salary) 
                VALUES 
                (1, '2022-01-01', '2022-12-31', 50000),
                (2, '2022-02-01', '2022-12-31', 60000),
                (3, '2022-03-01', '2022-12-31', 70000)
                '''
            )

            cursor.execute(
                '''
                INSERT INTO tasks (name, description, time, priority) 
                VALUES 
                ('Task 1', 'Description 1', '10:00:00', 1),
                ('Task 2', 'Description 2', '11:00:00', 2),
                ('Task 3', 'Description 3', '18:00:00', 3)
                '''
            )

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
