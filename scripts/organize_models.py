import os
import re
from pathlib import Path

# Model categories mapping
APP_MODELS = {
    'core': [
        'Company', 'Person', 'Location', 'Address', 'Email', 'Number',
        'Region', 'State', 'City', 'Website', 'Requirement',
        'RequirementType', 'RequirementLink',
        'CompanyCompanyPropertyLink', 'CompanyCompanyTypeLink', 'CompanyEmailLink',
        'CompanyLocatioLink', 'CompanyLocationLinkNumberLink', 
        'CompanyLocationLinkPersonLink', 'CompanyProperty', 'CompanyType'
    ],
    'users': [
        'User', 'UserLocationLink', 'Auth', 'Permission', 'PermissionApplication',
        'PermissionBlock', 'PermissionGroup', 'PermissionLink'
    ],
    'inventory': [
        'Material', 'MaterialInventory', 'MaterialTransaction', 'MaterialType',
        'Item', 'ItemInventory', 'ItemType', 'Product', 'ProductInventory',
        'ProductTransaction', 'ProductType', 'Measure', 'TransactionType'
    ],
    'production': [
        'ProductionOrder', 'ProductionOrderSchedule', 'ProductionOrderBatching',
        'Equipment', 'EquipmentStatus', 'EquipmentType', 'PreventativeMaintenance',
        'Furnace', 'FurnacePattern', 'Mixer', 'QCTest', 'Form', 'Additive',
        'Job', 'Grouping'
    ]
}

# Utility functions
def get_app_name(model_name):
    """Determine which app a model belongs to."""
    model_name = model_name.replace('Model', '')
    
    for app, models in APP_MODELS.items():
        if any(model_name.startswith(model) for model in models):
            return app
    return 'core'  # Default to core if no match found

def process_model_file(input_file):
    """Process models.py and organize models into their respective apps."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract model classes
    class_pattern = r'class\s+(\w+)\(models\.Model\):([^\n]*?\n(?:(?!class).*?\n)*)'  
    matches = re.finditer(class_pattern, content, re.MULTILINE | re.DOTALL)
    
    app_models = {
        'core': [],
        'users': [],
        'inventory': [],
        'production': []
    }
    
    for match in matches:
        model_name = match.group(1)
        model_content = match.group(0)
        app_name = get_app_name(model_name)
        app_models[app_name].append(model_content)

    # Create output files
    project_root = Path(__file__).resolve().parent.parent
    
    for app, models in app_models.items():
        if models:
            app_dir = project_root / 'apps' / app / 'models'
            app_dir.mkdir(parents=True, exist_ok=True)
            
            # Write models.py
            model_path = app_dir / 'models.py'
            with open(model_path, 'w', encoding='utf-8') as f:
                f.write('from django.db import models\n\n')
                if app != 'core':
                    f.write('from apps.core.models import *\n\n')
                f.write('\n'.join(models))
            
            # Write __init__.py if it doesn't exist
            init_path = app_dir / '__init__.py'
            if not init_path.exists():
                init_path.touch()

if __name__ == '__main__':
    input_file = Path(__file__).resolve().parent / 'models_inspection.py'
    if input_file.exists():
        process_model_file(input_file)
    else:
        print(f"Error: {input_file} not found!")