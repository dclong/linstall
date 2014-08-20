#!/usr/bin/env bash

function git.x.usage(){
    cat << EOF
Fix permission changes of files (due to OS systems).
Syntax: git.x
EOF
}

function git.x(){
    if [ "$1" == "-h" ]; then
        git.x.usage
        return 0
    fi
    local folder=.
    if [[ "$1" != "" ]]; then
        folder="$1"
    fi
    cd "$folder"
    git diff --summary | grep 'mode change 100755 => 100644' | cut -d ' ' -f7- | xargs -d '\n' chmod +x
    git diff --summary | grep 'mode change 100644 => 100755' | cut -d ' ' -f7- | xargs -d '\n' chmod -x
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    git.x $@
fi
