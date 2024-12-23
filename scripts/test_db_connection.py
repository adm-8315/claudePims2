import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def test_database_connection():
    try:
        # Attempt to connect to the database
        connection = connections['default']
        connection.cursor()
        print("Successfully connected to the database!")
        
        # Get database version
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Database version: {version[0]}")
            
            # Get list of tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("\nDatabase tables:")
            for table in tables:
                print(f"- {table[0]}")
                
    except OperationalError as e:
        print(f"Failed to connect to the database. Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_database_connection()