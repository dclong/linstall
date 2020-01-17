# ------------------------- programming languages -------------------------
def cargo(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} cargo')
        if is_macos():
            brew_install_safe(['cargo'])
        if is_centos_series():
            run_cmd(f'{args.sudo_s} yum install {args._yes_s} cargo')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} cargo')
        if is_macos():
            run_cmd(f'brew uninstall cargo')
        if is_centos_series():
            run_cmd(f'yum remove cargo')


def openjdk8(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} openjdk-jdk-8 maven gradle',
            )
        if is_macos():
            cmd = 'brew tap AdoptOpenJDK/openjdk && brew cask install adoptopenjdk8'
            run_cmd(cmd)
        if is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} openjdk-jdk-8 maven gradle',
            )
        if is_macos():
            run_cmd(f'brew cask uninstall adoptopenjdk8')
        if is_centos_series():
            pass


def sdkman(**kwargs):
    """ Install sdkman.
    https://sdkman.io/install
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f'''curl -s https://get.sdkman.io | bash''')
    if args.config:
        pass
    if args.uninstall:
        pass


def yapf(**kwargs):
    args = namespace(kwargs)
    if args.install:
        run_cmd(f'{args.pip} install --user {args._yes_s} yapf')
    if args.config:
        shutil.copy2(
            os.path.join(BASE_DIR, 'yapf/style.yapf'),
            os.path.join(args.dst_dir, '.style.yapf')
        )
    if args.uninstall:
        run_cmd(f'{args.pip} uninstall {args._yes_s} yapf')


def nodejs(**kwargs):
    """Install nodejs and npm.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            cmd = f'''{args.sudo_s} apt-get install {args._yes_s} nodejs npm'''
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(['nodejs'])
        if is_centos_series():
            run_cmd(f'{args.sudo_s} yum install {args._yes_s} nodejs')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} nodejs')
        if is_macos():
            run_cmd(f'brew uninstall nodejs')
        if is_centos_series():
            run_cmd(f'yum remove nodejs')


def ipython(**kwargs):
    """Install IPython for Python 3.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user {args._yes_s} ipython"
        run_cmd(cmd)
    if args.config:
        run_cmd(f"{args.ipython} profile create")
        src_dir = BASE_DIR / "ipython"
        dst_dir = HOME / ".ipython/profile_default"
        shutil.copy2(src_dir / "ipython_config.py", dst_dir)
        shutil.copy2(src_dir / "startup.ipy", dst_dir / "startup")
    if args.uninstall:
        pass


def python3(**kwargs):
    """Install and configure Python 3.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            cmd = f"{args.sudo_s} apt-get install {args._yes_s} python3 python3-pip python3-setuptools"
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(["python3"])
        if is_centos_series():
            run_cmd(
                f"{args.sudo_s} yum install {args._yes_s} python34 python34-devel python34-pip",
            )
            run_cmd(f"{args.pip} install --user setuptools")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f"{args.sudo_s} apt-get purge {args._yes_s} python3 python3-dev python3-setuptools python3-pip python3-venv",
            )
        if is_macos():
            run_cmd(f"brew uninstall python3")
        if is_centos_series():
            run_cmd(f"yum remove python3")


def poetry(**kwargs):
    """Install and configure Python poetry.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | {args.python}"
        run_cmd(cmd)
    poetry_bin = HOME / ".poetry/bin/poetry"
    if args.config:
        # symbolic link
        desfile = BIN_DIR / "poetry"
        if desfile.exists():
            desfile.unlink()
        desfile.symlink_to(poetry_bin)
        # make poetry always create virtual environment in the root directory of the project
        run_cmd(f"{poetry_bin} config virtualenvs.in-project true")
        # bash completion
        if args.bash_completion:
            if is_linux():
                cmd = f"{poetry_bin} completions bash | {args.sudo_s} tee /etc/bash_completion.d/poetry.bash-completion > /dev/null"
                run_cmd(cmd)
                return
            if is_macos():
                cmd = f"{poetry_bin} completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion"
                run_cmd(cmd)
    if args.uninstall:
        run_cmd(f"{poetry_bin} self:uninstall")



def pyjnius(**kwargs):
    """Install pyjnius for calling Java from Python.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user Cython pyjnius"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def spark(**kwargs):
    """Install Spark into /opt/spark.
    """
    args = namespace(kwargs)
    if args.install:
        spark_hdp = f"spark-{args.version}-bin-hadoop2.7"
        url = f"{args.mirror}/spark-{args.version}/{spark_hdp}.tgz"
        cmd = f"""curl {url} -o /tmp/{spark_hdp}.tgz \
                && {args.sudo_s} tar -zxvf /tmp/{spark_hdp}.tgz -C /opt/ \
                && {args.sudo_s} ln -svf /opt/{spark_hdp} /opt/spark \
                && rm /tmp/{spark_hdp}.tgz
            """
        run_cmd(cmd)
    if args.config:
        cmd = "export SPARK_HOME=/opt/spark"
        run_cmd(cmd)
    if args.uninstall:
        cmd = f"{args.sudo_s} rm -rf /opt/spark*"
        run_cmd(cmd)


