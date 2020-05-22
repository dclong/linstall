import logging
import shutil
import sys
import os
from .utils import HOME, BASE_DIR, BIN_DIR, is_ubuntu_debian, is_centos_series, is_linux, is_fedora, update_apt_source, brew_install_safe, is_macos, run_cmd, namespace, add_subparser


def coreutils(**kwargs):
    """Install CoreUtils.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args._yes_s} coreutils")
        elif is_macos():
            brew_install_safe("coreutils")
        elif is_centos_series():
            run_cmd(f"yum install coreutils")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args._yes_s} coreutils")
        elif is_macos():
            run_cmd(f"brew uninstall coreutils")
        elif is_centos_series():
            run_cmd(f"yum remove coreutils")
    if args.config:
        if is_macos():
            cmd = f"""export PATH=/usr/local/opt/findutils/libexec/gnubin:"$PATH" \
                && export MANPATH=/usr/local/opt/findutils/libexec/gnuman:"$MANPATH"
                """
            run_cmd(cmd)
            logging.info("GNU paths are exported.")


def _add_subparser_coreutils(subparsers):
    add_subparser(subparsers, "CoreUtils", func=coreutils, aliases=["cu"])


def shell_utils(**kwargs):
    """Install Shell-related utils.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f"apt-get install {args._yes_s} bash-completion command-not-found man-db",
            )
        elif is_macos():
            brew_install_safe(["bash-completion@2", "man-db"])
        elif is_centos_series():
            run_cmd(f"yum install bash-completion command-not-found man-db", )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f"apt-get purge {args._yes_s} bash-completion command-not-found man-db",
            )
        elif is_macos():
            run_cmd(f"brew uninstall bash-completion man-db")
        elif is_centos_series():
            run_cmd(f"yum remove bash-completion command-not-found man-db", )
    if args.config:
        pass


def _add_subparser_shell_utils(subparsers):
    add_subparser(
        subparsers,
        "Shell utils",
        func=shell_utils,
        aliases=["sh_utils", "shutils", "shu", "su"]
    )


def change_shell(**kwargs):
    """Change the default shell.
    """
    args = namespace(kwargs)
    if is_linux():
        pass
    elif is_macos():
        run_cmd(f"chsh -s {args.shell}")


def _change_shell_args(subparser):
    subparser.add_argument(
        "-s",
        "--shell",
        dest="shell",
        default="/bin/bash",
        help="the shell to change to."
    )


def _add_subparser_change_shell(subparsers):
    add_subparser(
        subparsers,
        "change shell",
        func="change_shell",
        aliases=["chsh", "cs"],
        add_argument=_change_shell_args
    )


def _homebrew_args(subparser):
    subparser.add_argument(
        "-d",
        "--install-deps",
        dest="dep",
        action="store_true",
        help="Whether to install dependencies."
    )


def homebrew(**kwargs):
    """Install Homebrew.
    """
    args = namespace(kwargs)
    if args.dep:
        args.install = True
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f"apt-get install {args._yes_s} build-essential curl file git",
            )
        elif is_centos_series():
            run_cmd(f'yum groupinstall "Development Tools"')
            run_cmd(f"yum install curl file git")
            if is_fedora():
                run_cmd(f"yum install libxcrypt-compat")
    cmd_brew = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"'
    if args.install:
        run_cmd(cmd_brew)
    if args.config:
        if is_linux():
            dirs = [f"{HOME}/.linuxbrew", "/home/linuxbrew/.linuxbrew"]
            paths = [f"{dir_}/bin/brew" for dir_ in dirs if os.path.isdir(dir_)]
            if paths:
                brew = paths[-1]
                profiles = [f"{HOME}/.bash_profile", f"{HOME}/.profile"]
                for profile in profiles:
                    run_cmd(f"{brew} shellenv >> {profile}")
                logging.info(f"Shell environment variables for Linuxbrew are inserted to {profiles}.")
            else:
                sys.exit("Homebrew is not installed!")
    if args.uninstall:
        if is_ubuntu_debian():
            pass
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def _add_subparser_homebrew(subparsers):
    add_subparser(
        subparsers,
        "Homebrew",
        func="homebrew",
        aliases=["brew"],
        add_argument=_homebrew_args
    )


