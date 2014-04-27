#!/bin/bash
function report.du.usage(){
    echo "Report disk usage. Warn user if the disk space is under 5G."
    echo "Syntax report.du"
}
function report.du(){
    if [ "$1" == "-h" ]; then
        report.du.usage
        return 0
    fi
    df -lh | head -n 2
    local disk_left=$(df -l | awk 'NR==2 {print $4}')
    if [ "$disk_left" -lt 10000000 ]; then
        local disk_left=$(df -lh | awk 'NR==2 {print $4}')
        vcowsay "Disk space is low. $disk_left is left."
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    report.du $@
fi
