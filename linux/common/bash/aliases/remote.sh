# vnc
alias vino.start='export DISPLAY=:0.0 && /usr/lib/vino/vino-server' 
alias start.vino='vino.start'
alias vnc.y570='vncviewer $y570'
alias vnc.toshiba1='vncviewer $toshiba:1'
alias vnc.toshiba2='vncviewer $toshiba:2'
alias vnc.toshiba3='vncviewer $toshiba:3'
alias vnc.home='vncviewer $homeip'

# nx 
alias start.nx='sudo /usr/NX/bin/nxserver --startup'
alias nx.start='start.nx'
alias restart.nx='sudo /usr/NX/bin/nxserver --restart'
alias nx.restart='restart.nx'
# stop.nx is defined as function 
alias nx.stop='stop.nx'
