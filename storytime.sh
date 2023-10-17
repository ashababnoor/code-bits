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

input_string="Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body."

for (( i=0; i<${#input_string}; i++ )); do
    echo -n "${input_string:$i:1}"
    sleep $(get_random_number $min_value $max_value)
done

echo