
#' TODO
#' Make the code support increase, decrease, set, get,
#' percent and so on
#' It's probably easier to write the code in Python
screen.brightness(){
    if [ "$#" -eq 0 ]; then
        setpci -s 00:02.0 F4.B
        return 0
    fi
    if [ "$#" -eq 1 ]; then
        sudo setpci -s 00:02.0 F4.B=$1
        return 0
    fi
    echo "Too many arguments!"
    return 1
}
