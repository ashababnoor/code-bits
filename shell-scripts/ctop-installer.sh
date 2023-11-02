#!/bin/bash

function install_ctop_on_linux_gnu() {
    sudo wget https://github.com/bcicen/ctop/releases/download/v0.7.7/ctop-0.7.7-linux-amd64 -O /usr/local/bin/ctop
    sudo chmod +x /usr/local/bin/ctop
}

function install_ctop_on_macos() {
    brew install ctop
}

function main() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        install_ctop_on_linux_gnu
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        install_ctop_on_macos
    else
        echo "OS type ${OSTYPE} is not supported."
    fi
}

main