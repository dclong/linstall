#!/bin/bash
#-------------------- Config -------------------------------
#function linux.config.rmdir() {
#    if [ "$#" -ne 1 ]; then
#        echo "Only 1 argument (base directory of configuration files) is supported."
#        return 1
#    fi
#    if [ -e "$1" ]; then
#        if [ -d "$1" ]; then
#            echo "Removing directory (if empty) \"$1\" ..."
#            rmdir "$1"
#        else
#            echo "\"$1\" is a non-directory file!"
#        fi
#    fi
#}
#function linux.config.mkdir() {
#    # need 1 or 2 arguments
#    # $1 the directory to be checked
#    # $2 the prefix, i.e. sudo -u user
#    prefix=""
#    if [ "$#" -eq 2 ]; then 
#        prefix="$2"
#    elif [ "$#" -ne 1 ]; then
#        echo "Wrong number of arguments!"
#        return 1
#    fi
#    if [ ! -e "$1" ]; then
#        echo "Creating directory \"$1\" ..."
#        $prefix mkdir -p "$1"
#        return 0
#    fi
#    if [ ! -d "$1" ]; then
#        echo "A non-directory file \"$1\" exists!"
#        return 1
#    fi
#}

#function linux.config.symlink(){
#    # need 2 or 3 arguments
#    # $1 is source 
#    # $2 is destination
#    # $3 prefix of command, sudo -u user
#    prefix=""
#    if [ "$#" -eq 3 ]; then
#        local prefix="$3"
#    elif [[ "$#" -ne 2 && "$#" -ne 3 ]]; then
#        echo "2 or 3 arguments are required!"
#        return 1
#    fi
#    if [ ! -e "$1" ]; then
#        echo "The source file/directory does not exist!"
#        return 2
#    fi
#    if [ -L "$2" ]; then
#        $prefix rm -rf "$2"
#    elif [ -e "$2" ]; then
#        echo "A non-symbolic file \"$2\" exists!"
#        echo "Do you want to remove it?"
#        echo "y/Y/yes/Yes/YES: Yes"
#        echo "Any other: No"
#        read -p "(Default yes): " remove
#        remove=${remove:-yes}
#        case "$remove" in
#            y|Y|yes|Yes|YES)
#                $prefix rm -rf "$2"
#                if [ $? -eq 0 ]; then
#                    echo "The non-symbolic file \"$2\" is removed."
#                else
#                    return 3 
#                fi
#                ;;
#            *)
#                return 3
#                echo "The non-symbolic file \"$2\" is kept."
#                ;;
#        esac
#    fi
#    $prefix ln -svf "$1" "$2"
#    return 0
#}

#function linux.config.copyfile(){
#    # need 2 or 3 arguments
#    # $1 is source 
#    # $2 is destination
#    # $3 prefix of command, sudo
#    prefix=""
#    if [ "$#" -eq 3 ]; then
#        local prefix="$3"
#    elif [[ "$#" -ne 2 || "$#" -ne 3 ]]; then
#        echo "2 or 3 arguments are required!"
#        return 1
#    fi
#    if [ ! -e "$1" ]; then
#        echo "The source file/directory does not exist!"
#        return 2
#    fi
#    if [ -L "$2" ]; then
#        $prefix rm -rf "$2"
#    elif [ -e "$2" ]; then
#        echo "A non-symbolic file \"$2\" exists!"
#        echo "Do you want to remove it?"
#        echo "y/Y/yes/Yes/YES: Yes"
#        echo "Any other: No"
#        read -p "(Default yes): " remove
#        remove=${remove:-yes}
#        case "$remove" in
#            y|Y|yes|Yes|YES)
#                $prefix rm -rf "$2"
#                echo "The non-symbolic file \"$2\" is removed."
#                ;;
#            *)
#                return 3
#                echo "The non-symbolic file \"$2\" is kept."
#                ;;
#        esac
#    fi
#    $prefix cp "$1" "$2"
#    return 0
#}
    
