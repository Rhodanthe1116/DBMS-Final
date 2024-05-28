from sqlalchemy import Column, Integer, Text, Float, Numeric, BLOB, String, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Utility function to format field names (you need to define this based on your specific formatting rules)
def format_field_name(name):
    # Example formatting function: convert to snake_case
    import re
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name

# Function to map column types
def transform_column_to_type(column_type):
    c = column_type.lower()

    if 'int' in c:
        return Integer
    if 'char' in c or c == 'clob' or c == 'text':
        return Text
    if 'double' in c or c == 'real' or c == 'float':
        return Float
    if 'decimal' in c or 'numeric' in c or c == 'boolean' or c == 'date' or c == 'datetime':
        return Numeric
    return BLOB

# Main function to transform columns
def transform_columns(columns):
    transformed_columns = {}
    for column in columns:
        field_name = format_field_name(column['name'])
        column_type = transform_column_to_type(column['type'])
        
        transformed_columns[field_name] = {
            'type': column_type,
            'primary_key': column['pk'] == 1,
            'field': column['name'],
            'nullable': column['notnull'] == 0 or column['dflt_value'] is not None,
            'default': column['dflt_value'],
            'autoincrement': column['type'] == 'INTEGER' and column['pk'] == 1,
        }

    return transformed_columns

# # Example usage
# columns = [
#     {'name': 'id', 'type': 'INTEGER', 'pk': 1, 'notnull': 1, 'dflt_value': None},
#     {'name': 'username', 'type': 'VARCHAR(255)', 'pk': 0, 'notnull': 1, 'dflt_value': None},
#     {'name': 'created_at', 'type': 'DATETIME', 'pk': 0, 'notnull': 1, 'dflt_value': 'CURRENT_TIMESTAMP'},
# ]

# transformed = transform_columns(columns)
# print(transformed)