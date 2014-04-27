function mplayer.wma2mp3.usage(){
    echo "Convert .wma audio to .mp3 audio using mplayer."
    echo "Syntax: mplayer wma_file"
}
function mplayer.wma2mp3(){
    if [ "$1" == "-h" ]; then
        mplayer.wma2mp3.usage
        return 0
    fi
    mplayer -vo null -vc dummy -af resample=44100 -ao pcm:waveheader "$1"
    lame -m s -V 3 audiodump.wav
    mv audiodump.mp3 $(basename "$1" .wma).mp3
    rm audiodump.wav
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    mplayer.wma2mp3 $@
fi
