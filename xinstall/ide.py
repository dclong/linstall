"""Install IDE related tools.
"""
from typing import Union
from pathlib import Path
from argparse import Namespace
#import logging
import os
import shutil
import re
from .utils import (
    USER, HOME, BASE_DIR, BIN_DIR, LOCAL_DIR, is_debian_series, is_fedora_series,
    update_apt_source, brew_install_safe, is_macos, run_cmd, add_subparser,
    intellij_idea_plugin, option_pip_bundle
)


def vim(args) -> None:
    """Install Vim.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} vim vim-nox")
        elif is_macos():
            brew_install_safe(["vim"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install {args.yes_s} vim-enhanced")
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} vim vim-nox")
        elif is_macos():
            run_cmd("brew uninstall vim")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove vim")
    if args.config:
        pass


def _add_subparser_vim(subparsers) -> None:
    add_subparser(subparsers, "Vim", func=vim)


def neovim(args) -> None:
    """Install NeoVim.
    """
    if args.ppa and is_debian_series():
        args.install = True
        run_cmd(f"{args.prefix} add-apt-repository -y ppa:neovim-ppa/unstable")
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} neovim")
        elif is_macos():
            brew_install_safe(["neovim"])
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum install neovim")
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} neovim")
        elif is_macos():
            run_cmd("brew uninstall neovim")
        elif is_fedora_series():
            run_cmd(f"{args.prefix} yum remove neovim")
    if args.config:
        pass


def _neovim_args(subparser) -> None:
    subparser.add_argument(
        "--ppa",
        dest="ppa",
        action="store_true",
        help="Install the unstable version of NeoVim from PPA."
    )


def _add_subparser_neovim(subparsers) -> None:
    add_subparser(
        subparsers, "NeoVim", func=neovim, aliases=["nvim"], add_argument=_neovim_args
    )




def bash_lsp(args) -> None:
    """Install Bash Language Server for SpaceVim.
    """
    if args.install:
        cmd = f"{args.prefix} npm install -g bash-language-server"
        run_cmd(cmd)
    if args.config:
        toml = HOME / ".SpaceVim.d/init.toml"
        with toml.open("r") as fin:
            lines = [
                '  "sh",' if re.search(r"^\s*#\s*(\"|')sh(\"|'),\s*$", line) else line
                for line in fin
            ]
        with toml.open("w") as fout:
            fout.writelines(lines)
    if args.uninstall:
        cmd = f"{args.prefix} npm uninstall bash-language-server"
        run_cmd(cmd)


def _add_subparser_bash_lsp(subparsers) -> None:
    add_subparser(subparsers, "Bash LSP", func=bash_lsp, aliases=["blsp"])


def ideavim(args) -> None:
    """Install IdeaVim for IntelliJ.
    """
    if args.config:
        shutil.copy2(BASE_DIR / "ideavim/ideavimrc", HOME / ".ideavimrc")


def _add_subparser_ideavim(subparsers) -> None:
    add_subparser(subparsers, "IdeaVim", func=ideavim, aliases=["ivim"])


def intellij_idea(args) -> None:
    """Install IntelliJ IDEA.
    """
    if args.install:
        if is_debian_series():
            update_apt_source(prefix=args.prefix)
            des_dir = f"{LOCAL_DIR}/share/ide/idea"
            executable = f"{BIN_DIR}/idea"
            if USER == "root":
                des_dir = "/opt/idea"
                executable = "/opt/idea/bin/idea.sh"
            cmd = f"""{args.prefix} apt-get install -y ubuntu-make \
                && umake ide idea {des_dir} \
                && ln -s {des_dir}/bin/idea.sh {executable}"""
            run_cmd(cmd)
        elif is_macos():
            run_cmd("brew cask install intellij-idea-ce")
        elif is_fedora_series():
            pass
    if args.uninstall:
        if is_debian_series():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} intellij-idea-ce")
        elif is_macos():
            run_cmd("brew cask uninstall intellij-idea-ce")
        elif is_fedora_series():
            pass
    if args.config:
        pass


def intellij_idea_scala(args) -> None:
    """Install the Scala plugin for IntelliJ IDEA Community Edition.
    """
    url = "http://plugins.jetbrains.com/files/1347/73157/scala-intellij-bin-2019.3.17.zip"
    intellij_idea_plugin(version=args.version, url=url)


def _add_subparser_intellij_idea_scala(subparsers) -> None:
    add_subparser(
        subparsers, "IntelliJ IDEA", func=intellij_idea, aliases=["intellij", "idea"]
    )


