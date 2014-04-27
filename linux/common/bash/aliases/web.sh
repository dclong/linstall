# downloading a whole website using wget
alias wget.site='wget --random-wait -r -p -e robots=off -U mozilla' 
alias wget.dir='wget -r --no-parent -e robots=off'
alias wget.folder='wget.dir'
alias wget.dir.nohtml='wget -r --no-parent -e robots=off -R "*.html"'
alias wget.folder.nohtml='wget.dir.noindex'
# http
# more up-to-date version than python -m SimpleHTTPServer
alias python.http.server='python3 -m http.server'
# ftp
alias ftp.cran='ftp cran.r-project.org'
# ips
alias ls.ip='sudo arp-scan -l'
# rake
alias rake.auto='rake generate && rake deploy'


