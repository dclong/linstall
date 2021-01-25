"""Install IDE related tools.
"""
from typing import Union
#import logging
import os
import shutil
import re
from .utils import (
    USER, HOME, BASE_DIR, BIN_DIR, LOCAL_DIR, is_ubuntu_debian, is_centos_series,
    update_apt_source, brew_install_safe, is_macos, run_cmd, add_subparser,
    intellij_idea_plugin, option_pip_bundle
)


def vim(args) -> None:
    """Install Vim.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} vim vim-nox")
        elif is_macos():
            brew_install_safe(["vim"])
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install {args.yes_s} vim-enhanced")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} vim vim-nox")
        elif is_macos():
            run_cmd("brew uninstall vim")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove vim")
    if args.config:
        pass


def _add_subparser_vim(subparsers) -> None:
    add_subparser(subparsers, "Vim", func=vim)


def neovim(args) -> None:
    """Install NeoVim.
    """
    if args.ppa and is_ubuntu_debian():
        args.install = True
        run_cmd(f"{args.prefix} add-apt-repository -y ppa:neovim-ppa/unstable")
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} neovim")
        elif is_macos():
            brew_install_safe(["neovim"])
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install neovim")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} neovim")
        elif is_macos():
            run_cmd("brew uninstall neovim")
        elif is_centos_series():
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


def _svim_true_color(true_color: Union[bool, None]) -> None:
    """Enable/disable true color for SpaceVim.
    """
    if true_color is None:
        return
    file = HOME / ".SpaceVim.d/init.toml"
    if not file.is_file():
        _svim_gen_config()
    with file.open() as fin:
        lines = fin.readlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith("enable_guicolors"):
            if true_color:
                lines[idx] = line.replace("false", "true")
            else:
                lines[idx] = line.replace("true", "false")
    with file.open("w") as fout:
        fout.writelines(lines)


def _svim_gen_config() -> None:
    """Generate init.toml for SpaceVim if it does not exist.
    """
    des_dir = HOME / ".SpaceVim.d"
    os.makedirs(des_dir, exist_ok=True)
    if not (des_dir / "init.toml").is_file():
        shutil.copy2(BASE_DIR / "SpaceVim/init.toml", des_dir)


def spacevim(args) -> None:
    """Install and configure SpaceVim.
    """
    if args.install:
        run_cmd("curl -sLf https://spacevim.org/install.sh | bash")
        if shutil.which("nvim"):
            run_cmd('nvim --headless +"call dein#install()" +qall')
        if not args.no_lsp:
            cmd = f"{args.pip} install {args.user_s} {args.pip_option} python-language-server[all] pyls-mypy"
            # npm install -g bash-language-server javascript-typescript-langserver
            run_cmd(cmd)
    if args.uninstall:
        run_cmd("curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall")
    if args.config:
        _svim_gen_config()
        _svim_true_color(args.true_colors)
        _svim_filetype_shiftwidth()


def _svim_filetype_shiftwidth():
    vimrc = HOME / ".SpaceVim.d/vimrc"
    with vimrc.open("a") as fout:
        fout.write("autocmd FileType yaml set shiftwidth=2")


def _spacevim_args(subparser) -> None:
    subparser.add_argument(
        "--enable-true-colors",
        dest="true_colors",
        action="store_true",
        default=None,
        help="enable true color (default true) for SpaceVim."
    )
    subparser.add_argument(
        "--disable-true-colors",
        dest="true_colors",
        action="store_false",
        help="disable true color (default true) for SpaceVim."
    )
    subparser.add_argument(
        "--no-lsp",
        dest="no_lsp",
        action="store_true",
        help="disable true color (default true) for SpaceVim."
    )
    option_pip_bundle(subparser)


def _add_subparser_spacevim(subparsers) -> None:
    add_subparser(
        subparsers,
        "SpaceVim",
        func=spacevim,
        aliases=["svim"],
        add_argument=_spacevim_args
    )


def bash_lsp(args) -> None:
    """Install Bash Language Server.
    """
    if args.install:
        cmd = f"{args.prefix} npm install -g bash-language-server"
        run_cmd(cmd)
    if args.config:
        _svim_gen_config()
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
        if is_ubuntu_debian():
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
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} intellij-idea-ce")
        elif is_macos():
            run_cmd("brew cask uninstall intellij-idea-ce")
        elif is_centos_series():
            pass
    if args.config:
        pass


def visual_studio_code(args) -> None:
    """Install Visual Studio Code.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} vscode")
        elif is_macos():
            run_cmd("brew cask install visual-studio-code")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install vscode")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} vscode")
        elif is_macos():
            run_cmd("brew cask uninstall visual-studio-code")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove vscode")
    if args.config:
        src_file = f"{BASE_DIR}/vscode/settings.json"
        if not args.dst_dir:
            args.dst_dir = f"{HOME}/.config/Code/User/"
            if is_macos():
                args.dst_dir = f"{HOME}/Library/Application Support/Code/User/"
        os.makedirs(args.dst_dir, exist_ok=True)
        shutil.copy2(src_file, args.dst_dir)


def _visual_studio_code_args(subparser) -> None:
    subparser.add_argument(
        "-d",
        "--destination-dir",
        "--dst-dir",
        dest="dst_dir",
        default="",
        help="Enable true color (default true) for SpaceVim."
    )
    option_pip_bundle(subparser)


def _add_subparser_visual_studio_code(subparsers) -> None:
    add_subparser(
        subparsers,
        "Visual Studio Code",
        func=visual_studio_code,
        aliases=["vscode", "code"],
        add_argument=_visual_studio_code_args
    )


def intellij_idea_scala(args) -> None:
    """Install the Scala plugin for IntelliJ IDEA Community Edition.
    """
    url = "http://plugins.jetbrains.com/files/1347/73157/scala-intellij-bin-2019.3.17.zip"
    intellij_idea_plugin(version=args.version, url=url)


def _add_subparser_intellij_idea_scala(subparsers) -> None:
    add_subparser(
        subparsers, "IntelliJ IDEA", func=intellij_idea, aliases=["intellij", "idea"]
    )


def _add_subparser_ide(subparsers):
    _add_subparser_vim(subparsers)
    _add_subparser_neovim(subparsers)
    _add_subparser_spacevim(subparsers)
    _add_subparser_ideavim(subparsers)
    _add_subparser_visual_studio_code(subparsers)
    _add_subparser_intellij_idea_scala(subparsers)
    _add_subparser_bash_lsp(subparsers)

