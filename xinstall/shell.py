"""Install shell (command-line) related tools.
"""
from pathlib import Path
import logging
import shutil
import sys
import os
import textwrap
from .utils import (
    HOME,
    BASE_DIR,
    BIN_DIR,
    is_ubuntu_debian,
    is_centos_series,
    is_linux,
    is_fedora,
    update_apt_source,
    brew_install_safe,
    is_macos,
    run_cmd,
    add_subparser,
    option_pip_bundle,
)


def _add_subparser_shell(subparsers):
    _add_subparser_coreutils(subparsers)
    _add_subparser_change_shell(subparsers)
    _add_subparser_shell_utils(subparsers)
    _add_subparser_bash_it(subparsers)
    _add_subparser_xonsh(subparsers)
    _add_subparser_homebrew(subparsers)
    _add_subparser_hyper(subparsers)
    _add_subparser_openinterminal(subparsers)
    _add_subparser_bash_complete(subparsers)
    _add_subparser_wajig(subparsers)
    _add_subparser_exa(subparsers)
    _add_subparser_osquery(subparsers)
    _add_subparser_dust(subparsers)


def coreutils(args) -> None:
    """Install CoreUtils.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} coreutils")
        elif is_macos():
            brew_install_safe("coreutils")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install coreutils")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} coreutils")
        elif is_macos():
            run_cmd("brew uninstall coreutils")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove coreutils")
    if args.config:
        if is_macos():
            cmd = """export PATH=/usr/local/opt/findutils/libexec/gnubin:"$PATH" \
                && export MANPATH=/usr/local/opt/findutils/libexec/gnuman:"$MANPATH"
                """
            run_cmd(cmd)
            logging.info("GNU paths are exported.")


def _add_subparser_coreutils(subparsers) -> None:
    add_subparser(subparsers, "CoreUtils", func=coreutils, aliases=["cu"])


def shell_utils(args) -> None:
    """Install Shell-related utils.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"""{args.prefix} apt-get install {args.yes_s} \
                    bash-completion command-not-found man-db""",
            )
        elif is_macos():
            brew_install_safe(["bash-completion@2", "man-db"])
        elif is_centos_series():
            run_cmd(
                f"{args.prefix} yum install bash-completion command-not-found man-db"
            )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f"""{args.prefix} apt-get purge {args.yes_s} \
                    bash-completion command-not-found man-db""",
            )
        elif is_macos():
            run_cmd("brew uninstall bash-completion man-db")
        elif is_centos_series():
            run_cmd(
                f"{args.prefix} yum remove bash-completion command-not-found man-db"
            )
    if args.config:
        pass


def _add_subparser_shell_utils(subparsers) -> None:
    add_subparser(
        subparsers,
        "Shell utils",
        func=shell_utils,
        aliases=["sh_utils", "shutils", "shu", "su"]
    )


def change_shell(args) -> None:
    """Change the default shell.
    """
    if is_linux():
        pass
    elif is_macos():
        run_cmd(f"{args.prefix} chsh -s {args.shell}")


def _change_shell_args(subparser) -> None:
    subparser.add_argument(
        "-s",
        "--shell",
        dest="shell",
        default="/bin/bash",
        help="the shell to change to."
    )


def _add_subparser_change_shell(subparsers) -> None:
    add_subparser(
        subparsers,
        "change shell",
        func=change_shell,
        aliases=["chsh", "cs"],
        add_argument=_change_shell_args
    )


def _homebrew_args(subparser) -> None:
    subparser.add_argument(
        "-d",
        "--install-deps",
        dest="dep",
        action="store_true",
        help="Whether to install dependencies."
    )


