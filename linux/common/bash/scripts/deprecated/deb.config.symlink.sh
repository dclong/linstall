#!/bin/bash

function deb.config.symlink.usage(){
    cat << EOF
Make a symbolic link in a safe manner.
Syntax: deb.config.symlink srcfile desfile [command_prefix]
command_prefix can be "sudo" or "sudo -u user" so that you can run commands with super permission.
EOF
}
function deb.config.symlink(){
    prefix=""
    if [ "$#" -eq 3 ]; then
        local prefix="$3"
    elif [[ "$#" -ne 2 && "$#" -ne 3 ]]; then
        echo "2 or 3 arguments are required!"
        return 1
    fi
    if [ ! -e "$1" ]; then
        echo "The source file/directory does not exist!"
        return 2
    fi
    if [ -L "$2" ]; then
        $prefix rm -rf "$2"
    elif [ -e "$2" ]; then
        echo "A non-symbolic file \"$2\" exists!"
        echo "Do you want to remove it?"
        echo "y/Y/yes/Yes/YES: Yes"
        echo "Any other: No"
        read -p "(Default yes): " remove
        remove=${remove:-yes}
        case "$remove" in
            y|Y|yes|Yes|YES)
                $prefix rm -rf "$2"
                if [ $? -eq 0 ]; then
                    echo "The non-symbolic file \"$2\" is removed."
                else
                    return 3 
                fi
                ;;
            *)
                return 3
                echo "The non-symbolic file \"$2\" is kept."
                ;;
        esac
    fi
    $prefix ln -svf "$1" "$2"
    return 0
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    deb.config.symlink $@
fi
