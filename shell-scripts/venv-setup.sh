ROOT_PROJECT_DIR=$(pwd)

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

    # pip install --upgrade pip

    log "Virtual environment activated successfully, Now installing requirements..."
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