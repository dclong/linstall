#!/usr/bin/env bash
function create.script.usage(){
    cat << EOF
Create a script of the given name using template.
Syntax: create.script script_name [srcdir]
If srcdir is not given, then a script is created in the directory "$bash_function_dir".
EOF
}
function create.script(){
    if [ "$1" == "-h" ]; then
        create.script.usage
        return 0
    fi
    local srcdir=$2
    if [ "$srcdir" == "" ]; then
        srcdir="$bash_scripts_dir"
    fi
    # make a file of the given name
    if [ -e "$srcdir/$1.sh" ]; then
        echo "A script with the same name exists!"
        return 1
    fi
    touch "$srcdir/$1.sh"
    cat << CREATE_SCRIPT_EOF > "$srcdir/$1.sh"
#!/usr/bin/env bash

function $1.usage(){
    cat << EOF
Description
Syntax: $1
EOF
}

function $1(){
    if [ "\$1" == "-h" ]; then
        $1.usage
        return 0
    fi
    
}

if [ "\$0" == \${BASH_SOURCE[0]} ]; then
    $1 \$@
fi
CREATE_SCRIPT_EOF
    chmod +x "$srcdir/$1.sh"
    echo "$srcdir/$1.sh is created."
}

if [ "$0" == ${BASH_SOURCE[0]} ]; then
    create.script $@
fi
