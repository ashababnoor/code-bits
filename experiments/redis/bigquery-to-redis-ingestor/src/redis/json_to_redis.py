import json

def json_to_redis_commands(json_str, output_file):
    # Parse the JSON string
    data = json.loads(json_str)
    
    # Initialize a list to store Redis commands
    redis_commands = []

    # Convert JSON data to Redis commands
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                redis_commands.append(f'HSET {key} {sub_key} {sub_value}')
        else:
            redis_commands.append(f'SET {key} {value}')

    # Write Redis commands to the output file
    with open(output_file, 'w') as file:
        file.write('\n'.join(redis_commands))

# Example usage
json_string = '{"name": "John Doe", "age": 30, "address": {"city": "New York", "state": "NY"}}'
output_file = 'redis_commands.txt'

json_to_redis_commands(json_string, output_file)