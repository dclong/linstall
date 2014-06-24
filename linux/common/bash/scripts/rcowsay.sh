#!/usr/bin/env bash
function rcowsay.usage(){
    cat << EOF
Random version of cowsay.
The syntax is the same as cowsay except that you should not use the -f option.
EOF
}
function rcowsay(){
    local pics=($(ls /usr/share/cowsay/cows/))
    local n=${#pics[@]}
    local choice=$(python -c "import random; print(random.sample(range($n-1), 1)[0])")
    cowsay -f ${pics[$choice]} $@
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    rcowsay $@
fi
