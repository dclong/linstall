#!/bin/bash
function vbvm.export.usage(){
    echo "Export virtualbox virtual machines. This function creates a directory with the name of the virtual machine and current date and export files into this directory."
    echo "Syntax: vbvm.export vm_name des_dir"
    echo "where vm_name is the name of the virtual machine to be exported and des_dir is the name of the directory where the virtual machine is to be exported."
}
function vbvm.export(){
    if [ "$1" == "-h" ]; then
        vbvm.export.usage
        return 0
    fi
    local name=$1_$(date +%Y%m%d)
    local desdir="$2/$name"
    echo "Creating directory \"$desdir\" ..."
    mkdir $desdir
    echo "Exporting the virtual machine to the created directory ..."
    VBoxManage export $1 -o "$desdir/$name.ovf"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    vbvm.export $@
fi
