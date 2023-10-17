min_value=0.1
max_value=0.25

function multiply_until_integer() {
    local value=$1
    local multiply_by=1
    local multiplications=0

    while ! [[ $value -eq ${value%.*} ]]; do
        value=$(bc <<< "$value * 10")
        multiply_by=$(bc <<< "$multiply_by * 10")
        ((multiplications++))
    done

    # Create an array with two elements
    local result=("$value" "$multiply_by" "$multiplications")

    # Return the array
    echo "${result[@]}"
}

function get_random_number() {
    local min_value=$1
    local max_value=$2

    local min_max_val_difference=$(( $max_value - $min_value ))
    local result_array=($(multiply_until_integer $min_max_val_difference))
    
    local lower_limit=1
    local upper_limit=${$(bc <<< "${result_array[1]} * 10")%.*}
    local multiplied_by=$(bc <<< "${result_array[2]} * 10" )
    local multiplications=${result_array[3]}

    # Get a random integer using shuf 
    local random_int=$(shuf -i $lower_limit-$upper_limit -n 1)

    # Calculate random number within specified range
    local random_number=$(bc <<< "scale=$(( multiplications + 1 )); ($random_int / $multiplied_by) + $min_value")
    
    echo $random_number
}

# if [ $# -eq 0 ]; then
#     echo "Error: No input string provided."
#     exit 1
# fi

# input_string=$1

input_string="Octopuses have three hearts."
echo

for (( i=0; i<${#input_string}; i++ )); do
    sleeptime=$(get_random_number $min_value $max_value)
    echo "\033[A$sleeptime"
    echo -n "${input_string:0:$i}"
    printf "\r"
    sleep 0.05 # $sleeptime
done

echo

text="There was once a hare who was friends with a tortoise. One day, he challenged the tortoise to a race. Seeing how slow the tortoise was going, the hare thought he’ll win this easily. So he took a nap while the tortoise kept on going. When the hare woke up, he saw that the tortoise was already at the finish line. Much to his chagrin, the tortoise won the race while he was busy sleeping."

# Function to split the text into chunks
# function split_text() {
#     local str="$1"
#     local len=${#str}
#     for ((i = 0; i < len; i += chunk_size)); do
#         echo "${str:$i:$chunk_size}"
#     done
# }

# # # Split the text into chunks and print
# split_text "$text" | while IFS= read -r chunk; do
#     for ((i = 0; i < ${#chunk}; i++)); do
#         echo -n "${chunk:$i:1}"
#         sleep $delay
#     done
#     echo  # Add a newline after each chunk
# done

# Print some lines
# echo "Line 1"
# echo "Line 2"
# echo "Line 3"

# # Move the cursor up one line
# echo -e "\033[A"
# echo -e "\033[AThis is on the line above"

# # Print something on the line above
# echo "This is on the line above"

#!/bin/bash

function print_chunks() {
    if [ $# -eq 0 ]; then
        echo "Error: No input string provided."
        return 1
    fi

    local input_string=$1
    local chunk_size=${2:-10}  # Default chunk size is 10

    local len=${#input_string}
    local i=0

    while [ $i -lt $len ]; do
        local chunk="${input_string:$i:$chunk_size}"
        for (( j=0; j<${#chunk}; j++ )); do
            echo -n "${chunk:$j:1}"
            sleep 0.05  # Optional: Add a small delay between characters
        done
        echo ""  # Print a newline after each chunk
        i=$((i + chunk_size))
    done
}

# print_chunks $text