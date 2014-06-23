#!/usr/bin/env bash

function merge.snippets.usage(){
    cat << EOF
Description: Merge snippets in the UltiSnips directory into the my_snippets directory.
Syntax: merge.snippets
EOF
}

function merge.snippets(){
    if [ "$1" == "-h" ]; then
        merge.snippets.usage
        return 0
    fi
    cd $HOME/.vim/UltiSnips
    for f in *.snippets; do
        if [[ -L $f ]]; then
            continue
        fi
        echo "Merging $f ..."
        cat $f >> ../my_snippets/$f
        mv $f $f.bak
    done
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    merge.snippets $@
fi
