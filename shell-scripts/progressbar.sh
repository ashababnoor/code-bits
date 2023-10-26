# Function to draw the progress bar
draw_progress_bar() {
    local current_progress=$(( $1 * 1 ))
    local total_width=$2
    local bar=""

    # Create the progress bar
    for (( i = 0; i < $current_progress; i++ )); do
        bar+="="
    done

    printf "[%-${total_width}s] %d%%" "$bar" "$current_progress"
}

progress_bar_total_width_default_value=50
progress_bar_total_width=${1-$progress_bar_total_width_default_value}

# Loop to simulate progress
for (( i = 0; i <= $progress_bar_total_width; i++ )); do
    draw_progress_bar $i $progress_bar_total_width
    sleep 0.05     # Simulate some work being done
    printf "\r"    # Move the cursor back to the beginning of the line
done

echo ""  # Move to the next line after the progress bar is complete