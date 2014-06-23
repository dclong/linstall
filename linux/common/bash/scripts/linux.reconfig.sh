#!/usr/bin/env bash
function deb.reconfig.usage(){
    cat << EOF
Reconfigure a Debian series Linux distribution.
Bash, Git, Vim and R are reconfigured.
EOF
}

function deb.reconfig(){
    local dist="$(lsb_release -d)"
    case "$dist" in
        *Debian* )
            linfig.xsession
            linfig.xdg
            linfig.synaptics
            linfig.tcpd
            linfig.mail
            linfig.shell
            linfig.sshs
            linfig.sshc
            linfig.git
            linfig.vim
            linfig.geany
            linfig.r
            linfig.terminator
            linfig.terminal
            linfig.remmina
            linfig.nomachine
        #    linfig.lightdm
        #    linfig.autostart
            return 0;;
        *LMDE* )
            linfig.xdg
            linfig.tcpd
            linfig.mail
            linfig.shell
            linfig.sshs
            linfig.sshc
            linfig.git
            linfig.vim
            linfig.geany
            linfig.r
            linfig.terminator
            linfig.terminal
            linfig.remmina
            linfig.nomachine
            return 0;;
        *Ubuntu* )
            linfig.xdg
            linfig.tcpd
            linfig.mail
            linfig.shell
            linfig.sshs
            linfig.sshc
            linfig.git
            linfig.vim
            linfig.geany
            linfig.r
            linfig.terminator
            linfig.terminal
            linfig.remmina
            linfig.nomachine
            return 0;;
        * )
            echo "This script does not support ${dist:13}."
            return 1;;
    esac
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    deb.reconfig $@
fi

