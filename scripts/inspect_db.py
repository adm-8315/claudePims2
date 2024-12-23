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

from django.core.management import call_command

def main():
    """
    Run Django's inspectdb command and save the output to a file.
    """
    output_file = project_root / 'scripts' / 'models_inspection.py'
    
    # Open the file in write mode
    with open(output_file, 'w', encoding='utf-8') as f:
        # Call inspectdb and redirect output to our file
        call_command('inspectdb', stdout=f)
    
    print(f"Models have been written to {output_file}")

if __name__ == '__main__':
    main()