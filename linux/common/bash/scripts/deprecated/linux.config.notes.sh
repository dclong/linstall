#!/bin/bash

function linux.config.notes.usage(){
    cat << EOF
Configures notes.
A symbolic link "$HOME/bin/notes" pointing to "$python_dir/notes/mongodb/notes.py" is created. 
EOF
}
function linux.config.notes(){
    echo "Configuring notes ..."
    local srcfile="$python_dir/notes/mongodb/notes.py" 
    local desfile="$HOME/bin/notes"
    chmod +x "$srcfile"
    ln -Tsvf "$srcfile" "$desfile"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.config.notes $@
fi
