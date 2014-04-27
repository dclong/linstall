#!/bin/bash

function linfig.icedove.usage(){
    cat << EOF
Configures Icedove.
Syntax: linfig.icedove
EOF
}

function linfig.icedove(){
    if [ "$1" == "-h" ]; then
        linfig.icedove.usage
        return 0
    fi
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            echo "Configuring Icedove ..."
            local desdir="$HOME/.icedove"
            local srcdir="$debian_dir/icedove"
            linfig.symlink "$srcdir" "$desdir"
            return 0;;
        *LMDE* )
            return 0;;
        *Ubuntu* )
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.icedove $@
fi
