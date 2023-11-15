#!/bin/bash

repository_name=""
gcp_project_id=""
gcp_project_zone=""
gcp_vm_name=""
gcp_vm_path="~/"

function create_repo_zip() {
    current_dir=$(pwd)
    echo "Currently inside ${current_dir}"

    cd //home/user/projects
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

    echo "Creating repo.zip file"
    zip -r $repository_name.zip repository
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

    echo "Sending $repository_name.zip to GCP VM $gcp_vm_name"
    gcloud compute scp --project=$gcp_project_id --zone=$gcp_project_zone $repository_name.zip $gcp_vm_name:$gcp_vm_path
    echo "File sent successfully"

    cd $current_dir
    echo "Moved back to $(pwd)"

    echo "Attempting to unzip $repository_name.zip in VM"
    gcloud compute ssh --project=$gcp_project_id --zone=$gcp_project_zone $gcp_vm_name --command="unzip -u $repository_name.zip" -- -t
    echo "Unzipping $repository_name.zip in VM completed successfully."
}

create_repo_zip
echo 
send_repo_zip_to_gcp_vm_and_unzip