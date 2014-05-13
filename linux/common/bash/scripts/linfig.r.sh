#!/bin/bash

function linfig.r.usage(){
    cat << EOF
Configure r.
Syntax: linfig.r
Make a symbolic link of \"$lommon/r/Renviron\" \ to \"$HOME/.Renviron\".
Make a symbolic link of \"$lommon/r/Rprofile.site\" \ to \"$HOME/.Rprofile\".
Make a symbolic link of \"$lommon/r/Makevars\" \ to \"$HOME/Makevars\".
Create $HOME/.R/library/ if not exists.
EOF
}
function linfig.r(){
    echo "Configuring R ..."
    # setup links
    if [[ "$(uname -a)" == CYGWIN_NT*GNU/Linux ]]; then
        ln -sf "$lommon/r/Renviron" "$HOME/.Renviron"
        echo "\"$HOME/.Renviron\" -> \"$lommon/r/Renviron\"" 
        ln -sf "$lommon/r/Rprofile.site" "$HOME/.Rprofile"
        echo "\"$lommon/r/Rprofile.site\" -> \"$HOME/.Rprofile\""
    fi
    ln -Tsvf "$lommon/r/Renviron" "$HOME/.Renviron"
    ln -Tsvf "$lommon/r/Rprofile.site" "$HOME/.Rprofile"
    #ln -svf $1/r/Rhistory $HOME/.Rhistory
    desdir="$HOME/.R" # must capitalize
    mkdir -p "$desdir"
    local state=$?
    if [ $state -eq 0 ]; then 
        # ln -Tsvf "$lommon/r/Makevars" "$desdir/Makevars"
        mkdir -p "$desdir/library"
    fi
    echo "Done."
    return 0
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.r $@
fi
