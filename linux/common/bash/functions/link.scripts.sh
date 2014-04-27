#!/bin/sh

function link.scripts.usage(){
    cat << EOF
Link my bash functions as scripts. 
Syntax: linux.config.scripts
EOF
}
function link.sidir(){
    local desdir="$HOME/bin"
    mkdir -p "$desdir"
    for f in $(ls "$1"); do
        for fext in .sh .py; do
            if [[ "$f" == *$fext ]]; then
                local srcfile="$1/$f"
                chmod +x "$srcfile"
                desfile="$desdir/$(basename "$f" $fext)"
                ln -svf "$srcfile" "$desfile" 
            fi
        done
    done
}
function link.scripts(){
    link.sidir "$bash_scripts_dir"
    case "$(uname -v)" in
        *Debian* ) link.sidir "$debian_dir/bash/scripts";;
        *Ubuntu* ) link.sidir "$ubuntu_dir/bash/scripts";;
        * ) ;;
    esac
    link.sidir "$python_dir/bin"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    link.scripts $@
fi
