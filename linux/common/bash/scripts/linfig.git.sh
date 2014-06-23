#!/usr/bin/env bash

function linfig.git.usage(){
    cat << EOF
Configure git.
Syntax: linfig.git
Make a symbolic link of \"$lommon/git/gitconfig\" to \"$HOME/.gitconfig\".
Make a symbolic link of \"$lommon/git/gitignore\" to \"$HOME/.gitignore\".
EOF
}
function linfig.git(){
    echo "Configuring Git ..."
    # configuration
    if [[ "$(uname -a)" == CYGWIN_NT* ]]; then
        ln -sf "$lommon/git/gitconfig" "$HOME/.gitconfig"
        echo "\"$HOME/.gitconfig\" -> \"$lommon/git/gitconfig\""
        ln -sf "$lommon/git/gitignore" "$HOME/.gitignore"
        echo "\"$HOME/.gitignore\" -> \"$lommon/git/gitignore\""
        return 0
    fi
    ln -Tsvf "$lommon/git/gitconfig" "$HOME/.gitconfig"
    ln -Tsvf "$lommon/git/gitignore" "$HOME/.gitignore"
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.git $@
fi
