
function lsr.file {
	# list files only
	# need 1 arguments
	ls -lR | grep ^- | awk '{print $9}'
}

