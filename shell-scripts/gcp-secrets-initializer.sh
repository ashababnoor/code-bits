#!/bin/bash

# Use this script to export GOOGLE_APPLICATION_CREDENTIALS path in your project
# Inside your project create a secrets directory that looks like this
# secrets
# ├── service_account.json
# └── gcp-secrets-initializer.sh


service_account_file_name=""

function set_google_app_cred() {
    local path=$1
    echo -n "Setting GOOGLE_APPLICATION_CREDENTIALS... "
    export GOOGLE_APPLICATION_CREDENTIALS=$path
    echo "Done"
}

function main() {
    local default_service_account_file_path="$(pwd)/secrets/$service_account_file_name"

    if [[ -f $default_service_account_file_path ]]; then
        echo "Service account json file found in secrets directory."
        
        local path=$default_service_account_file_path
        set_google_app_cred $path
    else
        echo "Service account json file NOT found in secrets directory."
        echo "GOOGLE_APPLICATION_CREDENTIALS is NOT set"
    fi
}

main
