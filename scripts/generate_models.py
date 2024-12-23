import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # Generate models
    with open('models_inspection.py', 'w') as f:
        sys.stdout = f
        execute_from_command_line(['manage.py', 'inspectdb'])
        sys.stdout = sys.__stdout__

    print("Models have been generated in models_inspection.py")

if __name__ == '__main__':
    main()