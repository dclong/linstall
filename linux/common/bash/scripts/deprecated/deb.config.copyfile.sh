#!/bin/bash

function deb.config.copyfile.usage(){
    cat << EOF
    Copy 
EOF
}
function deb.config.copyfile(){
    # need 2 or 3 arguments
    # $1 is source 
    # $2 is destination
    # $3 prefix of command, sudo
    prefix=""
    if [ "$#" -eq 3 ]; then
        local prefix="$3"
    elif [[ "$#" -ne 2 || "$#" -ne 3 ]]; then
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
                echo "The non-symbolic file \"$2\" is removed."
                ;;
            *)
                return 3
                echo "The non-symbolic file \"$2\" is kept."
                ;;
        esac
    fi
    $prefix cp "$1" "$2"
    return 0
}
    
