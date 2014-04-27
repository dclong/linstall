#!/bin/bash

function linfig.matlab.usage(){
    cat << EOF
Configures MATLAB.
Syntax: linfig.matlab
Make a symbolic link of MATLAB executable (installed in /usr/local/) to /usr/bin/matlab.
EOF
}

function linfig.matlab(){
    if [ "$1" == "-h" ]; then
        linfig.matlab.usage
        return 0
    fi
    echo "Configuring Matlab ..."
    local srcdir="/usr/local/MATLAB/"
    local state=$?
    if [ $state -eq 0 ]; then
        subdirs=$(find "$srcdir" -mindepth 1 -maxdepth 1 -not -empty -type d)
        n=$(echo "$subdirs" | wc -l)
        if [ $n -gt 1 ]; then
            echo "Multiple versions of Matlab exist. Please type in the one that you want to link."
            ls "$srcdir" | echo
            read version
            local desdir="/usr/bin/"
            linfig.mkdir "$desdir" sudo
            local state=$?
            if [ $state -eq 0 ]; then
                linfig.symlink "$srcdir/$version/bin/matlab" \
                "$desdir/matlab" sudo 
            fi
        else
            if [ $n -eq 1 ]; then
                local desdir="/usr/bin/"
                linfig.mkdir "$desdir" sudo
                local state=$?
                if [ $state -eq 0 ]; then
                    linfig.symlink "$subdirs/bin/matlab" \
                        "$desdir/matlab" sudo 
                fi
            else
                echo "Matlab is not installed (to the default location). \
                    Please configure it manually."
            fi
        fi
    fi
    echo "Done."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.matlab $@
fi
