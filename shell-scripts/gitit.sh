#!/bin/sh

SCRIPT_DIR=$(cd "$(dirname -- "$0")"; pwd)
source $SCRIPT_DIR/colors.sh


gitit_name_ascii_art="""${style_bold}
          _   _     _   _   
         (_) | |   (_) | |  
   __ _   _  | |_   _  | |_ 
  / _  | | | | __| | | | __|
 | (_| | | | | |_  | | | |_ 
  \__, | |_|  \__| |_|  \__|
   __/ |                    
  |___/                     
${style_reset}"""

gitit_help_message="""\
$gitit_name_ascii_art

Git add, commit and push in one command

${style_bold}Usage${style_reset} 
    gitit [OPTIONS] <commit-message>

${style_bold}Options${style_reset} 
    -s, --skip-stage  Do not add changes to staging area
    -f, --force       Force push the branch to remote
    -h, --help        Display this help message

${style_bold}Example${style_reset}
    gitit \"my awesome commit\"
    gitit --skip-stage \"commit without adding changes to stage\"
    gitit --force \"force push commit\"
"""

gitit_help_hint_message="Run 'gitit --help' to display help message"


command_running_message="${color_cyan}Running command:${style_reset}"
warning_prefix="${color_yellow_bold}Warning:${style_reset}"
error_prefix="${color_red_bold}Error:${style_reset}"
fatal_prefix="${color_red_bold}Fatal:${style_reset}"

function execute() {
    if [ $# -eq 0 ]; then
        echo -e "${fatal_prefix} No command provided"
        return 1
    fi

    local command=$1
    shift

    if ! command -v "$command" &> /dev/null; then
        echo -e "${fatal_prefix} Command '$command' not found"
        return 1
    fi

    echo -e "$command_running_message $command $@"
    $command "$@"
}


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
    local highlight_color=${1-$color_light_sea_green_bold}

    # Find the commit range of the last push
    local last_commit_hash=$(git log -n 1 --pretty=format:%H)
    local last_commit_short_hash=$(git rev-parse --short $last_commit_hash)
    local last_commit_time=$(git log -n 1 --format="%cd" --date=format:'%a %d %b %Y %H:%M:%S %z')

    # Show modified files in the last commit
    echo "Changes made in last commit: ${highlight_color}$last_commit_short_hash${style_reset} ($last_commit_time)"
    git diff --name-status $last_commit_hash^..$last_commit_hash | awk '
        BEGIN {
            color_D = "\033[0;31m";  # Red
            color_A = "\033[0;32m";  # Green
            color_M = "\033[0;33m";  # Yellow
            color_fbk = "\033[0;36m" # Cyan; Fallback color
            style_reset = "\033[0m"; # Reset color
        }
        {
                 if ($1 == "A") { print color_A $1 style_reset "    " $2 }
            else if ($1 == "M") { print color_M $1 style_reset "    " $2 }
            else if ($1 == "D") { print color_D $1 style_reset "    " $2 }
            else { print color_fbk $1 style_reset "    " $2 }
        }
    '
}

function do_git_push() {
    local default_push_branch=$(get_git_current_branch)
    local force_push=false
    local branch=""
    local print_success_message=false

    # Check if there is anything to push
    local git_status=$(git status --porcelain)

    # Check if there are any changes staged for commit
    # 0 = nothing staged for commit, 1 = changes staged for commit
    git diff --cached --quiet
    local changes_staged=$?

    # Check if there were any commits since the last push
    # Returns count of commits
    local commits_since_last_push=$(git rev-list --count @{u}..)

    if [[ $changes_staged -eq 0 ]]; then
        echo "No changes staged to be committed"
    fi
    
    if [[ $commits_since_last_push -eq 0 ]]; then
        echo "No changes committed to be pushed"
    fi

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force)
                force_push=true
                shift
                ;;
            --print-success)
                print_success_message=true
                shift
                ;;
            *)
                branch="$1"
                shift
                ;;
        esac
    done
    
    local branch=${branch:-$default_push_branch}
    
    if [[ $force_push = true ]]; then
        execute git push --force origin "$branch"
    else
        execute git push origin "$branch"
    fi

    if [[ $print_success_message = true && $commits_since_last_push -gt 0 ]]; then
        local server=$(get_git_remote_server)
        local repo=$(get_git_remote_repository)

        # Print push success message
        echo ""
        print_push_success_message "$server" "$repo" "$branch"
    fi
}

