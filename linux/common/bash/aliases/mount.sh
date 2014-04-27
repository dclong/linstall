
# sshfs
alias sshfs.l11='sshfs.server $(whoami)@$l11 $ssh_port'
alias sshfs.l10='sshfs.server $(whoami)@$l10 $ssh_port'
alias sshfs.y570='sshfs.server $(whoami)@$y570 $ssh_port'
alias sshfs.music='sshfs.y570 $HOME/btsync/music $HOME/btsync/music'
alias sshfs.pictures='sshfs.y570 $HOME/btsync/pictures $HOME/btsync/pictures'
alias sshfs.software='sshfs.y570 $HOME/btsync/software $HOME/btsync/software'
alias sshfs.study='sshfs.y570 $HOME/btsync/study $HOME/btsync/study'
alias sshfs.research='sshfs.y570 $HOME/btsync/research $HOME/btsync/research'
alias sshfs.home='sshfs.server $(whoami)@$homeip $ssh_port'
alias sshfs.nb205='sshfs.server $(whoami)@$nb205 $ssh_port'
alias sshfs.econ3='sshfs.server lisa1107@$econ3 $ssh_port'
alias sshfs.s07='sshfs.server lisa1107@$s07 $ssh_port'
alias sshfs.s08='sshfs.server lisa1107@$s08 $ssh_port'
# mount
alias mount.ntfs.sdb1='sudo mount -o uid=$(whoami),gid=$(whoami),fmask=0137,dmask=0027 /dev/sdb1'
alias mount.sdb1='sudo mount /dev/sdb1'
alias umount.sdb1='sudo umount /dev/sdb1'
alias mount.ntfs.sdc1='sudo mount -o uid=$(whoami),gid=$(whoami),fmask=0137,dmask=0027 /dev/sdc1'
alias mount.sdc1='sudo mount /dev/sdc1'
alias umount.sdc1='sudo umount /dev/sdc1'
alias mount.vboxsf='sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami)'
alias mount.vboxsf.hh='sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami) host_home'
alias mount.cd="sudo mount -t iso9660 -o ro /dev/cdrom"
alias mount.sr0="sudo mount -t iso9660 -o ro /dev/sr0"
alias mount.downloads='sudo mount -t nfs -o nfsvers=3 192.168.0.8:/home/dclong/downloads mnt/nfsshare/'


# bitcasa
alias bitcasa.mount='mkdir -p ~/bitcasa && sudo mount -tbitcasa duchuanlong+bitcasa@gmail.com ~/bitcasa'
alias mount.bitcasa='bitcasa.mount'

