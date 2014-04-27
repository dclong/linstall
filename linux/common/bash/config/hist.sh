# don't put duplicate lines or lines starting with space in the history
HISTCONTROL=ignoreboth
# append to history file, don't overwrite it
shopt -s histappend
# setting history length
HISTSIZE=1000
HISTFILESIZE=2000
# dispaly time in history commands
export HISTTIMEFORMAT='%F %T >> '
