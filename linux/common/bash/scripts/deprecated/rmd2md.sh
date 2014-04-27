function rmd2md.usage(){
    echo "Knit .rmd files into markdown files."
    echo "Syntax: rmd2md file/dir"
}
function rmd2md(){
    file=$(basename "$1")
    pdir=$(basedir "$1")
    output="$pdir/$script_dir/${file%.*}.markdown"
    if [ -f "$1" ]; then
       Rscript --no-init-file -e "knitr::knit(\"$1\",\"$output\")"
    fi
    # need to get _post directory
    rsync "$output" 
}
