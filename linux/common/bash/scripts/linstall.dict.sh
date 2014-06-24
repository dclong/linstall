#!/usr/bin/env bash
function linstall.dict.usage(){
    cat << EOF
Installs some useful dictionaries. Databases dict-gcide, dict-devil, dict-jargon, dict-xdict and dict-stardic are installed.
Syntax: linstall.dict
EOF
}
function linstall.dict(){
    wajig install dict dict-gcide dict-devil dict-jargon dict-xdict dict-stardic
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.dict $@
fi
