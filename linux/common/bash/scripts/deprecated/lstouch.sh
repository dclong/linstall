
function lstouch {
    if [ "$#" -eq 0 ]; then
        echo "Failed! Too few arguments."
        return 1
    fi
    if [ "$#" -eq 1 ]; then
       if [ -f $1 ] || [ -d $1 ]; then
           ls $1
           return 0
       fi
       touch $1
       echo "File \"$1\" did not exist and is now created."
       return 0
    fi
    if [ "$#" -ge 2 ]; then
        echo "Failed! Too many arguments."
        return 2
    fi
}

