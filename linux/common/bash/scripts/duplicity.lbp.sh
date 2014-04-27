function duplicity.lbp.usage(){
    cat << EOF
Use duplicity to backup files on local disk.
Syntax: duplicity.lbp src des
Git directories are not backuped. 
EOF
}
function duplicity.lbp(){
    if [ "$1" == "-h" ]; then
        duplicity.lbp.usage
        return 0
    fi
    if [ ! -e "$1" ]; then
        echo "The source file does not exist."
        return 1
    fi
    if [ ! -e "$2" ]; then
        echo "The destination file does not exist."
        return 2
    fi
    export PASSPHRASE=cooldragon 
#    duplicity --exclude "**.git" "$1" "file://$2"
    duplicity "$1" "file://$2"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    duplicity.lbp $@
fi
