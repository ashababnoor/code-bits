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

progress_bar_total_width_default_value=$(( $(tput cols) - 10 ))
progress_bar_total_width=${1-$progress_bar_total_width_default_value}

# Loop to simulate progress
for (( i = 0; i <= $progress_bar_total_width; i++ )); do
    draw_progress_bar $i $progress_bar_total_width
    sleep 0.05     # Simulate some work being done
    printf "\r"    # Move the cursor back to the beginning of the line
done

echo ""  # Move to the next line after the progress bar is complete