#function linux.config.xfce4.usage(){
#    cat << EOF 
#Configure the Xfce desktop environment.
#Syntax: linux.config.xfce4
#Create a symbolic link of a configuration directory in \"$lommon/xfce\" to \"$HOME/.config/xfce4\".
#EOF
#}
#function linux.config.xfce4(){
#    echo "Configuring Xfce ..."
#    local srcdir="$lommon/xfce"
#    local deslink="$HOME/.config/xfce4"
#    local cdirs=($(ls -d $srcdir/xfce4*))
#    echo "Please select the configuration directory to use."
#    local n=${#cdirs[@]}
#    for ((i=0; i<$n; ++i)); do
#        echo "$i: ${cdirs[$i]}"
#    done
#    read -p "(Default none): " cdir
#    if [ cdir == "" ]; then
#        return 0
#    fi
#    cdir=${cdir:-$n}
#    cdir=${cdirs[$cdir]}
#    linux.config.symlink "$cdir" "$deslink"
#}

#function linux.config.xfce(){
#    echo "Configuing Xfce ..."
#    # menu 
#    local desdir="$HOME/.config/menus/"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/xfce/menus/xfce-applications.menu" \
#            "$desdir/xfce-applications.menu"
#    fi
#    local desdir="$HOME/.local/share/"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/xfce/applications/" \
#            "$desdir/applications"
#    fi
#    # panel
#    local desdir="$HOME/.config/xfce4/"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/xfce/panel/" "$desdir/panel"
#    fi
#    echo "Done."
#}

#function linux.config.mimeapps(){
#    echo "Configuring mimeapps ..."
#    state=linux.config.mkdir "$HOME/.local/share/applications"
#    # mimeapps.list
#    ln -svf $1/mimeapps/mimeapps.list $HOME/.local/share/applications/
#    echo "Done."
#}

#function linux.config.eclipse(){
#    echo "Configuring Eclipse ..."
#    if [ -f /usr/local/eclipse/eclipse ]; then
        # $prefix ln -svf /usr/local/eclipse/eclipse /usr/bin/eclipse
#    fi
#}


function linux.config.dictionary.usage(){
    cat << EOF
Configure dictionary database.
Syntax: linux.config.dictionary
Make a symbolic link of \"$lommon/dictionary\" to \"$HOME/.dictionary\"."
EOF
}
function linux.config.dictionary(){
    echo "Configuring dictionary ..."
    # links
    linux.config.symlink "$lommon/dictionary" "$HOME/.dictionary"
    echo "Done."
}

function linux.config.juliastudio.usage(){
    cat << EOF
Configure juliastudio.
Syntax: linux.config.juliastudio
Make a symbolic link of \"$lommon/fonts\" to \"$HOME/.fonts\".
EOF
}
function linux.config.juliastudio() {
    echo "Configuring JuliaStudio ..."
    # symbolic links
    local desfile="/usr/bin/jstudio"
    local srcfile="/usr/local/julia-studio/bin/JuliaStudio"
    linux.config.symlink "$srcfile" "$desfile" sudo
}

#function linux.config.zotero.usage(){
#    echo "Configure zotero."
#    echo "Syntax: linux.config.zotero"
#    echo "Make a symbolic link of zotero (installed in /usr/local/) to /usr/bin/zotero."
#}

#function linux.config.zotero() {
#    echo "Configuring Zotero ..."
#    # symbolic links
#    local desdir="/usr/bin/"
#    local srcdir="/usr/local/zotero/"
#    linux.config.symlink "${srcdir}zotero" "${desdir}zotero" sudo
#    linux.config.symlink "${srcdir}run-zotero.sh" "${desdir}run-zotero" sudo
#}

#function linux.config.copy() {
#    echo "Configuring the cloud sync service Copy ..."
#    # symbolic link
#    local desdir="/usr/bin/"
#    local srcdir="/usr/local/copy/"
#    if [ $(getconf LONG_BIT) -eq 32 ]; then
#        srcdir="${srcdir}x86/"
#    else
#        srcdir="${srcdir}x86_64/"
#    fi
#    linux.config.symlink "${srcdir}CopyAgent" "${desdir}copyagent" sudo
#    linux.config.symlink "${srcdir}CopyCmd" "${desdir}copycmd" sudo
#    linux.config.symlink "${srcdir}CopyConsole" "${desdir}copyconsole" sudo
#}

#function linux.config.btsync(){
#    echo "Configuring btsync ..."
#    # symbolic link
#    local desfile=/usr/bin/btsync
#    local srcfile=/opt/btsync/btsync
#    linux.config.symlink $srcfile $desfile sudo
#}

