#!/bin/bash
function rsync2server.usage(){
    echo "Sync files from local to server."
    echo "Syntax: rsync2server server port local_file remote_file [options]"
}
function rsync2server(){
    if [ "$1" == "-h" ]; then
        rsync2server.usage
        return 0
    fi
    if [ "$#" -lt 4 ]; then
        echo "Too few arguments."
        return 0
    fi
    if [ "$#" -eq 4 ]; then
        options=""
    else
        options="$5"
    fi
    rsync -e "ssh -p $2" -avzh --progress "$3" $1:"$4" $5
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    rsync2server $@
fi
