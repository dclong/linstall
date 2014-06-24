#!/usr/bin/env bash
function stop.nx.usage(){
    cat << EOF
Stop the NX server if it's running.
Syntax: stop.nx
EOF
}
function stop.nx(){
    if [ "$1" == "-h" ]; then
        stop.nx.usage
    fi
    if [ $(ps aux | grep -i nxserver | wc -l) -gt 1 ]; then
        echo "Shutdowning the NX server ..."
        sudo /usr/NX/bin/nxserver --shutdown
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    stop.nx $@
fi
