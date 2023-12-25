kill_process_on_port() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: kill_process_on_port <port_number>"
        return 1
    fi

    local port="$1"
    local process_ids=$(lsof -t -i :"$port")

    if [[ -z $process_ids ]]; then
        echo "No processes found running on port $port"
    else
        echo "Processes running on port $port:"
        echo "$process_ids"
        echo -en "Killing processes... "
        kill -9 $process_ids
        echo "Done"
    fi
}

alias kill-port=kill_process_on_port