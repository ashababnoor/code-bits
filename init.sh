# Define Unicode code points 
party_popper_emoji="\U0001F389"   # 🎉
confetti_ball_emoji="\U0001F38A"  # 🎊

# Define ANSI escape codes
bold='\033[1m'
reset='\033[0m'

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

# Reset color and formatting
nc='\033[0m' # No Color


function get_last_commit_changes() {
    # Find the commit range of the last push
    local last_commit_hash=$(git log -n 1 --pretty=format:%H)
    local last_commit_short_hash=$(git rev-parse --short $last_commit_hash)
    local last_commit_time=$(git log -n 1 --format="%cd")

    # Show modified files in the last commit
    echo "Changes made in last commit: ${purple_bold}$last_commit_short_hash${nc} ($last_commit_time)"
    git diff --name-status $last_commit_hash^..$last_commit_hash | awk '
        BEGIN {
            color_A = "\033[1;32m";  # Green
            color_M = "\033[1;33m";  # Yellow
            color_D = "\033[1;31m";  # Red
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
    local command_running_string="${light_blue}Command running:${nc}"

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
        echo "${red_bold}Error:${nc} Please provide a commit message."
        return 1
    fi

    # Add changes to staging area if --no-add flag is not given
    if [[ ! $no_add = true ]]; then
        echo "${command_running_string} git add ."
        git add .
    fi

    # Commit changes with the provided message
    echo "${command_running_string} git commit -m \"$commit_message\""
    git commit -m "$commit_message"

    # Push changes to the current branch
    branch=$(git rev-parse --abbrev-ref HEAD)
    echo "${command_running_string} git push origin $branch"
    git push origin $branch

    # Print success message
    echo ""

    remote_url=$(git remote get-url origin)

    # Extract server and repo
    server=$(echo $remote_url | awk -F: '{print $1}' | awk -F@ '{print $2}')
    repo=$(echo $remote_url | awk -F: '{print $2}' | sed 's/.git$//')

    echo "${green_bold}Hurray!${nc} ${party_popper_emoji}${confetti_ball_emoji}"
    echo "Successfully, pushed to remote server: ${yellow}$server${nc}"
    echo "                        remote repo:   ${yellow}$repo${nc}"
    echo "                        remote branch: ${yellow}$branch${nc}"

    # Print last commit changes
    echo ""
    get_last_commit_changes
}

alias gitit=git_add_commit_push 