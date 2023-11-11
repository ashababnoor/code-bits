from fuzzywuzzy import fuzz
import json

def load_schema(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_schemas(schema1, schema2):
    common_columns = []
    similar_columns = []
    
    for col1 in schema1:
        for col2 in schema2:
            if col1['name'] == col2['name'] and col1['type'] == col2['type']:
                common_columns.append((col1['name'], col1['type']))
            elif col1['type'] == col2['type'] and fuzz.ratio(col1['name'], col2['name']) > 80:
                similar_columns.append((col1['name'], col2['name'], col1['type']))
            

    return common_columns, similar_columns

