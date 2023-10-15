# Define Unicode code points 
party_popper_emoji="\U0001F389"   # 🎉
confetti_ball_emoji="\U0001F38A"  # 🎊

# Define bold text and reset color and formatting
bold='\033[1m'  # bold text
reset='\033[0m' # reset color and formatting

# Define color codes (non-bold)
blue='\033[0;34m'       # Blue
light_blue='\033[0;36m' # Light Blue
green='\033[0;32m'      # Green
red='\033[0;31m'        # Red
yellow='\033[0;33m'     # Yellow
purple='\033[0;35m'     # Purple

# Define bold color codes
blue_bold='\033[1;34m'       # Bold Blue
light_blue_bold='\033[1;36m' # Bold Light Blue
green_bold='\033[1;32m'      # Bold Green
red_bold='\033[1;31m'        # Bold Red
yellow_bold='\033[1;33m'     # Bold Yellow
purple_bold='\033[1;35m'     # Bold Purple


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

function get_last_commit_changes() {
    # Find the commit range of the last push
    local last_commit_hash=$(git log -n 1 --pretty=format:%H)
    local last_commit_short_hash=$(git rev-parse --short $last_commit_hash)
    local last_commit_time=$(git log -n 1 --format="%cd" --date=format:'%a %d %b %Y %H:%M:%S %z')

    # Show modified files in the last commit
    echo "Changes made in last commit: ${purple_bold}$last_commit_short_hash${reset} ($last_commit_time)"
    git diff --name-status $last_commit_hash^..$last_commit_hash | awk '
        BEGIN {
            color_A = "\033[0;32m";  # Green
            color_M = "\033[0;33m";  # Yellow
            color_D = "\033[0;31m";  # Red
            color_fbk = "\033[0;36m" # Light Blue; Fallback color
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

function git_add_commit_push() {
    local no_add=false
    local commit_message
    local command_running_message="${light_blue}Command running:${reset}"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --no-add)
                no_add=true
                shift
                ;;
            *)
                commit_message="$1"
                shift
                ;;
        esac
    done

    # Check if a commit message is provided
    if [[ -z $commit_message ]]; then
        echo "${red_bold}Error:${reset} Please provide a commit message."
        return 1
    fi

    # Add changes to staging area if --no-add flag is not given
    if [[ ! $no_add = true ]]; then
        echo "${command_running_message} git add ."
        git add .
    fi

    # Commit changes with the provided message
    echo "${command_running_message} git commit -m \"$commit_message\""
    git commit -m "$commit_message"

    # Push changes to the current branch
    branch=$(get_git_current_branch)
    echo "${command_running_message} git push origin $branch"
    git push origin $branch

    # Print success message
    echo ""

    server=$(get_git_remote_server)
    repo=$(get_git_remote_repository)

    echo "${green_bold}Hurray!${reset} ${party_popper_emoji}${confetti_ball_emoji}"
    echo "Successfully, pushed to remote server: ${yellow}$server${reset}"
    echo "                        remote repo:   ${yellow}$repo${reset}"
    echo "                        remote branch: ${yellow}$branch${reset}"

    # Print last commit changes
    echo ""
    get_last_commit_changes
}

alias gitit=git_add_commit_push 