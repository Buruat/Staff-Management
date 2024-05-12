class Task:
    @staticmethod
    def add_procedure(cursor):
        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE add_task(
                    task_name VARCHAR(100),
                    task_description TEXT,
                    task_time TIME,
                    task_priority NUMERIC(10, 2)
                )

                LANGUAGE plpgsql
                AS $$
                BEGIN
                    INSERT INTO tasks (name, description, time, priority) VALUES (task_name, task_description, task_time, task_priority);
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE delete_task(
                    task_id INT
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    DELETE FROM tasks WHERE id = task_id;
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE update_task(
                    task_id INT,
                    task_name VARCHAR(100),
                    task_description TEXT,
                    task_time TIME,
                    task_priority NUMERIC(10, 2)
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    UPDATE tasks SET name = task_name, description = task_description, time = task_time, priority = task_priority WHERE id = task_id;
                END;
                $$;
            '''
        )