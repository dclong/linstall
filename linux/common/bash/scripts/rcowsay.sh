#!/bin/bash
function rcowsay.usage(){
    echo "Random version of cowsay."
    echo "The syntax is the same as cowsay except that you should not use the -f option."
}
function rcowsay(){
    local pics=($(ls /usr/share/cowsay/cows/))
    local n=${#pics[@]}
    cowsay -f ${pics[$(Rscript --no-init-file -e "cat(sample(0:($n-1), 1))")]} $@
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    rcowsay $@
fi
