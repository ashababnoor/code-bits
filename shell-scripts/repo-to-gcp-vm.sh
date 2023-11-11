#!/bin/bash

function create_repo_zip() {
    current_dir=$(pwd)
    echo "Currently inside ${current_dir}"

    cd //home/user/projects
    echo "Moved to $(pwd)"

    echo -n "Creating tmp directory and copying contents of repository... "
    mkdir -p tmp
    cp -r repository tmp
    echo "Done"

    cd tmp

    echo "Deleting directories: .git, venv... "
    find . -type d -name ".git" -exec rm -rf {} \;
    find . -type d -name "venv" -exec rm -rf {} \;
    echo "Directories deleted successfully"

    echo -n "Deleting files: *.csv... "
    find . -type f -name "*.csv" -delete
    echo "Done"

    echo "Creating repo.zip file"
    zip -r repo.zip repository
    echo "Zip file created successfully"

    mv repo.zip ..
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

    cd //home/user/projects
    echo "Moved to $(pwd)"

    echo "Sending repo.zip to GCP VM repo-vm"
    gcloud compute scp --project="gcp-project" --zone="us-central1-a" repo.zip repo-vm:~/
    echo "File sent successfully"

    cd $current_dir
    echo "Moved back to $(pwd)"

    echo "Attempting to unzip repo.zip in VM"
    gcloud compute ssh --project="gcp-project" --zone="us-central1-a" repo-vm --command="unzip -u repo.zip" -- -t
    echo "Unzipping repo.zip in VM completed successfully."
}

create_repo_zip
echo 
send_repo_zip_to_gcp_vm_and_unzip