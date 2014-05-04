#!/bin/bash
# TODO: keep at most 3 backups
# remind yourself to close thunderbird, and force to quit, etc ...

function backtbp.usage(){
    cat << EOF
Description
Syntax: backtbp
EOF
}

function backtbp(){
    if [ "$1" == "-h" ]; then
        backtbp.usage
        return 0
    fi
    echo "Backing up Thunderbird profile ..."
    rsync -a $HOME/.thunderbird/ $HOME/backup/tbp_$(date +%Y%m%d)/    
    echo "Done."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    backtbp $@
fi
