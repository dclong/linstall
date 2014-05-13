# ls colors
if [[ "$(uname -a)" != CYGWIN_NT*GNU/Linux ]]; then
	eval $(dircolors -b ${config_root_dir}/linux/common/ls/dircolors.conf)
fi

