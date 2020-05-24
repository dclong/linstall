"""Install IDE related tools.
"""
from typing import Union
import os
import shutil
import re
from .utils import (
    USER,
    HOME,
    BASE_DIR,
    BIN_DIR,
    LOCAL_DIR,
    is_ubuntu_debian,
    is_centos_series,
    update_apt_source,
    brew_install_safe,
    is_macos,
    run_cmd,
    namespace,
    add_subparser,
    intellij_idea_plugin,
)


def vim(**kwargs) -> None:
    """Install Vim.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args.yes_s} vim vim-nox")
        elif is_macos():
            brew_install_safe(["vim"])
        elif is_centos_series():
            run_cmd(f"yum install {args.yes_s} vim-enhanced")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} vim vim-nox")
        elif is_macos():
            run_cmd("brew uninstall vim")
        elif is_centos_series():
            run_cmd("yum remove vim")
    if args.config:
        pass


def _add_subparser_vim(subparsers) -> None:
    add_subparser(subparsers, "Vim", func=vim)


def neovim(**kwargs) -> None:
    """Install NeoVim.
    """
    args = namespace(kwargs)
    if args.ppa and is_ubuntu_debian():
        args.install = True
        run_cmd("add-apt-repository -y ppa:neovim-ppa/stable")
        update_apt_source()
    if args.install:
        if is_ubuntu_debian():
            run_cmd(f"apt-get install {args.yes_s} neovim")
        elif is_macos():
            brew_install_safe(["neovim"])
        elif is_centos_series():
            run_cmd("yum install neovim")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} neovim")
        elif is_macos():
            run_cmd("brew uninstall neovim")
        elif is_centos_series():
            run_cmd("yum remove neovim")
    if args.config:
        pass


def _neovim_args(subparser) -> None:
    subparser.add_argument(
        "--ppa",
        dest="ppa",
        action="store_true",
        help="Install the latest version of NeoVim from PPA."
    )


def _add_subparser_neovim(subparsers) -> None:
    add_subparser(
        subparsers,
        "NeoVim",
        func=neovim,
        aliases=["nvim"],
        add_argument=_neovim_args
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


def spacevim(**kwargs) -> None:
    """Install and configure SpaceVim.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd("curl -sLf https://spacevim.org/install.sh | bash")
        if shutil.which("nvim"):
            run_cmd('nvim --headless +"call dein#install()" +qall')
        cmd = f"{args.pip} install --user python-language-server[all] pyls-mypy"
        # npm install -g bash-language-server javascript-typescript-langserver
        run_cmd(cmd)
    if args.uninstall:
        run_cmd(
            "curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall",
        )
    if args.config:
        _svim_gen_config()
    _svim_true_color(args.true_colors)


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


def _add_subparser_spacevim(subparsers) -> None:
    add_subparser(
        subparsers,
        "SpaceVim",
        func=spacevim,
        aliases=["svim"],
        add_argument=_spacevim_args
    )


def bash_lsp(**kwargs) -> None:
    """Install Bash Language Server.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = "npm install -g bash-language-server"
        run_cmd(cmd)
    if args.config:
        _svim_gen_config()
        toml = HOME / ".SpaceVim.d/init.toml"
        with toml.open("r") as fin:
            lines = [
                '  "sh",'
                if re.search(r"^\s*#\s*(\"|')sh(\"|'),\s*$", line) else line
                for line in fin
            ]
        with toml.open("w") as fout:
            fout.writelines(lines)
    if args.uninstall:
        cmd = "npm uninstall bash-language-server"
        run_cmd(cmd)


def _add_subparser_bash_lsp(subparsers) -> None:
    add_subparser(subparsers, "Bash LSP", func=bash_lsp, aliases=["blsp"])


def ideavim(**kwargs) -> None:
    """Install IdeaVim for IntelliJ.
    """
    args = namespace(kwargs)
    if args.config:
        shutil.copy2(BASE_DIR / "ideavim/ideavimrc", HOME / ".ideavimrc")


def _add_subparser_ideavim(subparsers) -> None:
    add_subparser(subparsers, "IdeaVim", func=ideavim, aliases=["ivim"])


def intellij_idea(**kwargs) -> None:
    """Install IntelliJ IDEA.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            des_dir = f"{LOCAL_DIR}/share/ide/idea"
            executable = f"{BIN_DIR}/idea"
            if USER == "root":
                des_dir = "/opt/idea"
                executable = "/opt/idea/bin/idea.sh"
            cmd = f"""apt-get install -y ubuntu-make \
                && umake ide idea {des_dir} \
                && ln -s {des_dir}/bin/idea.sh {executable}"""
            run_cmd(cmd)
        elif is_macos():
            run_cmd("brew cask install intellij-idea-ce")
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} intellij-idea-ce")
        elif is_macos():
            run_cmd("brew cask uninstall intellij-idea-ce")
        elif is_centos_series():
            pass
    if args.config:
        pass


def visual_studio_code(**kwargs) -> None:
    """Install Visual Studio Code.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f"apt-get install {args.yes_s} vscode")
        elif is_macos():
            run_cmd("brew cask install visual-studio-code")
        elif is_centos_series():
            run_cmd("yum install vscode")
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"apt-get purge {args.yes_s} vscode")
        elif is_macos():
            run_cmd("brew cask uninstall visual-studio-code")
        elif is_centos_series():
            run_cmd("yum remove vscode")
    if args.config:
        src_file = f"{BASE_DIR}/vscode/settings.json"
        dst_dir = f"{HOME}/.config/Code/User/"
        if is_macos():
            dst_dir = "{HOME}/Library/Application Support/Code/User/"
        os.makedirs(dst_dir, exist_ok=True)
        os.symlink(src_file, dst_dir, target_is_directory=True)
        run_cmd(f"ln -svf {src_file} {dst_dir}")


def _add_subparser_visual_studio_code(subparsers) -> None:
    add_subparser(
        subparsers,
        "Visual Studio Code",
        func=visual_studio_code,
        aliases=["vscode", "code"]
    )


def intellij_idea_scala(**kwargs) -> None:
    """Install the Scala plugin for IntelliJ IDEA Community Edition.
    """
    args = namespace(kwargs)
    url = "http://plugins.jetbrains.com/files/1347/73157/scala-intellij-bin-2019.3.17.zip"
    intellij_idea_plugin(version=args.version, url=url)


def _add_subparser_intellij_idea_scala(subparsers) -> None:
    add_subparser(
        subparsers,
        "IntelliJ IDEA",
        func=intellij_idea,
        aliases=["intellij", "idea"]
    )
