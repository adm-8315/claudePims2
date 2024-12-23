import os
import sys
from django.core.management import execute_from_command_line
from django.db import connections
from collections import defaultdict

def get_table_relationships():
    """Get foreign key relationships between tables"""
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            SELECT 
                TABLE_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
                REFERENCED_TABLE_SCHEMA = 'pims2'
                AND REFERENCED_TABLE_NAME IS NOT NULL;
        """)
        relationships = defaultdict(list)
        for table, column, ref_table, ref_column in cursor.fetchall():
            relationships[table].append({
                'column': column,
                'references_table': ref_table,
                'references_column': ref_column
            })
        return relationships

def get_table_counts():
    """Get row counts for each table"""
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            SELECT 
                TABLE_NAME,
                TABLE_ROWS
            FROM
                INFORMATION_SCHEMA.TABLES
            WHERE
                TABLE_SCHEMA = 'pims2';
        """)
        return dict(cursor.fetchall())

def analyze_dependencies():
    """Analyze table dependencies and suggest app organization"""
    relationships = get_table_relationships()
    counts = get_table_counts()
    
    # Define patterns for categorizing tables
    patterns = {
        'users': ['user', 'permission', 'group', 'auth'],
        'inventory': ['product', 'material', 'stock', 'item', 'category', 'inventory'],
        'production': ['equipment', 'maintenance', 'schedule', 'job', 'work'],
        'core': ['address', 'contact', 'company', 'location', 'setting']
    }
    
    # Categorize tables
    categorized = defaultdict(list)
    uncategorized = []
    
    for table in counts.keys():
        categorized_flag = False
        for app, keywords in patterns.items():
            if any(keyword in table.lower() for keyword in keywords):
                categorized[app].append({
                    'table': table,
                    'count': counts[table],
                    'relationships': relationships.get(table, [])
                })
                categorized_flag = True
                break
        if not categorized_flag:
            uncategorized.append({
                'table': table,
                'count': counts[table],
                'relationships': relationships.get(table, [])
            })
    
    # Print analysis
    print("\nDatabase Analysis Report")
    print("=" * 50)
    
    for app, tables in categorized.items():
        print(f"\n{app.upper()} App Tables:")
        print("-" * 30)
        for table in tables:
            print(f"\n  {table['table']}:")
            print(f"    Rows: {table['count']}")
            if table['relationships']:
                print("    Foreign Keys:")
                for rel in table['relationships']:
                    print(f"      - {rel['column']} → {rel['references_table']}.{rel['references_column']}")
    
    if uncategorized:
        print("\nUncategorized Tables:")
        print("-" * 30)
        for table in uncategorized:
            print(f"\n  {table['table']}:")
            print(f"    Rows: {table['count']}")
            if table['relationships']:
                print("    Foreign Keys:")
                for rel in table['relationships']:
                    print(f"      - {rel['column']} → {rel['references_table']}.{rel['references_column']}")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        analyze_dependencies()
    except Exception as e:
        print(f"Error: {e}")
