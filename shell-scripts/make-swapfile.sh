#!/bin/bash

default_swapfile_size=1
swapfile_size=${1-$default_swapfile_size}

function make_swapfile() {
    local swapfile_size=$1
    
    echo "Attempting to create swap file..."

    echo "Allocating ${swapfile_size}G memory for the swap file"
    sudo fallocate -l "$swapfile_size"G /swapfile

    sudo chmod 600 /swapfile
    ls -hl /swapfile
    sudo mkswap /swapfile

    echo "Swapfile has been created. Activating swapfile"
    sudo swapon /swapfile

    echo "Running 'swapon --show' to confirm the swap space is enabled"
    sudo swapon --show

    echo "Running 'free -h' to confirm the amount of swap space available"
    free -h
}

function make_swapfile_with_user_caution() {
    local swapfile_size=$1
    echo "This script was tested on Ubuntu operating system. Do you wish to proceed? (y/[n])"
    read -r answer

    if [[ "$answer" == "y" ]]; then
        echo "Proceeding..."
        make_swapfile $swapfile_size
    elif [ "$answer" == "" || "$answer" == "n" ]; then
        echo "Exiting."
        exit 1  # Exit with status code 1
    else
        echo "Invalid input. Please enter 'y' or 'n'."
        echo "Exiting."
        exit 1  # Exit with status code 1
    fi
}

function main() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            source /etc/os-release
            if [ "$ID" == "ubuntu" ]; then
                echo "The operating system is Ubuntu."
                make_swapfile $swapfile_size
            else
                echo "The operating system is not Ubuntu."
                make_swapfile_with_user_caution $swapfile_size
            fi
        else
            echo "Unable to determine the operating system."
            make_swapfile_with_user_caution $swapfile_size
        fi

    else
        echo "OS type ${OSTYPE} is not supported."
        echo "Run this script in a linux-gnu machine to make swapfile."
    fi
}

main