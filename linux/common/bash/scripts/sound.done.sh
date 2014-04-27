#!/bin/bash
function sound.done.usage(){
    echo "Play the sound \"Job is done.\" repeatedly."
    echo "Syntax: sound.done n i"
    echo "where n is the number of times to repeat the sound, \
        and i is the time interval (seconds) between repeats."
}
function sound.done(){
    if [ "$1" == "-h" ]; then
        sound.done.usage
        return 0
    fi
    for i in {1..${1}}; do
        echo "Job is done." | espeak --stdin
        sleep ${2}s
    done
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    sound.done $@
fi
