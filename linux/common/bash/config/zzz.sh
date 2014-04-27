if [[ $(uname -n) == y570 || $(uname -n) == y450 || $(uname -n) == nb205 ]]; then
#    record ip
#    /sbin/ifconfig > ${HOME}/Dropbox/ips/$(hostname)_ip.txt

    # swap Caps Lock and ESC
    caps2escape

    # set vim as the default text editor
    export EDITOR=/usr/bin/vim

    if [ $RANDOM -lt 3000 ]; then
        fortune | rcowsay
    else
        report.du
    fi
fi