def homebrew(args) -> None:
    """Install Homebrew.
    """
    if args.dep:
        args.install = True
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"{args.prefix} apt-get install {args.yes_s} build-essential curl file git"
            )
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum groupinstall 'Development Tools'")
            run_cmd(f"{args.prefix} yum install curl file git")
            if is_fedora():
                run_cmd(f"{args.prefix} yum install libxcrypt-compat")
    url = "https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh"
    cmd_brew = f'sh -c "$(curl -fsSL {url})"'
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
                logging.info(
                    "Shell environment variables for Linuxbrew are inserted to %s.",
                    profiles
                )
            else:
                sys.exit("Homebrew is not installed!")
    if args.uninstall:
        if is_ubuntu_debian():
            pass
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def _add_subparser_homebrew(subparsers) -> None:
    add_subparser(
        subparsers,
        "Homebrew",
        func=homebrew,
        aliases=["brew"],
        add_argument=_homebrew_args
    )


def hyper(args) -> None:
    """Install the hyper.js terminal.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
        elif is_macos():
            run_cmd("brew cask install hyper")
        elif is_centos_series():
            #!yum install hyper
            pass
    if args.config:
        run_cmd("hyper i hypercwd")
        run_cmd("hyper i hyper-search")
        run_cmd("hyper i hyper-pane")
        run_cmd("hyper i hyperpower")
        logging.info(
            "Hyper plugins hypercwd, hyper-search, hyper-pane and hyperpower are installed."
        )
        path = f"{HOME}/.hyper.js"
        #if os.path.exists(path):
        #    os.remove(path)
        shutil.copy2(os.path.join(BASE_DIR, "hyper/hyper.js"), path)
        logging.info("%s is copied to %s.", BASE_DIR / "hyper/hyper.js", path)
    if args.uninstall:
        if is_ubuntu_debian():
            #!apt-get purge hyper
            pass
        elif is_macos():
            run_cmd("brew cask uninstall hyper")
        elif is_centos_series():
            #!yum remove hyper
            pass


def _add_subparser_hyper(subparsers) -> None:
    add_subparser(subparsers, "Hyper", func=hyper, aliases=["hp"])


def openinterminal(args) -> None:
    """Install openinterminal.
    """
    if args.install:
        if is_macos():
            run_cmd("brew cask install openinterminal")
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd("brew cask uninstall openinterminal")


def _add_subparser_openinterminal(subparsers) -> None:
    add_subparser(subparsers, "OpenInTerminal", func=openinterminal, aliases=["oit"])


def xonsh(args) -> None:
    """Install xonsh, a Python based shell.
    """
    if args.install:
        run_cmd(f"{args.pip} install {args.user_s} {args.pip_option} xonsh")
    if args.config:
        src = f"{BASE_DIR}/xonsh/xonshrc"
        dst = HOME / ".xonshrc"
        try:
            dst.unlink()
        except FileNotFoundError:
            pass
        shutil.copy2(src, dst)
        logging.info("%s is copied to %s.", src, dst)
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall xonsh")


def _xonsh_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_xonsh(subparsers) -> None:
    add_subparser(subparsers, "xonsh", func=xonsh, add_argument=_xonsh_args)


def bash_it(args) -> None:
    """Install Bash-it, a community Bash framework.
    For more details, please refer to https://github.com/Bash-it/bash-it#installation.
    """
    if args.install:
        dir_ = Path.home() / ".bash_it"
        try:
            dir_.unlink()
        except FileNotFoundError:
            pass
        cmd = f"""git clone --depth=1 https://github.com/Bash-it/bash-it.git {dir_} \
                && {dir_}/install.sh --silent -f
                """
        run_cmd(cmd)
    if args.config:
        bash = textwrap.dedent(
            f"""
            # PATH
            if [[ ! "$PATH" =~ (^{BIN_DIR}:)|(:{BIN_DIR}:)|(:{BIN_DIR}$) ]]; then
                export PATH={BIN_DIR}:$PATH
            fi
            """
        )
        profile = HOME / (".bashrc" if is_linux() else ".bash_profile")
        with profile.open("a") as fout:
            fout.write(bash)
        logging.info("'export PATH=%s:$PATH' is inserted into %s.", BIN_DIR, profile)
        if is_linux():
            bash = textwrap.dedent(
                """\
                # source in ~/.bashrc
                if [[ -f $HOME/.bashrc ]]; then
                    . $HOME/.bashrc
                fi
                """
            )
            with (HOME / ".bash_profile").open("w") as fout:
                fout.write(bash)
    if args.uninstall:
        run_cmd("~/.bash_it/uninstall.sh")
        shutil.rmtree(HOME / ".bash_it")


def _add_subparser_bash_it(subparsers) -> None:
    add_subparser(
        subparsers, "Bash-it", func=bash_it, aliases=["bashit", "shit", "bit"]
    )


def bash_completion(args) -> None:
    """Install and configure bash-complete.

    :param args:
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} bash-completion")
        elif is_macos():
            brew_install_safe(["bash-completion@2"])
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install bash-completion")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge bash-completion")
        elif is_macos():
            run_cmd("brew uninstall bash-completion")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove bash-completion")


