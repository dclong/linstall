
ls.ic(){
    # ls ignoring case
    if [ "$#" -eq 1 ]; then
        find . -maxdepth 1 -iname \*$1\*
        return 0
    fi
    if [ "$#" -eq 2 ]; then
        find $1 -maxdepth 1 -iname \*$2\*
        return 0
    fi
    echo "Only 1 or 2 arguments are allowed."
    return 1
}

