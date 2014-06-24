#!/usr/bin/env bash
# TODO make this more powerful, up k levels
# more robust about error and so on
function ancester.path.usage(){
    cat << EOF 
Get an ancester path of this script match the specified pattern.
Syntax: script.name basename untilname
EOF
}
function ancester.path(){
    local p=$(readlink -f ${BASH_SOURCE[0]})
    while [ $(basename ${p}) != "$1" ]; do
        p=$(dirname ${p})
        if [ ${p} == "$2" ]; then
            echo "$2"
            return 1
        fi
    done
    echo ${p}
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    ancester.path $@
fi
