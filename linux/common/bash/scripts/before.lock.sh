function before.lock.usage(){
    cat << EOF
Performs necessary clearups before locking the computer.
It shutdowns the NX server if it's running and warns about forgotten mounting devices.
Syntax: before.lock.usage
EOF
}
function before.lock(){
    # start bittorrent sync if it's not running
    if [ $(ps aux | grep -i btsync | wc -l) -le 1 ]; then
        echo "BitTorrent Sync isn't running. Do you want to start it?"
        read -p "Y/n:" choice
        choice=${choice:-"y"}
        choice=${choice,,}
        if [ "$choice" == "y" ]; then
            echo "You choose to start BitTorrent Sync."
            btsync
        else
            echo "You choose not to start BitTorrent Sync."
        fi
    fi
    # start dopbox if it's not running
    if [ "$(dropbox status)" == "Dropbox isn't running!" ]; then
        echo "Dropbox isn't running. Do you want to start it?"
        read -p "Y/n:" choice
        choice=${choice:-"y"}
        choice=${choice,,}
        if [ "$choice" == "y" ]; then
            echo "You choose to start Dropbox."
            dropbox start
        else
            echo "You choose not to start Dropbox."
        fi
    fi
    # check if disk is correctly mounted
    local md=$HOME/mnt/wd
    if [ $(ls /dev/sd? | wc -l) -gt 1 ] && [ "$(mountpoint $md)" == "$md is not a mountpoint" ]; then
        echo "You might forget to mount a removal disk. Abort to mount disk manually?"
        read -p "Y/n: " choice
        choice=${choice:y}
        choice=${choice,,}
        if [ choice == "y" ]; then
            exit 0
        fi
    fi
    # stop NX server to improve security
    if [ $(ps aux | grep -i nxserver | wc -l) -gt 1 ]; then
        echo "Do you want to shutdown the NX server?"
        read -p "Y/n:" choice
        choice=${choice:-"y"}
        choice=${choice,,}
        if [ "$choice" == "y" ]; then
            echo "You choose to shutdown the NX server."
            stop.nx
        else
            echo "You choose not to shutdown the NX server."
        fi
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    before.lock $@
fi
