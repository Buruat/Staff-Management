class Employee:
    @staticmethod
    def add_procedure(cursor):
        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE add_employee(
                    full_name VARCHAR(100),
                    "position" VARCHAR(100),
                    department VARCHAR(100)
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    INSERT INTO employees (full_name, position, department) VALUES (full_name, position, department);
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE delete_employee(
                    employee_id INT
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    DELETE FROM employees WHERE id = employee_id;
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE update_employee(
                    employee_id INT,
                    new_full_name VARCHAR(100),
                    new_position VARCHAR(100),
                    new_department VARCHAR(100)
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    UPDATE employees SET full_name = new_full_name, position = new_position, department = new_department WHERE id = employee_id;
                END;
                $$;
            '''
        )