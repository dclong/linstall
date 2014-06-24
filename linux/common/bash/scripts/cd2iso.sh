#!/usr/bin/env bash
function cd2iso.usage(){
    cat <<EOF
Make an iso image from a CD/DVD file.
usage: cd2iso dev output
EOF
}
function cd2iso(){
    if [ "$1" == "-h" ]; then
        cd2iso.usage
        return 0
    fi
    if [ "$#" -ne 2 ]; then
        echo "Exactly 2 arguments are required."
        cd2iso.uage
        return 1
    fi
    info=$(isoinfo -d -i $1) 
    ## Get Block size of CD
    blocksize=$(echo $info | grep -o "Logical block size is: [0-9]*" | cut -d " " -f 5)
    if test "$blocksize" = ""; then
        echo catdevice FATAL ERROR: Blank blocksize >&2
        exit
    fi
    ## Get Block count of CD
    blockcount=$(echo $info | grep -o "Volume size is: [0-9]*" | cut -d " " -f 4)
    if test "$blockcount" = ""; then
        echo catdevice FATAL ERROR: Blank blockcount >&2
        exit
    fi
    echo "Running the following command. It might take a while."
    echo "dd if=\"$1\" bs=$blocksize count=$blockcount of=\"$2\""
    dd if="$1" bs=$blocksize count=$blockcount of="$2"
} 

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    cd2iso $@
fi
