#!/bin/bash

default_swapfile_size=1
swapfile_size=${1-$default_swapfile_size}

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