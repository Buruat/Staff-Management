class Project:
    @staticmethod
    def add_procedure(cursor):
        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE add_project(
                    employee_id INT,
                    task_id INT,
                    start_date DATE,
                    end_date DATE
                )

                LANGUAGE plpgsql
                AS $$
                BEGIN
                    INSERT INTO projects (employee_id, task_id, start_date, end_date) VALUES (employee_id, task_id, start_date, end_date);
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE delete_project(
                    project_id INT
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    DELETE FROM projects WHERE id = project_id;
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE update_project(
                    project_id INT,
                    employee_id INT,
                    task_id INT,
                    start_date DATE,
                    end_date DATE
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    UPDATE projects SET employee_id = employee_id, task_id = task_id, start_date = start_date, end_date = end_date WHERE id = project_id;
                END;
                $$;
            '''
        )