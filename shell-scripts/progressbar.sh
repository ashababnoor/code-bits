# Function to draw the progress bar
draw_progress_bar() {
    local current_iteration=$1
    local total_iterations=$2
    local width=$3
    local message=$4

    local percentage=$(( ($current_iteration * 100) / $total_iterations ))
    local progress_bar=""

    # Create the progress bar
    local current_progress=$(( ($width * $percentage) / 100 ))
    for (( i = 0; i < $current_progress; i++ )); do
        progress_bar+="="
    done

    if [ -z "$message" ]; then

    else
        message+=": "
    fi
    
    printf "${message}[%-${width}s] %d%%" "$progress_bar" "$percentage"
}

function progressbar() {
    default_total_iterations=100
    total_iterations=${1-$default_total_iterations}

    default_progress_bar_width=$(( $(tput cols) - 20 ))
    progress_bar_width=${2-$default_progress_bar_width}

    default_progress_bar_message=""
    progress_bar_message=${3-$default_progress_bar_message}

    # Loop to simulate progress
    for (( iteration = 0; iteration <= $total_iterations; iteration++ )); do
        draw_progress_bar $iteration $total_iterations $progress_bar_width $progress_bar_message

        sleep 0.05     # Simulate some work being done
        printf "\r"    # Move the cursor back to the beginning of the line
    done

    echo ""  # Move to the next line after the progress bar is complete
}


default_total_iterations=100
total_iterations=${1-$default_total_iterations}

default_progress_bar_width=$(( $(tput cols) - 20 ))
progress_bar_width=${2-$default_progress_bar_width}

default_progress_bar_message=""
progress_bar_message=${3-$default_progress_bar_message}

progressbar $total_iterations $progress_bar_width $progress_bar_message