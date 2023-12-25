kill_process_on_port() {
    if [[ $# -ne 1 ]]; then
        echo "Usage:"
        echo "    kill-port <PORT_NUM>"
        echo "    kill_process_on_port <PORT_NUM>"
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
        kill -15 "$process_ids"
        sleep 2
        kill -9 "$process_ids" 2>/dev/null
        echo "Done"
    fi
}

alias kill-port=kill_process_on_port