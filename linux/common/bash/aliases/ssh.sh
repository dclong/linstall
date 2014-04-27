# ssh
alias ssh.auth_sock0='export SSH_AUTH_SOCK=0'
alias ssh.l10='ssh -p $ssh_port $(whoami)@$l10'
alias ssh.l11='ssh -p $ssh_port $(whoami)@$l11'
alias ssh.i1='ssh -p $ssh_port $(whoami)@$i1'
alias ssh.i2='ssh -p $ssh_port $(whoami)@$i2'
alias ssh.i3='ssh -p $ssh_port $(whoami)@$i3'
alias ssh.i4='ssh -p $ssh_port $(whoami)@$i4'
alias ssh.y570='ssh -p $ssh_port $(whoami)@$y570'
alias ssh.y450='ssh -p $ssh_port $(whoami)@$y450'
alias ssh.home='ssh -p $ssh_port $(whoami)@$homeip'
alias ssh.nb205='ssh -p $ssh_port $(whoami)@$nb205'
alias ssh.s07='ssh -p 22 lisa1107@$s07'
alias ssh.s08='ssh -p 22 lisa1107@$s08'
alias ssh.econ3='ssh -p 22 lisa1107@$econ3'
alias ssh.s3='ssh -p 46904 dclong@$s3'
alias ssh.ubsas="ssh -p 22 $(whoami)@${ubsas}"
# diff using ssh
alias diff.y570='diff.server $(whoami)@$y570 $ssh_port'
alias diff.home='diff.server $(whoami)@$homeip $ssh_port'
alias diff.nb205='diff.server $(whoami)@$nb205 $ssh_port'

alias ssh-copy-id.l11='ssh-copy-id -i ${HOME}/.ssh/id_rsa.pub "$(whoami)@$l11 -p $ssh_port"'
alias ssh-copy-id.l10='ssh-copy-id -i ${HOME}/.ssh/id_rsa.pub "$(whoami)@$l10 -p $ssh_port"'
alias ssh-copy-id.y570='ssh-copy-id -i ${HOME}/.ssh/id_rsa.pub "$(whoami)@$y570 -p $ssh_port"'
alias ssh-copy-id.econ3='ssh-copy-id -i ${HOME}/.ssh/id_rsa.pub "lisa1107@$econ3 -p $ssh_port"'


