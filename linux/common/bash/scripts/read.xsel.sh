#!/bin/bash
function read.xsel.usage(){
    echo "Play synthetised sound of selected text in X."
    echo "Syntax: read.xsel"
    echo "You have select text before you run this command."
}
function read.xsel(){
    if [ "$1" == "-h" ]; then
        read.xsel.usage
        return 0
    fi
    xsel | festival --tts --pipe
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    read.xsel $@
fi
