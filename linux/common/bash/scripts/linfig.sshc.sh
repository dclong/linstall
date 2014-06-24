#!/usr/bin/env bash

function linfig.sshc(){
    echo "Configuring SSH ..."
    local desdir="$HOME/.ssh"
    local srcdir="$lommon/ssh"
    mkdir -p "$desdir" 
    # if running in Windows as a virtualization solutions
    if [[ "$(uname -a)" == CYGWIN_NT* ]]; then
        ln -sf "$srcdir/ssh_config" "$desdir/config"
        echo "\"$desdir/config\" -> \"$srcdir/ssh_config\"" 
        ln -sf "$srcdir/known_hosts" "$desdir"
        echo "\"$desdir/known_hosts\" -> \"$srcdir/known_hosts\"" 
        ln -sf "$srcdir/authorized_keys" "$desdir"
        echo "\"$desdir/authorized_keys\" -> \"$srcdir/authorized_keys\"" 
        echo "Done."
        return 0
    fi
    ln -Tsvf "$srcdir/ssh_config" "$desdir/config"
    ln -svf "$srcdir/known_hosts" "$desdir"
    ln -svf "$srcdir/authorized_keys" "$desdir"
    echo "Done."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.sshc $@
fi
