function debian.install.1.usage(){
    echo -e "Installs apt-file, vim, openssh-client and git.\n\
        Packages are automatically configured if necessary and possible."
}
function debian.install.1(){
    wajig install -y apt-file 
    debian.install.vim
    debian.install.sshc
    debian.install.git
}

function debian.install.2.usage(){
    cat << EOF
Installs xfce, terminator, keepassx, evince, tmux and screen.
Packages are automatically configured if necessary and possible.
EOF
}

function debian.install.2(){
    debian.install.xfce
    wajig install -y keepassx evince tmux screen xarchiver remmina rdesktop 
    debian.install.terminator
}

function debian.install.3.usage(){
    cat << EOF
Installs wget, curl, rsync, openssh-server and sshfs.
Packages are automatically configured if necessary and possible.
EOF
}
function debian.install.3(){
    wajig install -y wget curl rsync 
    debian.install.sshfs
    debian.install.sshs
}
function debian.install.4.usage(){
    cat << EOF
Installs abiword, gnumeric, nautilus-dropbox, software-center and chinese fonts.
Packages are automatically configured if necessary and possible.
EOF
}
function debian.install.4(){
    wajig install -y nautilus-dropbox software-center abiword gnumeric  
    debian.install.chinese
}
function debian.install.5.usage(){
    cat << EOF
Installs R and Julia.
Packages are automatically configured if necessary and possible.
EOF
}
function debian.install.5(){
    debian.install.r
    debian.install.julia
    # debian.install.texlive
}
function debian.install.6.usage(){
	cat << EOF 
Installs archive tools (zip, rar, drtx, etc.) and media tools (see debian.install.media.usage for details).
Packages are automatically configured if necessary and possible.
EOF
}
function debian.install.6(){
    debian.install.archive
    debian.install.media
}
function debian.install.7.usage(){
    cat << EOF
Installs virtualbox and transmission.
Packages are automatically configured if necessary and possible.
EOF
}
function debian.install.7(){
    wajig install -y virtualbox transmission
    debian.install.editor
}
