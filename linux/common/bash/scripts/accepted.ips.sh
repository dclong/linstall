#!/bin/bash
function accepted.ips.usage(){
    echo "Exact and show accepted ips from authentication log files."
    echo "Syntax: accepted.ips log_file"
}
function accepted.ips(){
    if [ "${1#*.}" == "gz" ]; then
        sudo gunzip -c "$1" | grep -i 'accepted' | awk '{print $11}' | sort | uniq
    else
        sudo grep -i 'accepted' "$1" | awk '{print $11}' | sort | uniq
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    accepted.ips $@
fi
