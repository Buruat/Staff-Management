class EmploymentHistory:
    @staticmethod
    def add_procedure(cursor):
        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE add_employment_history(
                    employee_id INTEGER,
                    start_date DATE,
                    end_date DATE,
                    salary NUMERIC
                )
                
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    INSERT INTO employment_history (employee_id, start_date, end_date, salary) VALUES (employee_id, start_date, end_date, salary);
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE delete_employment_history(
                    employment_history_id INT
                )
    
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    DELETE FROM employment_history WHERE id = employment_history_id;
                END;
                $$;
            '''
        )

        cursor.execute(
            '''
                CREATE OR REPLACE PROCEDURE update_employment_history(
                    employment_history_id INTEGER,
                    employee_id INTEGER,
                    start_date DATE,
                    end_date DATE,
                    salary NUMERIC
                )
                LANGUAGE plpgsql
                AS $$
                BEGIN
                    UPDATE employment_history SET employee_id = employee_id, start_date = start_date, end_date = end_date, salary = salary WHERE id = employment_history_id;
                END;
                $$;
            '''
        )