#!/bin/bash

# Function to draw the progress bar
draw_progress_bar() {
    local progress=$(( $1 * 1 ))  # Scale the progress to fit the bar width
    local bar=""

    # Create the progress bar
    for (( i = 0; i < $progress; i++ )); do
        bar+="="
    done

    printf "[%-50s] %d%%" "$bar" "$1"
}

# Loop to simulate progress
for (( i = 0; i <= 50; i++ )); do
    draw_progress_bar $i
    sleep 0.1  # Simulate some work being done
    printf "\r"  # Move the cursor back to the beginning of the line
done

echo ""  # Move to the next line after the progress bar is complete