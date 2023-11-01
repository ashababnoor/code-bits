#!/bin/bash

default_swapfile_size=1
swapfile_size=${1-$default_swapfile_size}

function make_swapfile() {
    local swapfile_size=$1

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

function main() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        make_swapfile $swapfile_size
    else
        echo "OS type ${OSTYPE} is not supported."
        echo "Run this script in a linux-gnu machine to make swapfile."
    fi
}

main