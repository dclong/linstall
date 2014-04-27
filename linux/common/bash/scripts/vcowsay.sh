#!/bin/bash
function vcowsay.usage(){
    echo "Display a cow saying words and play synthertized sound of the words."
    echo "Syntax: vcowsay words"
} 
function vcowsay(){
    if [ "$1" == "-h" ]; then
        vcowsay.usage
        return 0
    fi
    rcowsay "$1"
    echo "$1" | festival --tts
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    vcowsay $@
fi
