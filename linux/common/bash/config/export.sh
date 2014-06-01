# move file to trash and backup files to be overwritten
# you can find config_root_dir automatically,
# see .bashrc for inspiration
export trash_dir="${HOME}/.local/share/Trash/files"
export cloud_dir="$HOME/cloud"
export btsync_dir="$HOME/btsync"
export backup_dir="$btsync_dir/backup"
export btsync_dclong="$btsync_dir/dclong"
export btsync_me="$btsync_dclong"
export btsync_downloads="$btsync_dclong/downloads"
export btsync_cloud="$btsync_dir/cloud"
export code_dir="${cloud_dir}/code"
export blog_dir="${cloud_dir}/blog"
export btsync_vcr="$btsync_dir/vcr"
export ideas_dir="$btsync_vcr/ideas_todo"
export todo_dir="$ideas_dir"
export archives_dir="${HOME}/archives"
export dropbox_dir="${HOME}/Dropbox"
# export sparkleshare_dir="${HOME}/SparkleShare"
export cyride_dir="$dropbox_dir/cyride"
# export job_dir="${btsync_vcr}/job"
#export job_dir="${dropbox_dir}/job"
export job_dir="${HOME}/Spaces/misc/job"
export resume_dir="${job_dir}/resume"
export research_dir="${dropbox_dir}/research"
export nettleton_dir="${research_dir}/nettleton"
export vardeman_dir="${research_dir}/vardeman"
export share_dir="${dropbox_dir}/share"
export share_lisha="${share_dir}/lisha_li"
export share_ling="${share_dir}/ling_li"
# export aerofs_dir="${HOME}/AeroFS"
# export tutorial_dir="${aerofs_dir}/tutorial"
# export life_dir="${aerofs_dir}/life"
# export vbill_dir="${life_dir}/vbill"
export downloads_dir="${HOME}/downloads"
export latex_dir="${code_dir}/latex"
export cpp_dir="${code_dir}/cpp"
export python_dir="${code_dir}/python"
export mongodb_dir="${code_dir}/mongodb"
export blog_en="${blog_dir}/en"
export eblog_dir="${blog_dir}/en"
export edeploy_dir="$blog_dir/en_deploy"
export blog_cn="${blog_dir}/cn"
export cblog_dir="${blog_dir}/cn"
export cdeploy_dir="$blog_dir/cn_deploy"
export blog_home="${blog_dir}/home"
export hblog_dir="${blog_dir}/home"
export hdeploy_dir="$blog_dir/home_deploy"
# define variables for servers
export nixuser="$(whoami)"
export ssh_port='323'
export l11='linux11.stat.iastate.edu'
export l10='linux10.stat.iastate.edu'
export i1='impact1.stat.iastate.edu'
export i2='impact2.stat.iastate.edu'
export i3='impact3.stat.iastate.edu'
export i4='impact4.stat.iastate.edu'
export y570='192.168.0.4'
#export y570='192.168.0.8'
export y450='192.168.0.6'
export homeip='174.108.114.169'
export nb205='192.168.1.35'
export s07='student07.econ.iastate.edu'
export s08='student08.econ.iastate.edu'
export econ3='econ3.econ.iastate.edu'
export s3='192.168.0.5'
# export ubsas="chbobdev201"
export aml='/risk/aml/'
export myaml="$aml/user_aml/dclong"
#----------------------------------------------
config_root_dir="$(ancester.path linux /)"
export config_root_dir="$(dirname ${config_root_dir})"
export common="$config_root_dir/common"
export linux_dir="${config_root_dir}/linux"
export lommon="${linux_dir}/common"
export vimrc="${lommon}/vim/vimrc"
export bash_dir="$lommon/bash"
export bash_functions_dir="${bash_dir}/functions"
export bash_config_dir="${bash_dir}/config"
export bash_aliases_dir="${bash_dir}/aliases"
export bash_scripts_dir="${bash_dir}/scripts"
export debian_dir="${linux_dir}/debian"
export ubuntu_dir="${linux_dir}/ubuntu"
export antix_dir="${linux_dir}/antix"
export lmde_dir="${linux_dir}/lmde"
export mint_dir="${linux_dir}/mint"
export cygwin_dir="${linux_dir}/cygwin"
export cygwin_bash="${cygwin_dir}/bash"
export cygwin_scripts="${cygwin_bash}/scripts"
export cygwin_functions="${cygwin_bash}/functions"
export cygwin_config="${cygwin_bash}/config"
#------------------------------------------
export ultisnips_dir="$HOME/.vim/vim-addons/UltiSnips"
export ultisnips_snip="$HOME/.vim/vim-addons/UltiSnips/UltiSnips"
