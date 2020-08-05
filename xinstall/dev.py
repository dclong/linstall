"""Installing dev related tools.
"""
import logging
import shutil
from pathlib import Path
from argparse import Namespace
from .utils import (
    HOME,
    BASE_DIR,
    BIN_DIR,
    is_ubuntu_debian,
    is_centos_series,
    is_linux,
    update_apt_source,
    brew_install_safe,
    is_macos,
    remove_file_safe,
    run_cmd,
    namespace,
    add_subparser,
    option_user,
)
from .web import ssh_client


def openjdk8(**kwargs):
    """Install OpenJDK 8.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args.yes_s} openjdk-jdk-8 maven gradle", )
        if is_macos():
            cmd = "brew tap AdoptOpenJDK/openjdk && brew cask install adoptopenjdk8"
            run_cmd(cmd)
        if is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} openjdk-jdk-8 maven gradle", )
        if is_macos():
            run_cmd("brew cask uninstall adoptopenjdk8")
        if is_centos_series():
            pass


def _add_subparser_openjdk(subparsers):
    add_subparser(subparsers, "OpenJDK8", func=openjdk8, aliases=["jdk8"])


def sdkman(**kwargs):
    """ Install sdkman.
    https://sdkman.io/install
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd("""curl -s https://get.sdkman.io | bash""")
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_sdkman(subparsers):
    add_subparser(subparsers, "sdkman", func=sdkman, aliases=[])


def yapf(**kwargs):
    """Install Google's yapf (for formatting Python scripts).
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f"{args.pip} install {args.user_s} yapf")
    if args.config:
        if args.dst_dir:
            src_file = BASE_DIR / "yapf/style.yapf"
            des_file = args.dst_dir / ".style.yapf"
            shutil.copy2(src_file, des_file)
            logging.info("%s is copied to %s.", src_file, des_file)
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall yapf")


def _yapf_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=None,
        help="The destination directory to copy the YAPF configuration file to.",
    )
    option_user(subparser)


def _add_subparser_yapf(subparsers):
    add_subparser(subparsers, "yapf", func=yapf, aliases=[], add_argument=_yapf_args)


def pylint(**kwargs):
    """Install pylint.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f"{args.pip} install {args.user_s} pylint")
    if args.config:
        src_file = BASE_DIR / "pylint/pylintrc"
        des_file = args.dst_dir / ".pylintrc"
        shutil.copy2(src_file, des_file)
        logging.info("%s is copied to %s.", src_file, des_file)
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall pylint")


def _pylint_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the pylint configuration file to.",
    )
    option_user(subparser)


def _add_subparser_pylint(subparsers):
    add_subparser(
        subparsers, "pylint", func=pylint, aliases=[], add_argument=_pylint_args
    )


def nodejs(**kwargs):
    """Install nodejs and npm.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            cmd = f"""apt-get install {args.yes_s} nodejs npm"""
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(["nodejs"])
        if is_centos_series():
            run_cmd(f"yum install {args.yes_s} nodejs")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} nodejs")
        if is_macos():
            run_cmd("brew uninstall nodejs")
        if is_centos_series():
            run_cmd("yum remove nodejs")


def _add_subparser_nodejs(subparsers):
    add_subparser(subparsers, "NodeJS", func=nodejs, aliases=["node"])


def ipython(**kwargs):
    """Install IPython for Python 3.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args.user_s} ipython"
        run_cmd(cmd)
    if args.config:
        src_dir = BASE_DIR / "ipython"
        dst_dir = args.profile_dir / "profile_default"
        (dst_dir / "startup").mkdir(mode=0o755, parents=True, exist_ok=True)
        shutil.copy2(src_dir / "ipython_config.py", dst_dir)
        shutil.copy2(src_dir / "startup.ipy", dst_dir / "startup")
        logging.info(
            "%s is copied to the directory %s.", src_dir / "ipython_config.py", dst_dir
        )
        logging.info(
            "%s is copied to the directory %s.", src_dir / "startup.ipy",
            dst_dir / "startup"
        )
    if args.uninstall:
        pass


def _ipython_args(subparser):
    subparser.add_argument(
        "--profile-dir",
        dest="profile_dir",
        type=Path,
        default=HOME / ".ipython",
        help="The directory for storing IPython configuration files.",
    )


def _add_subparser_ipython(subparsers):
    add_subparser(
        subparsers,
        "IPython",
        func=ipython,
        aliases=["ipy"],
        add_argument=_ipython_args,
    )


