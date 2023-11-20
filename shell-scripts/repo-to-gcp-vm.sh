#!/bin/bash

# Add values here as needed
default_gcp_project_id=""    # Google cloud platform porject ID
default_gcp_project_zone=""  # Google cloud platform porject zone
default_gcp_vm_name=""       # Google cloud platform virtual machine name
default_gcp_vm_user="$USER"  # Google cloud platform virtual machine user
default_gcp_vm_path="~/"     # Google cloud platform virtual machine path where contents will be sent

repository_name=$(basename "$(pwd)")
gcp_project_id=${1-$default_gcp_project_id}
gcp_project_zone=${2-$default_gcp_project_zone}
gcp_vm_name=${3-$default_gcp_vm_name}
gcp_vm_user=${4-$default_gcp_vm_user}
gcp_vm_path=${5-$default_gcp_vm_path}


alias gssh="gcloud compute ssh --project=$gcp_project_id --zone=$gcp_project_zone $gcp_vm_user@$gcp_vm_name"

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

    echo "Deleting directories: .git, venv... "
    find . -type d -name ".git" -exec rm -rf {} \;
    find . -type d -name "venv" -exec rm -rf {} \;
    echo "Directories deleted successfully"

    echo -n "Deleting files: *.csv... "
    find . -type f -name "*.csv" -delete
    echo "Done"

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

    gssh --command="(command -v unzip &>/dev/null) || (sudo apt-get install unzip)" -- -t

    echo "Attempting to unzip $repository_name.zip in VM"
    gssh --command="unzip -uo $repository_name.zip" -- -t
    echo "Unzipping $repository_name.zip in VM completed successfully."    
}

create_repo_zip
echo 
send_repo_zip_to_gcp_vm_and_unzip
unalias gssh