
function tb.profile.usage(){
    cat << EOF 
Setup thunderbird profile.
Syntax: switch.thunderbird [profile]
A symbolic link "$HOME/.thunderbird" pointing to the selected thunderbird profile is created.
EOF
}

function tb.profile(){
    if [[ "$1" == "-h" ]]; then
        tb.profile.usage
        return 0
    fi
    local srcdir="$btsync_dir/thunderbird"
    local desfile="$HOME/.thunderbird"
    if [[ "$#" -gt 0 ]]; then
        local srcfile="$srcdir/$@"
        ln -Tsvf "$srcfile" "$desfile"
        return 0
    fi
    local cdirs=($(ls $srcdir))
    echo "Please select the profile directory to use for thunderbird."
    local n=${#cdirs[@]}
    for ((i=0; i<$n; ++i)); do
        echo "$i: ${cdirs[$i]}"
    done
    read -p "(Default none): " choice
    if [ choice == "" ]; then
        return 0
    fi
    choice=${cdirs[$choice]}
    tb.profile "$choice"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    tb.profile $@
fi
