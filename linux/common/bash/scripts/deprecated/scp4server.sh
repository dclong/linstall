
function scp4server {
    # copy files from a server to local 
    # need 4 arguments
    # $1: server name
    # $2: port number
    # $3: the remote file name
    # $4: the local/destination file name
    # This function is mainly for the simplicity of creating aliases.
    scp -P $2 -r $1:"$3" "$4"
    local state=$?
    if [ $state -eq 0 ]; then
        echo "Copying succeed."
    fi
}

