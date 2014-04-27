#!/bin/bash

function linux.config.blog.usage(){
    cat << EOF 
Configure blog.
A symbolic link "$HOME/bin/epost" pointing to "$python_dir/blog/epost.py" is created.
EOF
}
function linux.config.blog(){
    echo "Configuring blog ..."
    local srcfile="$python_dir/blog/pelican/epost.py" 
    local desfile="$HOME/bin/epost"
    chmod +x "$srcfile"
    ln -Tsvf "$srcfile" "$desfile"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.config.blog $@
fi
