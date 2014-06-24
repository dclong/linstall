#!/usr/bin/env bash
function sshfs.server.usage(){
    echo "Mount remote filesystem using sshfs and fuse."
    echo "Syntax: sshfs.server server port remote_dir local_dir"
    echo "where server is the name/address of the remote server,\
        port is the port of ssh, \
        remote_dir is the directory on the remote server to be mounted on the local machine, \
        and local_dir is an empty directory on the local machine \
        where the remote directory is mounted."
}
function sshfs.server {
    if [ "$1" == "-h" ]; then
        sshfs.server.usage
        return 0
    fi
    sshfs -p $2 $1:"$3" "$4"
    local state=$?
    if [ $state -eq 0 ]; then
        echo "\"$3\" on \"$1\" has been mounted to the local directory \"$4\"." 
    fi
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    sshfs.server $@
fi
