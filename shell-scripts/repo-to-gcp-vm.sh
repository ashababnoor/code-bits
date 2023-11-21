#!/bin/bash

DEPLOYMENT=${1:-"dev"}

# Configure here as needed
case $DEPLOYMENT in
    prod)
        default_gcp_project_id=""
        default_gcp_project_zone=""
        default_gcp_vm_name=""
        default_gcp_vm_user=""
        default_gcp_vm_path=""
    ;;
    stage)
        default_gcp_project_id=""
        default_gcp_project_zone=""
        default_gcp_vm_name=""
        default_gcp_vm_user=""
        default_gcp_vm_path=""
    ;;
    dev | local)
        default_gcp_project_id=""
        default_gcp_project_zone=""
        default_gcp_vm_name=""
        default_gcp_vm_user=""
        default_gcp_vm_path=""
    ;;
    *)
        default_gcp_project_id=""
        default_gcp_project_zone=""
        default_gcp_vm_name=""
        default_gcp_vm_user=""
        default_gcp_vm_path=""
esac

repository_name=$(basename "$(pwd)")
gcp_project_id=${2-$default_gcp_project_id}
gcp_project_zone=${3-$default_gcp_project_zone}
gcp_vm_name=${4-$default_gcp_vm_name}
gcp_vm_user=${5-$default_gcp_vm_user}
gcp_vm_path=${6-$default_gcp_vm_path}

# List of directories and file extension to be deleted
directories_to_be_deleted=(".git" "venv" "__pycache__")
extensions_to_be_deleted=("tmp")


function gcloud_ssh_do() {
    local command=$1
    gcloud compute ssh --project=$gcp_project_id --zone=$gcp_project_zone $gcp_vm_user@$gcp_vm_name  --command="$command" -- -t
}

function create_repo_zip() {
    current_dir=$(pwd)
    echo "Currently inside ${current_dir}"

    cd ..
    echo "Moved to $(pwd)"

    echo -n "Creating tmp directory and copying contents of repository... "
    mkdir -p tmp
    cp -r $repository_name tmp
    echo "Done"

    cd tmp

    for dir in "${directories_to_be_deleted[@]}"; do
        echo "Deleting directory: $dir"
        find . -type d -name $dir -exec rm -rf {} \;
    done
    echo "Directories deleted successfully"

    for ext in "${extensions_to_be_deleted[@]}"; do
        echo "Deleting files with extension .$ext"
        find . -type f -name "*.$ext" -delete
    done
    echo "Files deleted successfully"

    echo "Creating $repository_name.zip file"
    zip -r $repository_name.zip $repository_name
    echo "Zip file created successfully"

    mv $repository_name.zip ..
    cd ..

    echo -n "Cleaning up tmp directory... "
    rm -rf tmp
    echo "Done"

    cd $current_dir
    echo "Moved back to $(pwd)"
}

function send_repo_zip_to_gcp_vm_and_unzip() {
    current_dir=$(pwd)
    echo "Currently inside ${current_dir}"

    cd ..
    echo "Moved to $(pwd)"

    echo "Sending $repository_name.zip to GCP VM $gcp_vm_name"
    gcloud compute scp --project=$gcp_project_id --zone=$gcp_project_zone $repository_name.zip $gcp_vm_user@$gcp_vm_name:$gcp_vm_path
    echo "File sent successfully"

    cd $current_dir
    echo "Moved back to $(pwd)"
    echo 

    gcloud_ssh_do "(command -v unzip &>/dev/null) || (sudo apt-get install unzip)"

    echo "Attempting to unzip $repository_name.zip in VM"
    gcloud_ssh_do "unzip -uo $repository_name.zip"
    echo "Unzipping $repository_name.zip in VM completed successfully."    
}

create_repo_zip
echo 
send_repo_zip_to_gcp_vm_and_unzip