#!/usr/bin/env bash
function accepted.ips.usage(){
    cat << EOF
Exact and show accepted ips from authentication log files.
Syntax: accepted.ips log_file
EOF
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
