#!/bin/bash
# what's the advatage of this function to grep directly? not sure ...
if [ "$#" -eq 0 ]; then
    echo "Failed! Too few arguments."
    return 1
fi
if [ "$#" -eq 1 ]; then
    echo "Search in the home directory by default."
    find $HOME -type f -print0 | xargs -0 grep -Hn $1
    return 0
fi
if [ "$#" -eq 2 ]; then
    find $1 -type f -print0 | xargs -0 grep -Hn $2
    return 0
fi
echo "Failed! Too many arguments."
return 2
