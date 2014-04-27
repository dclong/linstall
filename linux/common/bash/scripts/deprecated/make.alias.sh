
function make.alias {
    # make aliases 
    # need 2 or 3 arguments
    # $1 the full path of a directory
    # $2 a command that operate on a file, e.g. vim
    # $3 prefix to be used
    if [ "$#" -gt 3 ]; then
        echo 'Too many arguments!'
        return 2
    fi
    if [ "$#" -eq 3 ]; then
        local prefix=$3
    elif [ "$#" -eq 2 ]; then
        local prefix=$2
    fi
    for file in $(ls.nt $1); do
        echo "alias ${prefix}.$file='${2} ${1}/$file'"
    done
}

