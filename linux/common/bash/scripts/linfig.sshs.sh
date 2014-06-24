#!/usr/bin/env bash
function linfig.sshs.usage(){
    cat << EOF
Configure SSH server.
Syntax: linfig.ssh
Create symbolic link of \"$lommon/ssh/ssh_config\" to \"/etc/ssh/ssh_config/ssh_config\".
Create symbolic link of \"$lommon/ssh/sshd_config\" to \"/etc/sshd_config/sshd_config\".
EOF
}
function linfig.sshs(){
    echo "Configuring SSH server ..."
    local desfile="/etc/ssh/sshd_config"
    local srcfile="$lommon/ssh/sshd_config"
    if [ -f "$desfile" ]; then
        cp "$desfile" "${srcfile}.bak"
    fi
    sudo cp -i "$srcfile" "$desfile" 
    sudo chmod 644 "$desfile"
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.sshs $@
fi

