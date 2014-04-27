
function git.auto.usage(){
    echo "Auto add, commit and push changes in a GIT repository."
    echo "Syntax: git.auto rep_dir"
}
function git.auto(){
    if [ "$#" -ne 1 ]; then
        echo "Invalid number of arguments."
        return 1
    fi
    if [ $1 == "-h" ]; then
        git.auto.usage
        return 0
    fi
    cd "$1"
    git add .
    git commit -a -m ...
    git push
}
