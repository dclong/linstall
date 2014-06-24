#!/usr/bin/env bash
function sed.insert.usage(){
    echo "Insert chracters in the beginning of a specified line in text files."
    echo "Syntax: sed.insert line_number text_insert files [dlm]"
    echo "Arguments should be quoted in single quotation marks."
}
function sed.insert(){
    local dlm=_
    if [ "$#" -eq 4 ]; then
        dlm=$4
    fi
    sed -i "${1} s${dlm}^${dlm}${2}${dlm}" ${3} 
}
function sed.insertln.usage(){
    echo "Insert lines into at specified lines into text files."
    echo "Syntax: sed.insertln line_number text_insert files [dlm]"
    echo "Arguments should be quoted in single quotation marks."
}
function sed.insertln(){
    sed.insert $1 '$2\n' '$3' $4
}
function sed.shabang.usage(){
    echo "Insert \"#!/usr/bin\n\" as the first line into text files."
    echo "Syntax: sed.shabang files [dlm]"
}
function sed.shabang(){
    sed.insert 1 '#!/usr/bin\n' 
}
if [ "$0" == ${BASH_SOURCE[0]} ]; then
    sed.insert $@
fi
