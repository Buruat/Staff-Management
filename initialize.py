import psycopg2
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
        # Создаем таблицу employees
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(100),
                position VARCHAR(100),
                department VARCHAR(100)
            )
            '''
        )

        # Создаем таблицу employment_history
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employment_history (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id),
                start_date DATE,
                end_date DATE,
                salary NUMERIC(10, 2),
                CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
            '''
        )

        # Создаем таблицу tasks
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                description TEXT,
                time TIME,
                priority NUMERIC(10, 2)
            )
            '''
        )

        # Создаем таблицу projects
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                employee_id INTEGER REFERENCES employees(id),
                task_id INTEGER REFERENCES tasks(id),
                start_date DATE,
                end_date DATE,
                CONSTRAINT fk_employee_project FOREIGN KEY (employee_id) REFERENCES employees(id),
                CONSTRAINT fk_task_project FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
            '''
        )

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
