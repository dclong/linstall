#!/bin/bash

function linfig.sshc(){
    echo "Configuring SSH ..."
    local desdir="$HOME/.ssh"
    local srcdir="$lommon/ssh"
    mkdir -p "$desdir" 
    local state=$?
    if [ $state -eq 0 ]; then
        ln -Tsvf "$srcdir/ssh_config" "$desdir/config"
        ln -svf "$srcdir/known_hosts" "$desdir"
        ln -svf "$srcdir/authorized_keys" "$desdir"
    fi
    echo "Done."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.sshc $@
fi
