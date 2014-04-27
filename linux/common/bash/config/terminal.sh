#----------------- terminal -----------------------------
# check the window size after each command and, if necessary, 
# update the values of LINES and COLUMNS
shopt -s checkwinsize

# colorful commands
export PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n\[\033[01;32m\]\$\[\033[00m\] '
