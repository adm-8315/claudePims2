import mysql.connector
from pathlib import Path

# Database connection configuration
config = {
    'user': 'root',
    'password': 'Ma4322$$',
    'host': 'localhost',
    'database': 'pims2'
}

def execute_sql_file():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Read and execute the SQL file
        sql_file = Path(__file__).parent / 'reset_migrations.sql'
        with open(sql_file, 'r') as file:
            sql = file.read()
            # Split and execute each statement separately
            statements = sql.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement.strip() + ';')
        
        # Commit the changes
        conn.commit()
        print("Successfully reset migration state")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    execute_sql_file()