def hyper(**kwargs):
    """Install the hyper.js terminal.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            #!apt-get install {args._yes_s} hyper
        elif is_macos():
            run_cmd(f"brew cask install hyper")
        elif is_centos_series():
            #!yum install hyper
            pass
    if args.config:
        run_cmd(f"hyper i hypercwd")
        run_cmd(f"hyper i hyper-search")
        run_cmd(f"hyper i hyper-pane")
        run_cmd(f"hyper i hyperpower")
        logging.info(f"Hyper plugins hypercwd, hyper-search, hyper-pane and hyperpower are installed.")
        path = f"{HOME}/.hyper.js"
        #if os.path.exists(path):
        #    os.remove(path)
        shutil.copy2(os.path.join(BASE_DIR, "hyper/hyper.js"), path)
        logging.info(f"{BASE_DIR / 'hyper/hyper.js'} is copied to {path}.")
    if args.uninstall:
        if is_ubuntu_debian():
            #!apt-get purge hyper
            pass
        elif is_macos():
            run_cmd(f"brew cask uninstall hyper")
        elif is_centos_series():
            #!yum remove hyper
            pass


def _add_subparser_hyper(subparsers):
    add_subparser(subparsers, "Hyper", func=hyper, aliases=["hp"])


def openinterminal(**kwargs):
    """Install openinterminal.
    """
    args = namespace(kwargs)
    if args.install:
        if is_macos():
            run_cmd(f"brew cask install openinterminal")
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd(f"brew cask uninstall openinterminal")


def _add_subparser_openinterminal(subparsers):
    add_subparser(
        subparsers, "OpenInTerminal", func=openinterminal, aliases=["oit"]
    )


def xonsh(**kwargs):
    """Install xonsh, a Python based shell.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f"{args.pip} install --user xonsh")
    if args.config:
        src = f"{BASE_DIR}/xonsh/xonshrc"
        dst = HOME / ".xonshrc"
        try:
            dst.unlink()
        except FileNotFoundError:
            pass
        shutil.copy2(src, dst)
        logging.info(f"{src} is copied to {dst}.")
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall xonsh")


def _add_subparser_xonsh(subparsers):
    add_subparser(subparsers, "xonsh", func=xonsh)


def bash_it(**kwargs):
    """Install Bash-it, a community Bash framework.
    For more details, please refer to https://github.com/Bash-it/bash-it#installation.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"""rm -rf ~/.bash_it \
                && git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it \
                && ~/.bash_it/install.sh --silent
                """
        run_cmd(cmd)
    if args.config:
        profile = ".bashrc" if is_linux() else ".bash_profile"
        with (HOME / profile).open("a") as fout:
            fout.write(f"\n# PATH\nexport PATH={BIN_DIR}:$PATH")
        logging.info(f"'export PATH={BIN_DIR}:$PATH' is inserted into {profile}.")
    if args.uninstall:
        run_cmd("~/.bash_it/uninstall.sh")
        shutil.rmtree(HOME / ".bash_it")


def _add_subparser_bash_it(subparsers):
    add_subparser(
        subparsers, "Bash-it", func=bash_it, aliases=["bashit", "shit", "bit"]
    )


def bash_completion(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args._yes_s} bash-completion", )
        elif is_macos():
            brew_install_safe(["bash-completion@2"])
        elif is_centos_series():
            run_cmd(f"yum install bash-completion")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge bash-completion")
        elif is_macos():
            run_cmd(f"brew uninstall bash-completion")
        elif is_centos_series():
            run_cmd(f"yum remove bash-completion")


def _add_subparser_bash_complete(subparsers):
    add_subparser(
        subparsers,
        "Bash completion",
        func=bash_completion,
        aliases=["completion", "comp", "cp"]
    )


def exa(**kwargs):
    """Install exa which is an Rust-implemented alternative to ls.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(f"cargo install --root /usr/local/ exa")
        elif is_macos():
            brew_install_safe(["exa"])
        elif is_centos_series():
            run_cmd(f"cargo install --root /usr/local/ exa")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"cargo uninstall --root /usr/local/ exa")
        elif is_macos():
            run_cmd(f"brew uninstall exa")
        elif is_centos_series():
            run_cmd(f"cargo uninstall --root /usr/local/ exa")


def _add_subparser_exa(subparsers):
    add_subparser(subparsers, "exa", func=exa)


def osquery(**kwargs):
    """Install osquery for Linux admin.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            cmd = f"""apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B \
                    && add-apt-repository "deb [arch=amd64] https://pkg.osquery.io/deb deb main" \
                    && apt-get update {args._yes_s} \
                    && apt-get {args._yes_s} install osquery
                """
            run_cmd(cmd)
        elif is_macos():
            brew_install_safe(["osquery"])
        elif is_centos_series():
            run_cmd(f"yum install osquery")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args._yes_s} osquery")
        elif is_macos():
            run_cmd(f"brew uninstall osquery")
        elif is_centos_series():
            run_cmd(f"yum remove osquery")


def _add_subparser_osquery(subparsers):
    add_subparser(subparsers, "osquery", func=osquery, aliases=["osq"])


def wajig(**kwargs) -> None:
    args = namespace(kwargs)
    if not is_ubuntu_debian():
        return
    if args.install:
        update_apt_source()
        run_cmd(f"apt-get install {args._yes_s} wajig")
    if args.config:
        pass
    if args.proxy:
        cmd = f"""echo '\nAcquire::http::Proxy "{args.proxy}";\nAcquire::https::Proxy "{args.proxy}";' | tee -a /etc/apt/apt.conf"""
        run_cmd(cmd)
    if args.uninstall:
        run_cmd(f"apt-get purge {args._yes_s} wajig")


def _wajig_args(subparser):
    subparser.add_argument(
        "-p",
        "--proxy",
        dest="proxy",
        default="",
        help="Configure apt to use the specified proxy."
    )


def _add_subparser_wajig(subparsers):
    add_subparser(
        subparsers,
        "Wajig",
        func=wajig,
        aliases=["wj"],
        add_argument=_wajig_args
    )
