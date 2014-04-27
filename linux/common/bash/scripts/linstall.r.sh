#!/bin/bash
function linstall.r.usage(){
        cat << EOF
Install R.
Syntax: linstall.r
EOF

}
function linstall.r(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* | *LMDE* | *Ubuntu* )
            wajig install r-base-dev # rstudio 
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
    linfig.r
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.r $@
fi
