#!/usr/bin/env bash

function linfig.nomachine.usage(){
    cat << EOF
Make symbolic link of "$config_root_dir/common/nomachine" to "$HOME/.NoMachine". 
EOF
}
function linfig.nomachine(){
    if [[ "$1" == "-h" ]]; then
        linfig.nomachine.usage
        return 0
    fi
    echo "Configuring NoMachine ..."
    local srcfile="$config_root_dir/common/nomachine"
    local desfile="$HOME/.NoMachine"
    ln -Tsvf $srcfile $desfile
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.nomachine $@
fi
