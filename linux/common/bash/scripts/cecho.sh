#!/usr/bin/env bash
function cecho.usage(){
    echo "Display colorful text in terminal."
    echo "Syntax: cecho color text"
    echo "Supported color includes: black, white, read, blue, green, yellow, cyan, magenta."
}
function cecho(){
    case "$1" in
        "-h")
            cecho.usage;;
        "black")
            echo -e "\E[0;30m${2}\E[0;30m"
            ;;
        "blue")
            echo -e "\E[0;34m${2}\E[0;30m"
            ;;
        "cyan")
            echo -e "\E[0;36m${2}\E[0;30m"
            ;;
        "green")
            echo -e "\E[0;32m${2}\E[0;30m"
            ;;
        "magenta")
            echo -e "\E[0;35m${2}\E[0;30m"
            ;;
        "red")
            echo -e "\E[0;31m${2}\E[0;30m"
            ;;
        "yellow")
            echo -e "\E[0;33m${2}\E[0;30m"
            ;;
        "white")
            echo -e "\E[0;37m${2}\E[0;30m"
            ;;
        *)
            cecho red "Color not supported currently!"
            return 1
            ;;
    esac
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    cecho $@
fi
