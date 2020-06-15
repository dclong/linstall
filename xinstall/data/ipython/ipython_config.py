import platform
from pathlib import Path
HOME = Path.home()
PLATFORM = platform.platform().lower()
c = get_config()
c.AliasManager.user_aliases = [
    ("mvi", "mv -i"),
    ("cpi", "cp -ir"),
    ("rsync.progress", "rsync -avh --info=progress2"),
    ("rsync.progress.pc", "proxychains rsync -avh --info=progress2"),
    ("rsync.delete", "rsync -avh --info=progress2 --delete"),
    ("rsync.delete.pc", "proxychains rsync -avh --info=progress2 --delete"),
    ("hdfs.count", "hdfs dfs -count -q -v"),
    ("hdfs.ls", "hdfs dfs -ls"),
    ("blog", "python3 $HOME/archives/blog/main.py"),
    # du
    ("du.0", "du -hd 0"),
    ("du.1", "du -hd 1"),
    ("du.1s", "du -d 1 | sort -n"),
    # docker
    (
        "docker.jupyterhub_ds",
        "docker run -d --hostname jupyterhub-ds --log-opt max-size=50m -p 8000:8000 -p 5006:5006 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ds /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ds.next",
        "docker run -d --hostname jupyterhub-ds --log-opt max-size=50m -p 8000:8000 -p 5006:5006 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ds:next /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ds.linux",
        "docker run -d --hostname jupyterhub-ds --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8000:8000 -p 5006:5006 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ds /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ds.linux.next",
        "docker run -d --hostname jupyterhub-ds --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8000:8000 -p 5006:5006 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ds:next /scripts/sys/init.sh"
    ),
    (
        "docker.vscode_server",
        "docker run -d --hostname vscode-server --log-opt max-size=50m -p 8080:8080 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/vscode-server /scripts/sys/init.sh"
    ),
    (
        "docker.vscode_server.next",
        "docker run -d --hostname vscode-server --log-opt max-size=50m -p 8080:8080 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/vscode-server:next /scripts/sys/init.sh"
    ),
    (
        "docker.vscode_server.linux",
        "docker run -d --hostname vscode-server --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8080:8080 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/vscode-server /scripts/sys/init.sh"
    ),
    (
        "docker.vscode_server.linux.next",
        "docker run -d --hostname vscode-server --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8080:8080 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/vscode-server /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterlab",
        "docker run -d --hostname jupyterlab --log-opt max-size=50m -p 8888:8888 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterlab /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterlab.next",
        "docker run -d --hostname jupyterlab --log-opt max-size=50m -p 8888:8888 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterlab:next /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterlab.linux",
        "docker run -d --hostname jupyterlab --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8888:8888 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterlab /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterlab.linux.next",
        "docker run -d --hostname jupyterlab --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8888:8888 -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterlab:next /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ai",
        "docker run -d --hostname jupyterhub-ai --log-opt max-size=50m -p 8000:8000 --dns 8.8.8.8 --dns 8.8.4.4 --gpus all -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ai /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ai.next",
        "docker run -d --hostname jupyterhub-ai --log-opt max-size=50m -p 8000:8000 --dns 8.8.8.8 --dns 8.8.4.4 --gpus all -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ai:next /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ai.linux",
        "docker run -d --hostname jupyterhub-ai --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8000:8000 --dns 8.8.8.8 --dns 8.8.4.4 --gpus all -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ai /scripts/sys/init.sh"
    ),
    (
        "docker.jupyterhub_ai.linux.next",
        "docker run -d --hostname jupyterhub-ai --log-opt max-size=50m --memory=$(($(head -n 1 /proc/meminfo | awk '{print $2}') * 4 / 5))k --cpus=$(($(nproc) - 1)) -p 8000:8000 --dns 8.8.8.8 --dns 8.8.4.4 --gpus all -e DOCKER_USER=$(id -un) -e DOCKER_USER_ID=$(id -u) -e DOCKER_PASSWORD=$(id -un) -e DOCKER_GROUP_ID=$(id -g) -e DOCKER_ADMIN_USER=$(id -un) -v $(pwd):/workdir -v $(dirname $HOME):/home_host dclong/jupyterhub-ai:next /scripts/sys/init.sh"
    ),
    # find
    ("find.aux", "find . -type f -iname '*.aux'"),
    ("find.avro", "find . -type f -iname '*.avro'"),
    ("find.avsc", "find . -type f -iname '*.avsc'"),
    ("find.bak", "find . -type f -iname '*.bak'"),
    ("find.bin", "find . -name '*.bin'"),
    ("find.brolink", "find . -xtype l"),
    ("find.chp", "find . -type f -iname '*.chp'"),
    ("find.csv", "find . -type f -iname '*.csv'"),
    ("find.class", "find . -name '*.class'"),
    ("find.cel", "find . -type f -iname '*.cel'"),
    ("find.c", "find . -type f -iname '*.c'"),
    ("find.cpp", "find . -type f -iname '*.cpp'"),
    ("find.dockerfile", "find . -type f -name Dockerfile"),
    ("find.dat", "find . -type f -iname '*.dat'"),
    ("find.dll", "find . -type f -iname '*.dll'"),
    ("find.dbf", "find . -type f -iname '*.dbf'"),
    ("find.dylib", "find . -type f -iname '*.dylib'"),
    ("find.dat", "find . -type f -iname '*.dat'"),
    ("find.deb", "find . -name '*.deb'"),
    (
        "find.data",
        "find . -type f -iname '*.xls' -o -iname '*.xlsx' -o -iname '*.csv' -o -iname '*.tsv'"
    ),
    ("find.dvi", "find . -type f -iname '*.dvi'"),
    ("find.dir", "find . -type d"),
    ("find.eps", "find . -type f -iname '*.eps'"),
    (
        "find.excel",
        "find . -type f -iname '*.xls' -o -iname '*.xlsx' -o -iname '*.xlsm'"
    ),
    ("find.file", "find . -type f"),
    ("find.folder", "find.dir"),
    ("find.gz", "find . -name '*.gz'"),
    ("find.gt5m", "find . -xdev -type f -size +5M"),
    ("find.gt10m", "find . -xdev -type f -size +10M"),
    ("find.gt20m", "find . -xdev -type f -size +20M"),
    ("find.gt50m", "find . -xdev -type f -size +50M"),
    ("find.gt100m", "find . -xdev -type f -size +100M"),
    ("find.gt200m", "find . -xdev -type f -size +200M"),
    ("find.gt500m", "find . -xdev -type f -size +500M"),
    ("find.gt1g", "find . -xdev -type f -size +1G"),
    ("find.gt2g", "find . -xdev -type f -size +2G"),
    ("find.gt5g", "find . -xdev -type f -size +5G"),
    ("find.hive", "find . -type f -iname '*.hive'"),
    ("find.h", "find . -type f -iname '*.h'"),
    ("find.hpp", "find . -type f -iname '*.hpp'"),
    ("find.header", "find . -type f -iname '*.hpp' -o -iname '*.h'"),
    ("find.html", "find . -type f -iname '*.html'"),
    ("find.hidden", "find . -name '.[^/]*'"),
    ("find.ipynb", "find . -type f -iname '*.ipynb'"),
    ("find.inf", "find . -name '*.inf'"),
    ("find.jpg", "find . -name '*.jpg'"),
    ("find.jpeg", "find . -name '*.jpeg'"),
    ("find.java", "find . -name '*.java'"),
    ("find.jar", "find . -name '*.jar'"),
    ("find.java", "find . -type f -iname '*.java'"),
    ("find.json", "find . -type f -iname '*.json'"),
    ("find.log", "find . -name '*log'"),
    ("find.markdown", "find . -type f -iname '*.markdown' -o -iname '*.md'"),
    ("find.md", "find.markdown"),
    ("find.mov", "find . -type f -iname '*.mov'"),
    (
        "find.media",
        "find . -type f -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.mp3' -o -iname '*.avi' -o -iname '*.mkv' -o -iname '*.mov' -o -iname '*.mp4' -o -iname '*.wmv'"
    ),
    ("find.pig", "find . -type f -iname '*.pig'"),
    ("find.pdf", "find . -type f -iname '*.pdf'"),
    ("find.png", "find . -iname '*.png'"),
    ("find.parquet", "find . -iname '*.parquet'"),
    ("find.pom", "find . -name 'pom.xml'"),
    ("find.ppt", "find . -type f -iname '*.ppt' -o -iname '*.pptx'"),
    (
        "find.py",
        "find . -type f -iname '*.py' -not -path '*/.venv/*' -not -path '*/venv/*' -not -path '*/.ipynb_checkpoints/*'"
    ),
    ("find.r", "find . -type f -iname '*.r'"),
    ("find.rdata", "find . -type f -iname '*.rdata'"),
    ("find.rpt", "find . -type f -iname '*.rpt'"),
    ("find.rmarkdown", "find . -type f -iname '*.rmarkdown' -o -iname '*.rmd'"),
    ("find.rmd", "find.rmarkdown"),
    ("find.rhistory", "find . -type f -iname '*.rhistory'"),
    ("find.snippets", "find . -type f -name '*.snippets'"),
    ("find.sql", "find . -type f -iname '*.sql'"),
    ("find.sh", "find . -type f -iname '*.sh'"),
    ("find.scala", "find . -type f -iname '*.scala'"),
    ("find.so", "find . -type f -iname '*.so'"),
    ("find.sl", "find . -type f -iname '*.sl'"),
    ("find.swp", "find . -name '*.swp'"),
    ("find.sys", "find . -name '*.sys'"),
    ("find.sync", "find . -name '*.!sync'"),
    (
        "find.spreadsheet",
        "find . -type f -iname '*.xls' -o -iname '*.xlsx' -o -iname '*.csv'"
    ),
    ("find.txt", "find . -type f -iname '*.txt'"),
    (
        "find.textemp",
        "find . -type f -iname '*.dvi' -o -iname '*.log' -o -iname '*.aux' -o -iname '*.lof' -o -iname '*.log' -o -iname '*.toc' -o -iname '*.bbl' -o -iname '*.blg' -o -iname '*.synctex.gz' -o -iname '*.nav' -o -iname '*.snm' -o -iname '*.vrb' -o -iname '*.out'"
    ),
    ("find.tar.gz", "find . -name '*.tar.gz'"),
    ("find.tsv", "find . -type f -iname '*.tsv'"),
    ("find.tex", "find . -type f -iname '*.tex'"),
    ("find.tilde", "find . -name '*~'"),
    (
        "find.video",
        "find . -type f  -iname '*.avi' -o -iname '*.mkv' -o -iname '*.mov' -o -iname '*.mp4' -o -iname '*.wmv'"
    ),
    ("find.word", "find . -type f -iname '*.doc' -o -iname '*.docx' -o iname"),
    ("find.word", "find . -type f -iname '*.doc' -o -iname '*.docx'"),
    ("find.xml", "find . -type f -iname '*.xml'"),
    # mount
    (
        "mount.ntfs.sdb1",
        "sudo mount -o uid=$(whoami),gid=$(whoami),fmask=0137,dmask=0027 /dev/sdb1"
    ),
    ("mount.sdb1", "sudo mount /dev/sdb1"),
    ("umount.sdb1", "sudo umount /dev/sdb1"),
    (
        "mount.ntfs.sdc1",
        "sudo mount -o uid=$(whoami),gid=$(whoami),fmask=0137,dmask=0027 /dev/sdc1"
    ),
    ("mount.sdc1", "sudo mount /dev/sdc1"),
    ("umount.sdc1", "sudo umount /dev/sdc1"),
    ("mount.cd", "sudo mount -t iso9660 -o ro /dev/cdrom"),
    ("mount.sr0", "sudo mount -t iso9660 -o ro /dev/sr0"),
    (
        "mount.downloads",
        "sudo mount -t nfs -o nfsvers=3 192.168.0.8:$HOME/downloads mnt/nfsshare/"
    ),
    (
        "mount.vboxsf",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077"
    ),
    (
        "mount.vboxsf.hh",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077 host_home"
    ),
    (
        "mount.vboxsf.cdrive",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077 cdrive ${HOME}/cdrive"
    ),
    (
        "mount.vboxsf.ddrive",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077 ddrive ${HOME}/ddrive"
    ),
    (
        "mount.vboxsf.edrive",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077 edrive ${HOME}/edrive"
    ),
    (
        "mount.vboxsf.fdrive",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077 fdrive ${HOME}/fdrive"
    ),
    (
        "mount.vboxsf.gdrive",
        "sudo mount -t vboxsf -o uid=$(whoami),gid=$(whoami),fmask=177,dmask=077 gdrive ${HOME}/gdrive"
    ),
    ("ls.media", "ls *.jpg *.jpeg *.png *.mp3 *.avi *.mkv *.mov *.mp4 *.wmv"),
    ("ls.excel", "ls *.xls *.xlsx"),
    ("ls.word", "ls *.doc *.docx"),
    ("ls.spreadsheet", "ls *.xls *.xlsx *.csv"),
    ("ls.data", "ls *.xls *.xlsx *.csv *.tsv"),
    ("ls.archive", "ls *.zip *.tar.gz *.tar.xz *.tar"),
    ("ls.zip", "ls.archive"),
    ("ls.package", "ls *.air *.deb *.jar *.apk"),
    ("ls.pkg", "ls *.air *.deb *.jar *.apk"),
    ("ls.tex.aux", "ls *.aux *.bbl *.blg *.log *.toc *.synctex.gz"),
]
if "darwin" in PLATFORM:
    c.AliasManager.user_aliases.extend(
        [
            ("md5sum", "md5 -r"),
            (
                "ffmpeg.record_screen",
                "ffmpeg -f avfoundation -i '1' -pix_fmt yuv420p -r 25 $(date +%m%d%H%M%S).mp4"
            ),
            (
                "record_screen",
                "ffmpeg -f avfoundation -i '1' -pix_fmt yuv420p -r 25 $(date +%m%d%H%M%S).mp4"
            ),
        ]
    )
    trash_dir = HOME / ".Trash"
else:
    c.AliasManager.user_aliases.extend(
        [
            (
                "ffmpeg.record_screen",
                "ffmpeg -f x11grab -r 25 -s cif -i :0.0 $(date +%m%d%H%M%S).mp4"
            ),
            (
                "record_screen",
                "ffmpeg -f x11grab -r 25 -s cif -i :0.0 $(date +%m%d%H%M%S).mp4"
            ),
        ]
    )
    trash_dir = HOME / ".local/share/Trash/"
c.IPCompleter.use_jedi = False
