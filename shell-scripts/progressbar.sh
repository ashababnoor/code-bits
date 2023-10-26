# Function to draw the progress bar
draw_progress_bar() {
    local current_iteration=$1
    local total_iterations=$2
    local progress_bar_width=$3
    local progress_bar_message=$4

    local progress_bar_percentage=$(( ($current_iteration * 100) / $total_iterations ))
    local progress_bar=""

    # Create the progress bar
    local current_progress=$(( ($progress_bar_width * $progress_bar_percentage) / 100 ))
    for (( i = 0; i < $current_progress; i++ )); do
        progress_bar+="="
    done

    if [ -z "$progress_bar_message" ]; then

    else
        progress_bar_message+=": "
    fi
    
    printf "${progress_bar_message}[%-${progress_bar_width}s] %d%%" "$progress_bar" "$progress_bar_percentage"
}

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