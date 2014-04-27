
function deb.config.xfce4.usage(){
    cat << EOF 
Configure the Xfce desktop environment.
Syntax: deb.config xfce4
Create a symbolic link of a configuration directory in \"$lommon/xfce\" to \"$HOME/.config/xfce4\".
EOF
}

function deb.config.xfce4(){
    echo "Configuring Xfce ..."
    local srcdir="$lommon/xfce"
    local deslink="$HOME/.config/xfce4"
    local cdirs=($(ls -d $srcdir/xfce4*))
    echo "Please select the configuration directory to use."
    local n=${#cdirs[@]}
    for ((i=0; i<$n; ++i)); do
        echo "$i: ${cdirs[$i]}"
    done
    read -p "(Default none): " cdir
    if [ cdir == "" ]; then
        return 0
    fi
    cdir=${cdir:-$n}
    cdir=${cdirs[$cdir]}
    deb.config.symlink "$cdir" "$deslink"
}

