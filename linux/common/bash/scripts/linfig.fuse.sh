#!/bin/bash
function linfig.fuse.usage(){
    cat << EOF
Configures fuse. The specified user or the current user is added to the fuse group.
Syntax: linfig.fuse
EOF
}
function linfig.fuse(){
    user=$(whoami)
    if [ "$#" -gt 0 ]; then
        user=$@
    fi
    sudo adduser $user fuse
    newgrp fuse
    echo "Logout and then login or reboot if group permission is not in effect."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.fuse $@
fi