function do_git_pull() {
    local default_pull_branch=$(get_git_current_branch)
    
    local branch=${1:-$default_pull_branch}
    execute git pull origin "$branch"
}

function print_commit_success_message() {
    local branch=$1
    local highlight_color=${2:-$color_dark_orange}

    echo "${color_green_bold}Hurray!${style_reset} ${emoji_party_popper}${emoji_confetti_ball}"
    echo "Successfully, committed changes in branch: ${highlight_color}$branch${style_reset}"
}

function print_push_success_message() {
    local server=$1
    local repo=$2
    local branch=$3
    local highlight_color=${4:-$color_dark_orange}

    echo "${color_green_bold}Hurray!${style_reset} ${emoji_party_popper}${emoji_confetti_ball}"
    echo "Successfully, pushed to remote server: ${highlight_color}$server${style_reset}"
    echo "                        remote repo:   ${highlight_color}$repo${style_reset}"
    echo "                        remote branch: ${highlight_color}$branch${style_reset}"
}

function git_add_commit_push() {
    local skip_stage=false
    local force_push=false
    local commit_message=""
    local branch=""
    local server=""
    local repo=""
    local git_repo_validity_message=""

    # Check if inside a git repo or not
    git_repo_validity_message=$(git rev-parse --is-inside-work-tree 2>&1)

    if [[ $git_repo_validity_message != "true" ]]; then
        echo -e "${fatal_prefix} $git_repo_validity_message"
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
            --skip-stage|-s)
                skip_stage=true
                shift
                ;;
            --force|-f)
                force_push=true
                shift
                ;;
            --help|-h)
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
        echo -e "${error_prefix} Please provide a commit message"
        echo ""
        echo $gitit_help_hint_message
        return 1
    fi

    # Add changes to staging area if --no-add flag is not given
    if [[ ! $skip_stage = true ]]; then
        execute git add .
    fi

    # Commit changes with the provided message
    execute git commit -m "$commit_message"

    # Check if commit was successful
    if [ $? -ne 0 ]; then
        echo "${error_prefix} Commit failed, not pushing changes"
        return 1
    fi

    # Push changes to the current branch
    branch=$(get_git_current_branch)

    # Check if any remote exists
    if [[ -z $(git remote) ]]; then
        echo -e "${warning_prefix} No remote repository found. Skipping git push"

        # Print commit success message
        echo ""
        print_commit_success_message "$branch"
    else
        if $force_push; then 
            do_git_push --force "$branch"
        else
            do_git_push "$branch"
        fi

        server=$(get_git_remote_server)
        repo=$(get_git_remote_repository)

        # Print push success message
        echo ""
        print_push_success_message "$server" "$repo" "$branch"
    fi

    # Print last commit changes
    echo ""
    print_last_commit_changes
}

alias gitit=git_add_commit_push
alias gpush="do_git_push --print-success"
alias gpull=do_git_pull


# TODO: New features to be added 

# --amend: 
#     This option could be used to amend the last commit. 
#     This is useful if you made a mistake in your last 
#     commit message or forgot to add some changes.

# --branch: 
#     This option could allow the user to specify a branch 
#     to push to, instead of always pushing to the current 
#     branch.

# --remote: 
#     This option could allow the user to specify a remote 
#     to push to, instead of always pushing to the default 
#     remote.

# --all: 
#     This option could add all changes (including untracked 
#     files) to the staging area, instead of only changes to 
#     already tracked files.