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
            

    return common_columns, similar_columns, schema1_columns


schema2 = load_schema('schema1.json')
schema1 = load_schema('schema2.json')

common_columns, similar_columns, schema1_columns = compare_schemas(schema1, schema2)

print("Common columns:")
for col, type in common_columns:
    print(f"{col}, {type}")

print("\nSimilar columns:")
for col1, col2, type in similar_columns:
    # print(f"{col1} (in schema1) and {col2} (in schema2) have similar data types.")
    print(f"{col1}, {col2}, {type}")