def _add_subparser_bash_complete(subparsers) -> None:
    add_subparser(
        subparsers,
        "Bash completion",
        func=bash_completion,
        aliases=["completion", "comp", "cp"]
    )


def exa(args) -> None:
    """Install exa which is an Rust-implemented alternative to ls.
    """
    if args.install:
        if is_ubuntu_debian():
            run_cmd("cargo install --root /usr/local/ exa")
        elif is_macos():
            brew_install_safe(["exa"])
        elif is_centos_series():
            run_cmd("cargo install --root /usr/local/ exa")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd("cargo uninstall --root /usr/local/ exa")
        elif is_macos():
            run_cmd("brew uninstall exa")
        elif is_centos_series():
            run_cmd("cargo uninstall --root /usr/local/ exa")


def _add_subparser_exa(subparsers) -> None:
    add_subparser(subparsers, "exa", func=exa)


def osquery(args) -> None:
    """Install osquery for Linux admin.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            cmd = f"""{args.prefix} apt-get {args.yes_s} install dirmngr \
                    && {args.prefix} apt-key adv --keyserver keyserver.ubuntu.com \
                        --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B \
                    && {args.prefix} add-apt-repository \
                        "deb [arch=amd64] https://pkg.osquery.io/deb deb main" \
                    && {args.prefix} apt-get {args.yes_s} install osquery
                """
            run_cmd(cmd)
        elif is_macos():
            brew_install_safe(["osquery"])
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install osquery")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} osquery")
        elif is_macos():
            run_cmd("brew uninstall osquery")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove osquery")


def _add_subparser_osquery(subparsers) -> None:
    add_subparser(subparsers, "osquery", func=osquery, aliases=["osq"])


def wajig(args) -> None:
    """Install wajig.
    """
    if not is_ubuntu_debian():
        return
    if args.install:
        update_apt_source(prefix=args.prefix)
        run_cmd(f"{args.prefix} apt-get install {args.yes_s} wajig")
    if args.config:
        pass
    if args.proxy:
        cmd = f"""echo '\nAcquire::http::Proxy "{args.proxy}";\nAcquire::https::Proxy "{args.proxy}";' \
            | {args.prefix} tee -a /etc/apt/apt.conf"""
        run_cmd(cmd)
    if args.uninstall:
        run_cmd(f"{args.prefix} apt-get purge {args.yes_s} wajig")


def _wajig_args(subparser) -> None:
    subparser.add_argument(
        "-p",
        "--proxy",
        dest="proxy",
        default="",
        help="Configure apt to use the specified proxy."
    )


def _add_subparser_wajig(subparsers) -> None:
    add_subparser(
        subparsers, "Wajig", func=wajig, aliases=["wj"], add_argument=_wajig_args
    )


def dust(args) -> None:
    """Install dust which is du implemented in Rust.
    The cargo command must be available on the search path in order to install dust.
    """
    if args.install:
        if is_macos():
            run_cmd("brew install dust")
        else:
            run_cmd("cargo install du-dust")
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd("brew uninstall dust")
        else:
            run_cmd("cargo uninstall du-dust")


def _add_subparser_dust(subparsers) -> None:
    add_subparser(subparsers, "dust", func=dust, aliases=[])
