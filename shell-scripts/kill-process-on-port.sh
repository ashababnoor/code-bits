kill_process_on_port() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: kill_process_on_port <port_number>"
        return 1
    fi

    local port="$1"
    local pid_list=$(lsof -t -i :"$port")

    if [[ -z $pid_list ]]; then
        echo "No processes found running on port $port"
    else
        echo "Processes running on port $port:"
        echo "$pid_list"
        echo -en "Killing processes... "
        kill -9 $pid_list
        echo "Done"
    fi
}

alias kill-port=kill_process_on_port