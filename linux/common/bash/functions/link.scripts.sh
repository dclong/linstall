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
    # MobaXterm - busybox: ln does not support -v option 
    if [[ "$(uname -a)" == CYGWIN_NT*GNU/Linux ]]; then
        for f in $(ls "$1"); do
            for fext in .sh .py; do
                if [[ "$f" == *$fext ]]; then
                    local srcfile="$1/$f"
                    chmod +x "$srcfile"
                    desfile="$desdir/$(basename "$f" $fext)"
                    ln -sf "$srcfile" "$desfile" 
                    echo "\"$desfile\" -> \"$srcfile\""
                fi
            done
        done
        return 0
    fi
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
    # link common scripts
    link.sidir "$bash_scripts_dir"
    # if running on Windows as virtualization solutin, 
    # then link scripts in the cygwin directory
    if [[ $(uname -a) == CYGWIN* ]]; then
        link.sidir "$cygwin_dir/bash/scripts"
        return
    fi
    # link Linux distribution-specific scripts
    case "$(lsb_release -d)" in
        *Debian* ) 
            link.sidir "$debian_dir/bash/scripts";;
        *Ubuntu* ) 
            link.sidir "$ubuntu_dir/bash/scripts";;
        *LMDE* )
            link.sidir "$lmde_dir/bash/scripts";;
        * ) 
            echo "Distribution not supported!";;
    esac
    link.sidir "$python_dir/bin"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    link.scripts $@
fi
