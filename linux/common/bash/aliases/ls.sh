# display files not ending with ~
alias ls='ls --color=auto' 
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ls.nt='ls --ignore=*~'
alias ls.all='ls -a'
alias ls.lh='ls -lh'
alias ls.nc='ls --color=never'
alias ls.sd='ls /dev/sd*'
alias ls.dir='ls -d */'
alias ls.tree="ls -R | grep ':$' | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'"

