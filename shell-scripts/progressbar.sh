# Function to draw the progress bar
draw_progress_bar() {
    local current_progress=$1
    local progress_bar_width=$2
    local percentage=$(( ($current_progress * 100) / $progress_bar_width ))
    local progress_bar=""

    # Create the progress bar
    for (( i = 0; i < $current_progress; i++ )); do
        progress_bar+="="
    done

    printf "[%-${progress_bar_width}s] %d%%" "$progress_bar" "$percentage"
}

default_total_iterations=100
total_iterations=${1-$default_total_iterations}

default_progress_bar_width=$(( $(tput cols) - 20 ))
progress_bar_width=${2-$default_progress_bar_width}

# Loop to simulate progress
for (( iteration = 0; iteration <= $progress_bar_total_width; iteration++ )); do
    draw_progress_bar $iteration $total_iterations $progress_bar_width
    sleep 0.05     # Simulate some work being done
    printf "\r"    # Move the cursor back to the beginning of the line
done

echo ""  # Move to the next line after the progress bar is complete