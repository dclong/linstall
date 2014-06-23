#!/usr/bin/env bash
function linstall.thunderbird.usage(){
    cat << EOF
Automatically download the right latest version of Thunderbird, install and configure it.
Syntax: linstall.thunderbird
EOF
}

function linstall.thunderbird(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            # download latest thunderbird
            local path=ftp.mozilla.org/pub/mozilla.org/thunderbird/releases/latest/linux-$(uname -m)/en-US/
            local dir=$(mktemp -d)
            echo "Temporary directory \"$dir\" is created."
            cd $dir
            echo "Downloading thunderbird into \"$dir\" ..."
            wget -r --no-parent -e robots=off http://$path
            path=$(ls $path/thunderbird-*)
            local filename=$(basename $path)
            cp $path $filename
            # decompress thunderbird installation files
            echo "Decompressing thunderbird installation file ..."
            if [ "$filename" == *.tar.bz2 ]; then
                option=-jxvf
            elif [ "$filename" == *.tar.gz ]; then
                option=-zxvf
            else
                echo "Unrecognized installation file!"
                return 1
            fi
            tar $option $filename
            # copy to /opt
            echo "Copying thunderbird to /opt ..."
            sudo rm -rf /opt/thunderbird
            sudo cp -r thunderbird /opt/
            # uninstall iceweasel
            if [ "$(wajig list | grep -i icedove)" != "" ]; then
                # wajig purge -y iceweasel
                echo "Please uninstall icedove."
            fi
            return 0;;
        *LMDE* )
            wajig install thunderbird
            return 0;;
        *Ubuntu* )
            wajig install thunderbird
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
    linfig.thunderbird
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linstall.thunderbird $@
fi
