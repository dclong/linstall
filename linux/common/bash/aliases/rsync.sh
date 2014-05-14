alias rsync.progress='rsync -ah --progress'
alias rsync.nogit='rsync -ah --progress --exclude "**.git"'

alias rsync2l11='rsync2server $(whoami)@$l11 $ssh_port'
alias rsync2l10='rsync2server $(whoami)@$l10 $ssh_port'
alias rsync2y570='rsync2server $(whoami)@$y570 $ssh_port'
alias rsync2econ3='rsync2server lisa1107@$econ3 $ssh_port'
alias rsync2s07='rsync2server lisa1107@$s07 $ssh_port'
alias rsync2s08='rsync2server lisa1107@$s08 $ssh_port'
alias rsync2nb205='rsync2server $(whoami)@$nb205 $ssh_port'
alias rsync2home='rsync2server $(whoami)@$homeip $ssh_port'
alias rsync2ubsas='rsync2server $(whoami)@${ubsas} 22'
alias rsync2boasas='rsync2server $(nixuser)@${boasas} 22'



alias rsync4l11='rsync4server $(whoami)@$l11 $ssh_port'
alias rsync4l10='rsync4server $(whoami)@$l10 $ssh_port'
alias rsync4y570='rsync4server $(whoami)@$y570 $ssh_port'
alias rsync4econ3='rsync4server lisa1107@$econ3 $ssh_port'
alias rsync4s07='rsync4server lisa1107@$s07 $ssh_port'
alias rsync4s08='rsync4server lisa1107@$s08 $ssh_port'
alias rsync4nb205='rsync4server $(whoami)@$nb205 $ssh_port'
alias rsync4home='rsync4server $(whoami)@$homeip $ssh_port'
alias rsync4ubsas='rsync4server $(whoami)@${ubsas} 22'
alias rsync4boasas='rsync4server $(nixuser)@${boasas} 22'


alias backup.thunderbird='backup $HOME/.thunderbird "$backup_dir/tbp"'
alias backup.tbp='backup.thunderbird'
alias backup.documents='backup "$documents" "$backup_dir/documents"'
alias backup.doc='backup.documents'
