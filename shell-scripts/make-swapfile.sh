#!/bin/bash

default_swapfile_size=1
swapfile_size=${1-$default_swapfile_size}

sudo fallocate -l "$swapfile_size"G /swapfile
sudo chmod 600 /swapfile
ls -hl /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
free -h