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

multiply_until_integer 12.78