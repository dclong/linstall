#!/usr/bin/env bash

function runat.usage(){
    cat << EOF
Run a command or script file (approximately) at a given time. 
This program is not intended to be a replacement of the Linux "at" utility. 
but an alternative when users do not have access to the "at" utility.
Syntax: runat yyyymmddhhmmss command_to_be_run 
EOF
}

function runat(){
    if [ "$1" == "-h" ]; then
        runat.usage
        return 0
    fi
    if [ ${#1} -ne 14 ]; then
        echo "Invalid time format. You must specify time in the format yyyymmddhhmmss."
        return 1
    fi
    script=$(id -un)_$1.sh
    cat << EOF > $script
while [ \$(date +%Y%m%d%H%M%S) -lt $1 ]; do
    sleep 30
done
${@:2}
EOF
    chmod +x $script
    nohup ./$script &
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    runat $@
fi