def python3(**kwargs):
    """Install and configure Python 3.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            cmd = f"apt-get install {args.yes_s} python3 python3-dev python3-pip python3-setuptools python3-venv"
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(["python3"])
        if is_centos_series():
            run_cmd(f"yum install {args.yes_s} python3 python3-devel python3-pip", )
            run_cmd(f"{args.pip} install {args.user_s} setuptools")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            cmd = f"""apt-get purge {args.yes_s} \
                python3 python3-dev python3-setuptools python3-pip python3-venv"""
            run_cmd(cmd)
        if is_macos():
            run_cmd("brew uninstall python3")
        if is_centos_series():
            run_cmd("yum remove python3")


def _add_subparser_python3(subparsers):
    add_subparser(
        subparsers,
        "Python3",
        func=python3,
        aliases=["py3", "py", "python"],
        add_argument=option_user
    )


def poetry(**kwargs):
    """Install and configure Python poetry.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | {args.python}"
        if args.version:
            cmd += f" - --version {args.version}"
        run_cmd(cmd)
    poetry_bin = HOME / ".poetry/bin/poetry"
    if args.config:
        # symbolic link
        desfile = BIN_DIR / "poetry"
        try:
            desfile.unlink()
        except FileNotFoundError:
            pass
        desfile.symlink_to(poetry_bin)
        logging.info("Symbolic link %s pointing to %s is created.", desfile, poetry_bin)
        # make poetry always create virtual environment in the root directory of the project
        run_cmd(f"{poetry_bin} config virtualenvs.in-project true")
        logging.info(
            "Python poetry has been configured to create virtual environments inside projects!"
        )
        # bash completion
        if args.bash_completion:
            if is_linux():
                cmd = f"{poetry_bin} completions bash | tee /etc/bash_completion.d/poetry.bash-completion > /dev/null"
                run_cmd(cmd)
                return
            if is_macos():
                cmd = f"{poetry_bin} completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion"
                run_cmd(cmd)
            logging.info("Bash completion is enabled for poetry.")
    if args.uninstall:
        run_cmd(f"{poetry_bin} self:uninstall")


def _poetry_args(subparser):
    subparser.add_argument(
        "-b",
        "--bash-completion",
        dest="bash_completion",
        action="store_true",
        help="Configure Bash completion for poetry as well."
    )
    subparser.add_argument(
        "-v",
        "--version",
        dest="version",
        default="",
        help="The version of Python Poetry to install."
    )


def _add_subparser_poetry(subparsers):
    add_subparser(
        subparsers, "Poetry", func=poetry, aliases=["pt"], add_argument=_poetry_args
    )


def pyjnius(**kwargs):
    """Install pyjnius for calling Java from Python.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args.user} Cython pyjnius"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_pyjnius(subparsers):
    add_subparser(
        subparsers, "pyjnius", func=pyjnius, aliases=["pyj"], add_argument=option_user
    )


def rustup(**kwargs):
    """Install rustup which is the version management tool for Rust.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = "rustup self uninstall"
        run_cmd(cmd)


def _add_subparser_rustup(subparsers):
    add_subparser(subparsers, "rustup", func=rustup)


