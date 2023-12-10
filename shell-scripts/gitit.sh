#!/bin/sh

SCRIPT_DIR=$(cd "$(dirname -- "$0")"; pwd)
source $SCRIPT_DIR/colors.sh


command_running_message="${cyan}Command running:${reset}"

gitit_help_message="""\
Git add, commit and push in one command

${bold}Usage:${reset} 
    gitit [OPTIONS] <commit-message>

${bold}Options:${reset} 
    --no-add    Do not add changes to staging area
    --help      Display this help message

${bold}Example:${reset}
    gitit \"my awesome commit\"
"""

gitit_help_hint_message="Run 'gitit --help' to display help message"


function check_if_valid_git_repo(){
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [ -d "$dir/.git" ]; then
            echo "This is a Git repository."
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "This is not a Git repository."
    return 1
}

function get_git_remote_url(){
    remote_url=$(git remote get-url origin)
    echo $remote_url
}

function get_git_remote_server() {
    remote_url=$(get_git_remote_url)

    # Extract server
    remote_server=$(echo $remote_url | awk -F: '{print $1}' | awk -F@ '{print $2}')
    echo $remote_server
}

function get_git_remote_repository(){
    remote_url=$(get_git_remote_url)

    # Extract repository
    remote_repository=$(echo $remote_url | awk -F: '{print $2}' | sed 's/.git$//')
    echo $remote_repository
}

function get_git_current_branch(){
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    echo $current_branch
}

function print_last_commit_changes() {
    local highlight_color=${1-$light_sea_green_bold}

    # Find the commit range of the last push
    local last_commit_hash=$(git log -n 1 --pretty=format:%H)
    local last_commit_short_hash=$(git rev-parse --short $last_commit_hash)
    local last_commit_time=$(git log -n 1 --format="%cd" --date=format:'%a %d %b %Y %H:%M:%S %z')

    # Show modified files in the last commit
    echo "Changes made in last commit: ${highlight_color}$last_commit_short_hash${reset} ($last_commit_time)"
    git diff --name-status $last_commit_hash^..$last_commit_hash | awk '
        BEGIN {
            color_D = "\033[0;31m";  # Red
            color_A = "\033[0;32m";  # Green
            color_M = "\033[0;33m";  # Yellow
            color_fbk = "\033[0;36m" # Cyan; Fallback color
            reset = "\033[0m";       # Reset color
        }
        {
                 if ($1 == "A") { print color_A $1 reset "    " $2 }
            else if ($1 == "M") { print color_M $1 reset "    " $2 }
            else if ($1 == "D") { print color_D $1 reset "    " $2 }
            else { print color_fbk $1 reset "    " $2 }
        }
    '
}

function do_git_push() {
    local default_push_branch=$(get_git_current_branch)
    
    branch=${1:-$default_push_branch}
    echo "${command_running_message} git push origin $branch"
    git push origin "$branch"
}

function do_git_pull() {
    local default_pull_branch=$(get_git_current_branch)
    
    branch=${1:-$default_pull_branch}
    echo "${command_running_message} git pull origin $branch"
    git pull origin "$branch"
}

function print_success_message(){
    local server=$1
    local repo=$2
    local branch=$3
    local highlight_color=${4:-$dark_orange}

    echo "${green_bold}Hurray!${reset} ${party_popper_emoji}${confetti_ball_emoji}"
    echo "Successfully, pushed to remote server: ${highlight_color}$server${reset}"
    echo "                        remote repo:   ${highlight_color}$repo${reset}"
    echo "                        remote branch: ${highlight_color}$branch${reset}"
}

function git_add_commit_push() {
    local no_add=false
    local force_push=false
    local commit_message

    # Check if inside a git repo or not
    git_repo_validity_message=$(git rev-parse --is-inside-work-tree 2>&1)

    if [[ $git_repo_validity_message != "true" ]]; then
        echo -e "${red_bold}Fatal:${reset} $git_repo_validity_message"
        return 1
    fi

    # Check that we have at least one argument
    if [[ $# -lt 1 ]]; then
        echo -e $gitit_help_message
        return 1
    fi

    # Process the arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --no-add)
                no_add=true
                shift
                ;;
            --force)
                force_push=true
                shift
                ;;
            --help)
                echo -e $gitit_help_message
                return 0
            ;;
            *)
                commit_message="$1"
                shift
                ;;
        esac
    done

    # Check if a commit message is provided
    if [[ -z $commit_message ]]; then
        echo -e "${red_bold}Error:${reset} Please provide a commit message"
        echo ""
        echo $gitit_help_hint_message
        return 1
    fi

    # Add changes to staging area if --no-add flag is not given
    if [[ ! $no_add = true ]]; then
        echo -e "${command_running_message} git add ."
        git add .
    fi

    # Commit changes with the provided message
    echo "${command_running_message} git commit -m \"$commit_message\""
    git commit -m "$commit_message"

    # Check if commit was successful
    if [ $? -ne 0 ]; then
        echo "${red_bold}Error:${reset} Commit failed, not pushing changes"
        return 1
    fi

    # Push changes to the current branch
    branch=$(get_git_current_branch)

    if $force_push; then 
        do_git_push --force "$branch"
    else
        do_git_push "$branch"
    fi

    # Print success message
    echo ""

    server=$(get_git_remote_server)
    repo=$(get_git_remote_repository)

    print_success_message "$server" "$repo" "$branch"

    # Print last commit changes
    echo ""
    print_last_commit_changes
}

alias gitit=git_add_commit_push
alias gpush=do_git_push
alias gpull=do_git_pull