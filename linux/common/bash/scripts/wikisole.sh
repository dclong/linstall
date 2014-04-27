#!/bin/bash
function wikisole.usage(){
    echo "Get Wikepedia definition of words."
    echo "Syntax: wikisole word"
    echo "where word is the word/phrase that you want check on Wikipedia."  
}
function wikisole(){
    if [ "$1" == "-h" ]; then
        wikisole.usage
        return 0
    fi
    if [ "$#" -eq 1 ]; then
        dig +short txt "${1}".wp.dg.cx
        return 0
    fi
    echo "Only 1 argument is supported currently."
    return 1
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    wikisole $@
fi
