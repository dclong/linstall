function avconv.video2mp3.usage(){
    echo "Extract video to mp3."
    echo "Syntax: avconv.video2mp3 input_file [output_file]"
}
function avconv.video2mp3(){
    if [ "$1" == "-h" ]; then
        avconv.video2mp3.usage
        return 0
    fi
    if [ "$#" -eq 2 ]; then
        output="${2%.*}.mp3"
    elif [ "$#" -eq 1 ]; then
        output="${1%.*}.mp3"
    else
        echo "Wrong number of arguments!"
        return 1
    fi
    avconv -i "$1" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "$output"
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    avconv.video2mp3 $@
fi
