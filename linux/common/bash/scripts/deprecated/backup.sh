#!/bin/bash
# need 3 arguments
# $1 path of the file to be backed up
# $2 destination directory
# $3 optional (remote) directory for saving a copy of the compressed file 
# i think you shoud not use zipped file, at least give options ...
local file="$2/$(basename $1)_$(date +%Y%m%d).7z"
7z a -t7z "$file" -mmt "$1"
local state=$?
if [ $state -eq 0 ]; then
    echo "\"$file\" has been compressed successfully!"
    if [ "$#" -eq 3 ]; then
        cp "$file" "$3"
        local state=$?
        if [ $state -eq 0 ]; then
            echo "\"$file\" has been copied to the directory \"$3\" successfully."
        fi
    fi
fi
