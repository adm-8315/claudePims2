import os
import re
from pathlib import Path

# Model categories and their associated tables
MODEL_CATEGORIES = {
    'core': [
        'company', 'person', 'location', 'address', 'email', 'number',
        'region', 'state', 'city', 'permission', 'requirement'
    ],
    'users': [
        'user', 'auth', 'userlocationlink'
    ],
    'inventory': [
        'material', 'item', 'product', 'inventory', 'transaction'
    ],
    'production': [
        'productionorder', 'equipment', 'preventativemaintenance',
        'furnace', 'mixer', 'qctest', 'form'
    ]
}

def categorize_model(model_name):
    """Determine which app a model belongs to based on its name."""
    model_name = model_name.lower()
    
    for category, patterns in MODEL_CATEGORIES.items():
        if any(pattern in model_name for pattern in patterns):
            return category
    
    return 'core'  # Default to core if no match found

def process_models_file(input_file, output_dir):
    """Process the inspectdb output and split into appropriate app model files."""
    current_model = None
    current_category = None
    current_content = []
    
    app_contents = {
        'core': [],
        'users': [],
        'inventory': [],
        'production': []
    }
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith('class '):
            # If we have a previous model, save it
            if current_model and current_category:
                app_contents[current_category].extend(current_content)
            
            # Start new model
            current_model = re.search(r'class (\w+)', line).group(1)
            current_category = categorize_model(current_model)
            current_content = [line]
        else:
            if current_model:
                current_content.append(line)
    
    # Save the last model
    if current_model and current_category:
        app_contents[current_category].extend(current_content)
    
    # Write each app's models to its own file
    for app, content in app_contents.items():
        if content:
            app_dir = Path(output_dir) / app / 'models'
            app_dir.mkdir(parents=True, exist_ok=True)
            
            with open(app_dir / 'models.py', 'w') as f:
                f.write('from django.db import models\n\n')
                f.writelines(content)

if __name__ == '__main__':
    project_root = Path(__file__).resolve().parent.parent
    input_file = project_root / 'scripts' / 'models_inspection.py'
    output_dir = project_root / 'apps'
    
    process_models_file(input_file, output_dir)