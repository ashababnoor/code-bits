# Define Unicode code points
party_popper_emoji="\U0001F389"   # 🎉
confetti_ball_emoji="\U0001F38A"  # 🎊

# Define bold text and reset color and formatting
bold='\033[1m'  # bold text
reset='\033[0m' # reset color and formatting

# Define 3-bit non-bold color codes
black='\033[0;30m'         # Black
red='\033[0;31m'           # Red
green='\033[0;32m'         # Green
yellow='\033[0;33m'        # Yellow
blue='\033[0;34m'          # Blue
magenta='\033[0;35m'       # Magenta
cyan='\033[0;36m'          # Cyan
white='\033[0;37m'         # White

# Define 3-bit background codes
black_bg='\033[0;40m'      # Black Background
red_bg='\033[0;41m'        # Red Background
green_bg='\033[0;42m'      # Green Background
yellow_bg='\033[0;43m'     # Yellow Background
blue_bg='\033[0;44m'       # Blue Background
magenta_bg='\033[0;45m'    # Magenta Background
cyan_bg='\033[0;46m'       # Cyan Background
white_bg='\033[0;47m'      # White Background

# Define 3-bit bold color color codes
black_bold='\033[1;30m'    # Bold Black
red_bold='\033[1;31m'      # Bold Red
green_bold='\033[1;32m'    # Bold Green
yellow_bold='\033[1;33m'   # Bold Yellow
blue_bold='\033[1;34m'     # Bold Blue
magenta_bold='\033[1;35m'  # Bold Magenta
cyan_bold='\033[1;36m'     # Bold Cyan
white_bold='\033[1;37m'    # Bold White

# Define 8-bit color non-bold codes
orage='\033[38;5;214m'          # Orange
dark_orange='\033[38;5;208m'    # Dark Orange
orange_red='\033[38;5;202m'     # Orange Red
light_sea_green='\033[38;5;37m' # Light Sea Green
dodger_blue='\033[38;5;33m'     # Dodger Blue

# Define 8-bit color bold codes
orage_bold='\033[1;38;5;214m'          # Bold Orange
dark_orange_bold='\033[1;38;5;208m'    # Bold Dark Orange
orange_red_bold='\033[1;38;5;202m'     # Bold Orange Red
light_sea_green_bold='\033[1;38;5;37m' # Bold Light Sea Green
dodger_blue_bold='\033[1;38;5;33m'     # Bold Dodger Blue

# Read more: 
#   1) https://en.wikipedia.org/wiki/ANSI_escape_code
#   2) https://www.ditig.com/256-colors-cheat-sheet 


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
    local commit_message
    local command_running_message="${cyan}Command running:${reset}"

    # Check if inside a git repo or not
    git_repo_validity_message=$(check_if_valid_git_repo)

    if [[ $git_repo_validity_message == "This is not a Git repository." ]]; then
        echo "${red_bold}Fatal Error:${reset} Please provide a commit message."
        return 1
    fi

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

    print_success_message $server $repo $branch

    # Print last commit changes
    echo ""
    print_last_commit_changes
}

alias gitit=git_add_commit_push 