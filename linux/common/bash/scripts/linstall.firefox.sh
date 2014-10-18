#!/usr/bin/env bash
function linstall.firefox.usage(){
    cat << EOF
Automatically download the latest version of Firefox (for the current Linux distribution), install and configure it.
Syntax: linstall.firefox
EOF
}

function linstall.firefox(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            # download latest firefox
            local path=ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest/linux-$(uname -m)/en-US/
            local dir=$(mktemp -d)
            echo "Temporary directory \"$dir\" is created."
            cd $dir
            echo "Downloading firefox into \"$dir\" ..."
            wget -r --no-parent -e robots=off http://$path
            path=$(ls $path/firefox-*)
            local filename=$(basename $path)
            cp $path $filename
            # decompress firefox installation files
            echo "Decompressing firefox installation file ..."
            if [[ "$filename" == *.tar.bz2 ]]; then
                option=-jxvf
            elif [[ "$extension" == *.tar.gz ]]; then
                option=-zxvf
            else
                echo "Unrecognized installation file!"
                return 1
            fi
            tar $option $filename
            # copy to /opt
            echo "Copying firefox files to /opt ..."
            sudo rm -rf /opt/firefox
            sudo cp -r firefox /opt/
            # install flashplugin-nonfree to make firefox more usable
            echo "Installing flashplugin-nonfree ..."
            wajig install -y flashplugin-nonfree
            # uninstall iceweasel
            if [ "$(wajig list | grep -i iceweasel)" != "" ]; then 
                # wajig purge -y iceweasel
                echo "Please uninstall iceweasel manually!"
            fi
        *LMDE* )
            wajig install firefox mint-flashplugin
        *Ubuntu* )
            wajig install firefox flashplugin-installer
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
    linfig.firefox
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.firefox $@
fi
