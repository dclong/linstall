
function scp2server {
    # copy files from local to server
    # need 4 arguments
    # $1: server name
    # $2: port number
    # $3: local file 
    # $4: remote file
    # This function is mainly for the simplicity of creating aliases.
    scp -P $2 -r "$3" $1:"$4"
    local state=$?
    if [ $state -eq 0 ]; then
        echo "Copying succeed."
    fi
}

