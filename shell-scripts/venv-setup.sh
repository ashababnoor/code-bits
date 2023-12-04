#!/bin/sh

SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
ROOT_PROJECT_DIR=$SCRIPT_DIR


function log() {
    echo -e "$(date +"%Y-%m-%d %H:%M:%S %z") ${blue}INFO${reset} $@"
}

function warn() {
    echo -e "$(date +"%Y-%m-%d %H:%M:%S %z") ${yellow}WARNING${reset} $@"
}

function error() {
    echo -e "$(date +"%Y-%m-%d %H:%M:%S %z") ${red}ERROR${reset} $@"
    exit 1
}

function create_python_venv() {
    if [ -d "$ROOT_PROJECT_DIR/venv" ]; then
        log "Directory $ROOT_PROJECT_DIR/venv exists."
    else
        log "Creating virtual environment for os:$OSTYPE"
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            (python -m venv venv) || (python3 -m venv venv)
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            python3 -m venv venv     # Mac OSX
        elif [[ "$OSTYPE" == "cygwin" ]]; then
            python -m venv venv      # POSIX compatibility layer and Linux environment emulation for Windows
        elif [[ "$OSTYPE" == "msys" ]]; then
            python -m venv venv      # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
        elif [[ "$OSTYPE" == "freebsd"* ]]; then
            python -m venv venv
		else
			log "Unknown os version, trying to install venv..."
            (python3 -m venv venv) || (python -m venv venv)      # Unknown
        fi
        log "Virtual environment created"
    fi
}

function activate_python_venv() {
    log "Activating virtual environment"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "cygwin"* ]]; then
        source venv/Scripts/activate
    elif [[ "$OSTYPE" == "msys"* ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    log "Virtual environment activated successfully"
}

function install_venv_requirements() {
    if [[ -f "requirements.txt" ]]; then
        pip install --upgrade pip
        pip install -r requirements.txt
        log "Requirements installed successfully"
    else
        warn "No 'requirements.txt' file found, So, not installing any dependencies"
    fi
}

function pip_install() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: pip_install <package_name>"
        return 1
    fi

    local package_name="$1"
    local installed_packages=$(pip freeze)

    if echo "$installed_packages" | grep -iq "^$package_name"; then
        echo "$package_name is already installed"
    else
        echo "Installing $package_name"
        pip install "$package_name"
    fi
}

function install_requirements_full() {
    if [[ -f "requirements.txt" ]]; then
        log "Installing requirements"
        
        pip install --upgrade pip
        pip install -r requirements.txt
        
        log "Requirements installed successfully"
    else
        warn "No 'requirements.txt' file found, So, not installing any dependencies"
    fi
}

function install_requirements_partial() {
    # Get the list of installed packages
    installed_packages=$(pip freeze)

    # Read requirements.txt line by line
    while IFS= read -r package
    do
    # Check if the package is installed
    if ! echo "$installed_packages" | grep -iq "^$package"; then
        # If not installed, install it
        echo "Installing $package"
        # pip install "$package"
    else
        echo "$package is already installed"
    fi
    done < requirements.txt
}