#function linux.config.texlive.usage(){
#    echo "Configure texlive."
#    echo "Syntax: linux.config.texlive"
#    echo "Make a symbolic link of firefox (installed in /usr/local/) to /usr/bin/firefox"
#    echo "Make a symbolic link of \"$lommon/texlive/ctex-xecjk-winfonts.def\" \
#        to \"/usr/share/texlive/texmf-dist/tex/latex/ctex/fontset/ctex-xecjk-winfonts.def\"."
#}
#function linux.config.texlive(){
#    echo "Configuring texlive ..."
#    local desdir="/usr/share/texlive/texmf-dist/tex/latex/ctex/fontset/"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/texlive/ctex-xecjk-winfonts.def" \
#            "$desdir/ctex-xecjk-winfonts.def"
#    fi
#    echo "Done."
#}

#function linux.config.jabref.usage(){
#    echo "Configure JabRef."
#    echo "Syntax: linux.config.jabref"
#    echo "Make a symbolic link of \"$lommon/jabref/prefs.xml\"\
#        to \"$HOME/.java/.userPrefs/net/sf/jabref\"."
#}

#function linux.config.jabref() {
#    echo "Configuring jabref ..."
#    local desdir="$HOME/.java/.userPrefs/net/sf/jabref"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/jabref/prefs.xml" "$desdir/prefs.xml"
#    fi
#    echo "Done."
#}

function linux.config.vbill.usage(){
    echo "Configure vbill"
    echo "Syntax: linux.config.jabref"
    echo "Make a symbolic link of \"$lommon/jabref/prefs.xml\"\
        to \"$HOME/.java/.userPrefs/net/sf/jabref\"."
}

function linux.config.vbill(){
    echo "Configuring verizon bill ..."
    desfile="/usr/bin/vbill"
    srcfile="$ruby_dir/verizon/vbill.rb"
    linux.config.symlink "$srcfile" "$desfile" sudo 
}


#function linux.config.synctime(){
#    echo "Configruing time synchronization ..."
#    local desdir="/etc/cron.weekly"
#    linux.config.symlink "$lommon/system/sync_time" "$desdir/sync_time"
#    echo "Done."
#}


#function linux.config.postfix(){
#    echo "Configuring postfix ..."
#    local desdir="/etc/postfix/"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/postfix/main.cf" "$desdir/main.cf"
#        linux.config.symlink "$lommon/postfix/sasl_passwd" "$desdir/sasl_passwd"
#        linux.config.symlink "$lommon/postfix/sasl_passwd.db" "$desdir/sasl_passwd.db"
#    fi
#    echo "Done."
#}


#function linux.config.network(){
#    echo "Configuing network ..."
#    local desdir="/etc/network/"
#    linux.config.mkdir "$desdir"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.copyfile "$lommon/network/interfaces" "$desdir/interfaces" sudo
#    fi
#    echo "Done."
#}


#function linux.config.mixer(){
#    echo "Configuring mixer ..."
#    local desdir="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml"
#    linux.config.mkdir "$HOME"
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$lommon/xfce/xfce-perchannel-xml/xfce4-mixer.xml" "$desdir/xfce4-mixer.xml"
#    fi
#}


#function linux.config.unison(){
#    echo "Configuring unison ..."
#    local desdir="$HOME/.unison"
#    local desfile="$desdir/default.prf"
#    local srcfile="$lommon/unison/default.prf"
#    linux.config.mkdir "$desdir" 
#    local state=$?
#    if [ $state -eq 0 ]; then
#        linux.config.symlink "$srcfile" "$desfile" 
#    fi
#    echo "Done."
#}

function linux.config.usage(){
    if [ $# -eq 1 ]; then
        echo "Configure installed packages."
        echo "Syntax: linux.config.package"
        echo "To get help use: linux.config.-h package"
        echo "Supported package configuration includes:"
        echo "r: linux.config -h r"
        echo "git: linux.config -h git" 
    else
       linux.config.$2.usage 
    fi
}
function linux.config(){
    # need to write a function return all keywords, 
    # and check whether $1 is in the keywords, ...
    if [ "$1" == "-h" ]; then
        linux.config.usage $@
    else
        linux.config $1
    fi
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linux.config.$@
fi
