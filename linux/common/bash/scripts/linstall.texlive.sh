#!/usr/bin/env bash

function linstall.texlive.usage(){
    cat << EOF
Description
Syntax: linstall.texlive
EOF
}

function linstall.texlive(){
    if [ "$1" == "-h" ]; then
        linstall.texlive.usage
        return 0
    fi
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* | *LMDE* | *Ubuntu* )
            # install minimum texlive and some extra fonts
            wajig install texlive texlive-latex-extra texlive-fonts-extra dvipng texstudio
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.texlive $@
fi
