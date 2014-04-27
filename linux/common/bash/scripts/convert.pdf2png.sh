#!/bin/bash
function convert.pdf2png.usage(){
    cat << EOF
Convert all pdf images in a directory to PNG images.
Syntax: convert.pdf2png dir
The argument dir is the directory in which pdf images are to be converted to PNG images.
EOF
}

function convert.pdf2png(){
    if [ "$#" -ne 1 ]; then
        echo "Exactly 1 argument is required."
        return 1
    fi
    if [ $1 == "-h" ]; then
        convert.pdf2png.usage
    fi
    echo "Converting pdf images in \"$1\" to PNG ..."
    for f in $1/*.pdf; do 
        convert $f $1/$(basename $f .pdf).png; 
        echo "$f has been converted to PNG."
    done;
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    convert.pdf2png $@
fi

