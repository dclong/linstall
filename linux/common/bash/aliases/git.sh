# git
alias git.c='git commit'
alias git.ac='git commit -a'
alias git.acp='git commit -a -m ... && git push'
alias git.modified="git status | grep 'modified' | sed 's/^#.*modified://'"
alias git.deleted="git status | grep 'deleted' | sed 's/^#.*deleted://'"
alias git.renamed="git status | grep 'renamed' | sed 's/^#.*renamed://'"
alias git.stat='git status'
alias git.commit='git commit -m'
alias git.om="git push origin master"
alias push.om="git.om"
