#!/usr/bin/env bash

function linfig.vim.usage(){
    cat << EOF
Configure vim.
Syntax: linfig.vim
Make a symbolic link of \"$lommon/vim/vimrc/vimrc\" to \"$HOME/.vimrc\".
Make a symbolic link of \"$lommon/vim/colors\" to \"$HOME/.vim/colors\".
EOF
}

function linfig.vim(){
    echo "Configuring Vim ..."
    local desdir="$HOME/.vim"
    mkdir -vp "$desdir"
    # create a directory for SWap and backUP files
    mkdir -vp "$desdir/swup"
    desfile="$HOME/.vimrc"
    srcfile="$lommon/vim/vimrc/vimrc"
    # if running under MobaXterm in Windows as a virtualization solutions
    if [[ "$(uname -a)" == CYGWIN_NT*GNU/Linux ]]; then
        ln -sf "$srcfile" "$desfile"
        echo "\"$desfile\" -> \"$srcfile\"" 
        ln -sf "$lommon/vim/colors" "$desdir"
        echo "\"$desdir/colors\" -> \"$lommon/vim/colors\"" 
        ln -svf "$lommon/vim/pythonx" "$desdir"
        echo "\"$desdir/pythonx\" -> \"$lommon/vim/pythonx\"" 
#        ln -sf "$lommon/vim/my_snippets" "$desdir" 
#        echo "\"$desdir/my_snippets\" -> \"$lommon/vim/my_snippets\"" 
        ln -sf "$lommon/vim/UltiSnips" "$desdir" 
        echo "\"$desdir/UltiSnips\" -> \"$lommon/vim/UltiSnips\"" 
        ln -sf "$python_dir/vim" "$desdir/pythonx"
        echo "\"$desdir/pythonx\" -> \"$python_dir/vim\""
        echo "Done."
        return 0
    fi
    ln -Tsvf "$srcfile" "$desfile"
    ln -svf "$lommon/vim/colors" "$desdir"
    ln -svf "$lommon/vim/pythonx" "$desdir"
#    ln -svf "$lommon/vim/my_snippets" "$desdir" 
    ln -svf "$lommon/vim/UltiSnips" "$desdir" 
    ln -Tsvf "$python_dir/vim" "$desdir/pythonx"
    echo "Done."
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    linfig.vim $@
fi