def pyspark(**kwargs):
    """Install PySpark.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install pyspark findspark optimuspyspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall pyspark findspark optimuspyspark"
        run_cmd(cmd)



def rust(**kwargs):
    """Install the Rust programming language.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.sudo_s} apt-get install {args._yes_s} cmake cargo"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.sudo_s} apt-get purge {args._yes_s} cargo"
        run_cmd(cmd)


def git_ignore(**kwargs):
    """Insert patterns to ingore into .gitignore in the current directory.
    """
    args = namespace(kwargs)
    if args.python_pattern:
        lines = [
            ".DS_Store",
            ".idea/",
            "*.ipr",
            "*.iws",
            ".ipynb_checkpoints/",
            ".coverage",
            ".mypy",
            ".mypy_cache",
            "*.crc",
            "__pycache__/",
            "venv/",
            ".venv/",
            "target/",
            "dist/",
            "*.egg-info/",
        ]
        lines = [line.strip() + "\n" for line in lines]
        with Path(".gitignore").open("a") as fout:
            fout.writelines(lines)
    if args.java_pattern:
        lines = [
            "# Java",
            "*.class",
            "## BlueJ files",
            "*.ctxt",
            "## Mobile Tools for Java (J2ME)",
            ".mtj.tmp/",
            "## Package Files",
            "*.jar",
            "*.war",
            "*.ear",
            "# Gradle",
            ".gradle",
            "/build/",
            "/out/",
            "## Ignore Gradle GUI config",
            "gradle-app.setting",
            "## Avoid ignoring Gradle wrapper jar file (.jar files are usually ignored)",
            "!gradle-wrapper.jar",
            "## Cache of project",
            ".gradletasknamecache",
            "# virtual machine crash logs, see http://www.java.com/en/download/help/error_hotspot.xml",
            "hs_err_pid*",
            "# Mac",
            ".DS_Store",
            "# IDE",
            ".idea/",
            "*.ipr",
            "*.iws",
            "# Misc",
            "core",
            "*.log",
            "deprecated",
        ]
        lines = [line.strip() + "\n" for line in lines]
        with Path(".gitignore").open("a") as fout:
            fout.writelines(lines)

def git(**kwargs) -> None:
    """Install and configure Git.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} git git-lfs',
            )
        elif is_macos():
            brew_install_safe(['git', 'git-lfs', 'bash-completion@2'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install git')
        run_cmd('git lfs install')
    if args.uninstall:
        run_cmd('git lfs uninstall')
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} git git-lfs')
        elif is_macos():
            run_cmd(f'brew uninstall git git-lfs')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove git')
    if args.config:
        ssh_client(config=True)
        gitconfig = HOME / '.gitconfig'
        # try to remove the file to avoid dead symbolic link problem
        remove_file_safe(gitconfig)
        shutil.copy2(BASE_DIR / 'git/gitconfig', gitconfig)
        gitignore = HOME / '.gitignore'
        remove_file_safe(gitignore)
        shutil.copy2(BASE_DIR / 'git/gitignore', gitignore)
        if is_macos():
            file = '/usr/local/etc/bash_completion.d/git-completion.bash'
            bashrc = f'\n# Git completion\n[ -f {file} ] &&  . {file}'
            with (HOME / '.bash_profile').open('a') as fout:
                fout.write(bashrc)
    if 'proxy' in kwargs and args.proxy:
        run_cmd(f'git config --global http.proxy {args.proxy}')
        run_cmd(f'git config --global https.proxy {args.proxy}')

        

def antlr(**kwargs):
    """Install and configure Antrl4.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} antlr4')
        elif is_macos():
            brew_install_safe(['antlr4'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install antlr')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} antlr4')
        elif is_macos():
            run_cmd(f'brew uninstall antlr4')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove antlr')