def rust(**kwargs):
    """Install the Rust programming language (rustc and cargo) 
        (to system-wide locations using apt-get instead of to ~/.cargo using rustup).
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            cmd = f"apt-get install {args.yes_s} cmake rustc cargo"
            run_cmd(cmd)
        if is_centos_series():
            cmd = f"yum install {args.yes_s} cmake rustc cargo"
            run_cmd(cmd)
        if is_macos():
            brew_install_safe(["cmake", "rustc", "cargo"])
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            cmd = f"apt-get purge {args.yes_s} rustc cargo"
            run_cmd(cmd)
        if is_centos_series():
            run_cmd("yum remove rustc cargo")
        if is_macos():
            cmd = "brew uninstall rustc cargo"
            run_cmd(cmd)


def _add_subparser_rust(subparsers):
    add_subparser(subparsers, "rust", func=rust)


def rustpython(**kwargs):
    """Install and configure RustPython.
    """
    rust(**kwargs)
    args = namespace(kwargs)
    if args.install:
        cmd = "cargo install rustpython"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = "cargo uninstall rustpython"
        run_cmd(cmd)


def _add_subparser_rustpython(subparsers):
    add_subparser(subparsers, "RustPython", func=rustpython, aliases=["rustpy"])


def _git_ignore(args: Namespace) -> None:
    """Insert patterns to ingore into .gitignore in the current directory.
    """
    if not args.language:
        return
    srcfile = BASE_DIR / f"git/gitignore_{args.language}"
    dstfile = args.dst_dir / ".gitignore"
    mode = "a" if args.append else "w"
    with dstfile.open(mode) as fout:
        fout.write(srcfile.read_text())
    msg = f"%s is {'appended into' if mode == 'a' else 'copied to'} %s."
    logging.info(msg, srcfile, dstfile)


def git(**kwargs) -> None:
    """Install and configure Git.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args.yes_s} git git-lfs")
        elif is_macos():
            brew_install_safe(["git", "git-lfs", "bash-completion@2"])
        elif is_centos_series():
            run_cmd("yum install git")
        run_cmd("git lfs install")
    if args.uninstall:
        run_cmd("git lfs uninstall")
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} git git-lfs")
        elif is_macos():
            run_cmd("brew uninstall git git-lfs")
        elif is_centos_series():
            run_cmd("yum remove git")
    if args.config:
        ssh_client(config=True)
        gitconfig = HOME / ".gitconfig"
        # try to remove the file to avoid dead symbolic link problem
        remove_file_safe(gitconfig)
        shutil.copy2(BASE_DIR / "git/gitconfig", gitconfig)
        logging.info("%s is copied to %s", BASE_DIR / "git/gitconfig", gitconfig)
        if is_macos():
            file = "/usr/local/etc/bash_completion.d/git-completion.bash"
            bashrc = f"\n# Git completion\n[ -f {file} ] &&  . {file}"
            with (HOME / ".bash_profile").open("a") as fout:
                fout.write(bashrc)
            logging.info("Bash completion is enabled for Git.")
    _git_ignore(args)
    if "proxy" in kwargs and args.proxy:
        run_cmd(f"git config --global http.proxy {args.proxy}")
        run_cmd(f"git config --global https.proxy {args.proxy}")


def _git_args(subparser):
    subparser.add_argument(
        "--proxy",
        dest="proxy",
        default="",
        help="Configure Git to use the specified proxy."
    )
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        type=Path,
        default=Path(),
        help="The destination directory to copy the YAPF configuration file to.",
    )
    subparser.add_argument(
        "-p",
        "--python",
        dest="language",
        action="store_const",
        const="python",
        default="",
        help="Gitignore patterns for Python developing."
    )
    subparser.add_argument(
        "-j",
        "--java",
        dest="java",
        action="store_const",
        const="java",
        help="Gitignore patterns for Java developing."
    )
    subparser.add_argument(
        "-a",
        "--append",
        dest="append",
        action="store_true",
        help="Append patterns to ignore into .gitignore rather than overwrite it."
    )


def _add_subparser_git(subparsers):
    add_subparser(subparsers, "Git", func=git, add_argument=_git_args)


def antlr(**kwargs):
    """Install and configure Antrl4.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args.yes_s} antlr4")
        elif is_macos():
            brew_install_safe(["antlr4"])
        elif is_centos_series():
            run_cmd("yum install antlr")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} antlr4")
        elif is_macos():
            run_cmd("brew uninstall antlr4")
        elif is_centos_series():
            run_cmd("yum remove antlr")


def _add_subparser_antlr(subparsers):
    add_subparser(subparsers, "ANTLR", func=antlr)


def jpype1(**kwargs):
    """Install the Python package JPype.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args.user_s} JPype1"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall JPype1"
        run_cmd(cmd)


def _add_subparser_jpype1(subparsers):
    add_subparser(
        subparsers,
        "JPype1",
        func=jpype1,
        aliases=["jpype", "jp"],
        add_argument=option_user
    )


def deno(**kwargs):
    args = namespace(kwargs)
    if args.install:
        cmd = "curl -fsSL https://deno.land/x/install/install.sh | sh"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_deno(subparsers):
    add_subparser(subparsers, "Deno", func=deno, aliases=[])


def sphinx(**kwargs):
    args = namespace(kwargs)
    if args.install:
        cmd = "{args.pip} install {args.user_s} sphinx sphinx-autodoc-typehints"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = "{args.pip} uninstall sphinx sphinx-autodoc-typehints"
        run_cmd(cmd)


def _add_subparser_sphinx(subparsers):
    add_subparser(subparsers, "sphinx", func=sphinx, aliases=[])
