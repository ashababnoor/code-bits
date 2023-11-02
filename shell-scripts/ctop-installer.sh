#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
    sudo chmod +x /usr/local/bin/ctop

elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ctop

else
    echo "OS type ${OSTYPE} is not supported."

fi