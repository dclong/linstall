#!/usr/bin/env bash
#---------------- Uninstall -------------------------------

function linfig.uninstall.juliastudio(){
    echo "Removing installtion files ..."
    sudo rm -r /usr/local/julia-studio
    echo "Removing symbolic links ..."
    sudo rm /usr/bin/juliastudio /usr/bin/julia-studio /usr/bin/julia.studio
}

#function linfig.uninstall.zotero(){
#    echo "Removing installtion files ..."
#    sudo rm -r /usr/local/zotero
#    echo "Removing symbolic links ..."
#    sudo rm /usr/bin/zotero /usr/bin/run-zotero
#}

#function deb.uninstall.copy() {
#    echo "Removing installation files ..."
#    sudo rm -r /usr/local/copy
#    echo "Removing symbolic links ..."
#    sudo rm /usr/bin/copyagent /usr/bin/copycmd /usr/bin/copyconsole
#    echo "Done."
#}

function linfig.uninstall.blog(){
    echo "Removing symbolic links ..."
    sudo rm /usr/bin/epost /usr/bin/eheader
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    debian.uninstall $@
fi
