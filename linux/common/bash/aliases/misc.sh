# sudo
alias sudo='sudo '

# ip
alias ip.private="/sbin/ifconfig $2 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}'" 
alias private.ip=ip.private
alias ip.public='curl ifconfig.me'
alias public.ip=ip.public

alias clock.console='while sleep 1;do tput sc;tput cup 0 $(($(tput cols)-29));date;tput rc;done &'

# awk
alias awk.users="awk -F: '\$3>=1000' /etc/passwd"
alias awk.unique="awk '!x[$0]++'" 

# ls
alias ls.tree="ls -R | grep ':$' | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'"

# services
alias restart.lightdm='sudo service lightdm restart'

# entertainment
alias fortune.cowsay='fortune | cowsay'
alias cowsay.fortune='fortune | cowsay'
alias vcowsay.done='vcowsay "Job is done."'
# ImageMagick
alias avconv.record='avconv -f x11grab -s wxga -r 25 -i :0.0 -sameq' 

# source bashrc
alias source.bashrc="source $bash_dir/bashrc"

# wajig
alias wajig.list="wajig list | awk '{print \$2}'"
alias wajig.auto="wajig update && wajig upgrade"

# cp and mv
alias cpi="cp -i"
alias cpa="cp -a"
alias mvi="mv -i"

# grep
alias cgrep="grep --color"

# VBoxManage
alias VBoxManage.vmdk2vdi='VBoxManage clonehd --format VDI'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# xfce4
alias xaf='xfce4-appfinder &'
alias xsm='xfce4-settings-manager &'

# btsync
# alias btsync='btsync --config "$HOME/.sync/btsync.conf"'
alias btsync.default='btsync --config "$HOME/.sync/btsync.conf"'

# firefox
alias ff='firefox &'
