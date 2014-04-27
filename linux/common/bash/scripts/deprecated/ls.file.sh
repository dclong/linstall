
function ls.file {
	# list files only
	# need 1 arguments
	ls -l | grep ^- | awk '{print $9}'
}

