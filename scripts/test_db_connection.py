import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connections
from django.db.utils import OperationalError

def test_connection():
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
        print('Database connection successful!')
        
        # Get list of tables
        c.execute("SHOW TABLES")
        tables = c.fetchall()
        
        print('\nFound tables:')
        for table in tables:
            print(f'- {table[0]}')
            
    except OperationalError as e:
        print('Database connection failed!')
        print(f'Error: {e}')

if __name__ == '__main__':
    test_connection()