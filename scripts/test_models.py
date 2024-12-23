import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(project_root)

import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import City, State, Location, Address
from apps.inventory.models import Item, Itemtype, Iteminventory

def test_connections():
    print("Testing database connections...")
    print(f"Using project root: {project_root}")
    
    try:
        print("\nTesting City model:")
        cities = City.objects.all()
        print(f"Found {cities.count()} cities")
        
        print("\nTesting State model:")
        states = State.objects.all()
        print(f"Found {states.count()} states")
        
        print("\nTesting Location model:")
        locations = Location.objects.all()
        print(f"Found {locations.count()} locations")
        
        print("\nTesting Item model:")
        items = Item.objects.all()
        print(f"Found {items.count()} items")
        
        print("\nDatabase connection test completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == '__main__':
    test_connections()
