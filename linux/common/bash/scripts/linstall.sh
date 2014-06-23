#!/usr/bin/env bash
#------------------ Install -------------------------------
function linstall.server(){
    apt-get install sudo wajig vim openssh-client openssh-server screen tmux 
    linfig.ssh
}
function linstall.dbms(){
    wajig install mysql-server mysql-workbench sqlite3 mongodb
}
function linstall.finance(){
    wajig install gnucash
}
function linstall.speedup.usage(){
    echo "Installs packages (readahead, localepurge, bootchart and preload) that speeds up Debian."
    echo "Syntax: linstall.speedup"
}
function linstall.speedup(){
    wajig install -y readahead localepurge bootchart preload
}
function linstall.terminator(){
    wajig install -y terminator
    linfig.terminator
}
function linstall.media.usage(){
    echo "Installs some multimedia related tools including vlc, ffmpeg, tesseract-ocr, gocr, imagemagic, gwenview and pdftk."
    echo "Syntax: linstall.media"
}
function linstall.media(){
    wajig install -y vlc ffmpeg tesseract-ocr gocr imagemagick gwenview pdftk
}
function linstall.archive(){
    wajig install -y unzip zip rar unrar p7zip tar dtrx xarchiver
}
function linstall.archive.usage(){
    echo "Installs archive tools (tar, unzip, zip, rar, unrar, p7zip and dtrx)"
    echo "Syntax: linstall.archive"
}
function linstall.chinese(){
    linstall.ibus
    linstall.fonts
}
function linstall.editor.usage(){
    echo "Installs some popular editors including vim, eclipse, textstudio and gedit."
    echo "Syntax: linstall.editor"
}
function linstall.editor(){
    linstall.vim
    linstall.geany
    wajig install -y eclipse texstudio 
}
function linstall.postfix(){
    wajig install -y postfix
}
function linstall.sshfs(){
    wajig install -y sshfs 
    linfig.fuse
}
function linstall.entertainment.usage(){
    echo "Installs fortune and cowsay."
    echo "Syntax: linstall.entertainment"
}
function linstall.entertainment(){
    wajig install -y fortune cowsay
}
function linstall.network(){
    # ask which wireless manager to use
    echo "Which network manager do you want to install?"
    echo "1: network-manager-gnome"
    echo "2: wicd"
    echo "Any other key: none of them"
    read -p "(Default 1): " nm
    nm=${nm:-1} 
    case "$nm" in
        "1")
            nm=network-manager-gnome
            ;;
        "2")
            nm=wicd
            ;;
        *)
            nm=""
            ;;
    esac
    wajig install -y $nm arp-scan
}
function linstall.de(){
    # ask which desktop manager to use
    echo "Which desktop manager do you want to install?"
    echo "1: lightdm"
    echo "2: gdm3"
    echo "3: kdm"
    echo "Any other key: none of them"
    read -p "(Default 1): " dm
    dm=${dm:-1}
    case "$dm" in
        "1")
            dm=lightdm
            ;;
        "2")
            dm=gdm3
            ;;
        "3")
            dm=kdm
            ;;
        *)
            dm=""
            ;;
    esac
    wajig install -y $dm
}
function linstall.xfce4(){
    wajig install -y xfce4 xfce4-datetime-plugin xfce4-battery-plugin 
    linstall.de
    linstall.network
    linfig.xfce4 
}
function linstall.python(){
    wajig install -y ipython3 ipython3-notebook
}
function linstall.git(){
    # install git
    wajig install -y git
    linfig.git
}
function linstall.fonts.usage(){
    echo 'Install some fonts (mostly chinese related) including: ttf-arphic-uming, ttf-wqy-microhei, ttf-wqy-zenhei, xfonts-wqy and fonts-sil-abyssinica.'
    echo 'You can also installing existing (via symbolic link) fonts using linfig.fonts.'
    echo 'Syntax: linstall.fonts'
}
# chinese fonts
function linstall.fonts(){
    wajig install -y ttf-arphic-uming ttf-wqy-microhei ttf-wqy-zenhei \
        xfonts-wqy fonts-sil-abyssinica
    linfig.fonts
}
# install tools needed to build .deb packages
function linstall.deb(){
    wajig install -y build-essential autoconf automake libtool pkg-config intltool checkinstall
}
function linstall.sshc(){
    wajig install -y openssh-client 
    linfig.sshc
}
function linstall.sshs(){
    wajig install -y openssh-server fail2ban
    linfig.sshs
}
function linstall.java.usage(){
    echo "Installs JDK, icedtea-netx and icedtea-plugin."
    echo "Syntax: linstall.java"
}
function deb.intall.java(){
    wajig install -y default-jdk icedtea-netx icedtea-plugin
}
function linstall.julia(){
    wajig install -y julia # julia-studio
}
function linstall.gedit(){
    wajig install -y gedit
    # linfig.gedit
}
function linstall.unison(){
    wajig install -y unison
    linfig.unison
}
function linstall.iceweasel(){
    wajig install -y iceweasel flashplugin-nonfree
}
function linstall.btsync(){
    filename=$(basename "$1")
    extension="${filename##*.}"
    if [ $extension == "bz2" ]; then
        option=-jxvf
    elif [ $extension == "gz" ]; then
        option=-zxvf
    else
        echo "Unrecognized installation file!."
        return 1
    fi
    local desdir=/opt/btsync
    sudo mkdir -p $desdir 
    echo "Uncompressing files into \"$desdir\" ..."
    sudo tar $option $1 -C $desdir
    linfig.btsync
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    deb.install $@
fi
