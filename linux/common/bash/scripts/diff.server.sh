#!/bin/bash

function diff.server.usage(){
    cat << EOF
Compare a remote file with a local file for difference using SSH.
Syntax: diff.server server port local_file [remote_file]
EOF
}

function diff.server(){
    if [ "$1" == "-h" ]; then
        diff.server.usage
        return 0
    fi
    if [[ "$#" -eq 4 ]]; then
        local file_l="$(realpath "$3")"
        local file_r="$(ssh -p "$2" "$1" realpath "$4")"
        local hash_r="$(ssh -p "$2" "$1" md5sum "$file_r" | cut -d " " -f 1)"
        local hash_l="$(md5sum "$file_l" | cut -d " " -f 1)"
        if [[ "$hash_r" == "$hash_l" ]]; then
            echo "No difference."
            return 0
        else
            echo "There's difference."
        fi
        local type_r="$(ssh -p "$2" "$1" file -ib "$file_r")"
        local type_l="$(file -ib "$file_l")"
        if [[ "$type_r" == text/* ]] && [[ "$type_l" == text/* ]]; then
            ssh -p "$2" "$1" cat "$file_r" | diff "$file_l" -
        fi
    elif [[ "$#" -eq 3 ]]; then
        local file="$(realpath "$3")"
        diff.server "$1" "$2" "$file" "$(realpath "$file")" 
    else
        echo "3 or 4 arguments are required."
        return 1
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    diff.server $@
fi
