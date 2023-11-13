def redis_commands_to_resp(input_file, output_file):
    with open(input_file, 'r') as file:
        redis_commands = file.read().splitlines()

    resp_commands = []

    for command in redis_commands:
        parts = command.split()
        command_type = parts[0].encode('utf-8')
        arguments = [arg.encode('utf-8') for arg in parts[1:]]
        resp_command = b'*' + str(len(arguments) + 1).encode('utf-8') + b'\r\n' + b'$' + str(len(command_type)).encode('utf-8') + b'\r\n' + command_type + b'\r\n'

        for arg in arguments:
            resp_command += b'$' + str(len(arg)).encode('utf-8') + b'\r\n' + arg + b'\r\n'

        resp_commands.append(resp_command)

    with open(output_file, 'wb') as file:
        for resp_command in resp_commands:
            file.write(resp_command)


if __name__ == "__main__":
    # Example usage
    input_file = 'redis_commands.txt'
    output_file = 'resp_commands.txt'

    redis_commands_to_resp(input_file, output_file)