#!/bin/bash

function link.resume.usage(){
    cat << EOF
Link resume to home directory for easy access.
Syntax: link.resume
EOF
}
function find.dir(){
    local dirs=($(ls -d $1/j*))
    local n=${#dirs[@]}
    local dir=${dirs[n-1]}
    echo "$dir"
}
function link.resume(){
    if [ "$1" == "-h" ]; then
        link.resume.usage
        return 0
    fi
    local desdir="$HOME/resume"
    mkdir -p "$desdir"
    local ml_stat=$(find.dir "$job_dir/resume/ml_stat")
    ln -Tsvf "$ml_stat/resume--Ben_Du.pdf" "$desdir/resume-dmml-Ben_Du.pdf"
    ln -Tsvf "$ml_stat/resume--Ben_Du.docx" "$desdir/resume-dmml-Ben_Du.docx"
    ln -Tsvf "$ml_stat/resume--Ben_Du.txt" "$desdir/resume-dmml-Ben_Du.txt"
    local quant=$(find.dir "$job_dir/resume/quant")
    ln -Tsvf "$quant/resume--Ben_Du.pdf" "$desdir/resume-quant-Ben_Du.pdf"
    ln -Tsvf "$quant/resume--Ben_Du.docx" "$desdir/resume-quant-Ben_Du.docx"
    ln -Tsvf "$quant/resume--Ben_Du.txt" "$desdir/resume-quant-Ben_Du.txt"
    local biostat=$(find.dir "$job_dir/resume/biostat")
    ln -Tsvf "$biostat/resume--Ben_Du.pdf" "$desdir/resume-biostat-Ben_Du.pdf"
    ln -Tsvf "$biostat/resume--Ben_Du.docx" "$desdir/resume-biostat-Ben_Du.docx"
    ln -Tsvf "$biostat/resume--Ben_Du.txt" "$desdir/resume-biostat-Ben_Du.txt"
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    link.resume $@
fi
