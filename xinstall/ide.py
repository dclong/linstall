from typing import Union
import os
import shutil
import re
from .utils import USER, HOME, BASE_DIR, BIN_DIR, LOCAL_DIR, is_ubuntu_debian, is_centos_series, is_linux, is_fedora, update_apt_source, brew_install_safe, is_macos, run_cmd, namespace, add_subparser, intellij_idea_plugin


def vim(**kwargs):
    """Install Vim.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} vim vim-nox',
            )
        elif is_macos():
            brew_install_safe(['vim'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install {args._yes_s} vim-enhanced')
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} vim vim-nox')
        elif is_macos():
            run_cmd(f'brew uninstall vim')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove vim')
    if args.config:
        pass


def neovim(**kwargs):
    """Install NeoVim.
    """
    args = namespace(kwargs)
    if args.ppa and is_ubuntu_debian():
        args.install = True
        run_cmd(f'{args.sudo_s} add-apt-repository -y ppa:neovim-ppa/stable')
        update_apt_source()
    if args.install:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} neovim')
        elif is_macos():
            brew_install_safe(['neovim'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install neovim')
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} neovim')
        elif is_macos():
            run_cmd(f'brew uninstall neovim')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove neovim')
    if args.config:
        pass


def _neovim_args(subparser):
    subparser.add_argument(
        "--ppa",
        dest="ppa",
        action="store_true",
        help="Install the latest version of NeoVim from PPA."
    )


def add_subparser_neovim(subparsers):
    add_subparser(
        subparsers, "NeoVim", aliases=["nvim"], add_argument=_neovim_args
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


def _svim_gen_config():
    """Generate init.toml for SpaceVim if it does not exist.
    """
    des_dir = HOME / ".SpaceVim.d"
    os.makedirs(des_dir, exist_ok=True)
    if not (des_dir / "init.toml").is_file():
        shutil.copy2(BASE_DIR / "SpaceVim/init.toml", des_dir)


def spacevim(**kwargs):
    """Install and configure SpaceVim.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f"curl -sLf https://spacevim.org/install.sh | bash")
        if shutil.which("nvim"):
            run_cmd(f'nvim --headless +"call dein#install()" +qall')
        cmd = f"{args.pip} install --user python-language-server[all] pyls-mypy"
        # {args.sudo_s} npm install -g bash-language-server javascript-typescript-langserver
        run_cmd(cmd)
    if args.uninstall:
        run_cmd(
            f"curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall",
        )
    if args.config:
        _svim_gen_config()
    _svim_true_color(args.true_colors)


def _spacevim_args(subparser):
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


def add_subparser_spacevim(subparsers):
    add_subparser(
        subparsers, "SpaceVim", aliases=["svim"], add_argument=_spacevim_args
    )
    

def bash_lsp(**kwargs):
    """Install Bash Language Server.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.sudo_s} npm install -g bash-language-server"
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
        cmd = f"{args.sudo_s} npm uninstall bash-language-server"
        run_cmd(cmd)



def ideavim(**kwargs):
    """Install IdeaVim for IntelliJ.
    """
    args = namespace(kwargs)
    if args.config:
        shutil.copy2(BASE_DIR / 'ideavim/ideavimrc', HOME / '.ideavimrc')


def intellij_idea(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            des_dir = f"{LOCAL_DIR}/share/ide/idea"
            executable = f"{BIN_DIR}/idea"
            if USER == "root":
                des_dir = "/opt/idea"
                executable = "/opt/idea/bin/idea.sh"
            cmd = f"""{args.sudo_s} apt-get install -y ubuntu-make \
                && umake ide idea {des_dir} \
                && ln -s {des_dir}/bin/idea.sh {executable}"""
            run_cmd(cmd)
        elif is_macos():
            run_cmd(f'brew cask install intellij-idea-ce')
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} intellij-idea-ce',
            )
        elif is_macos():
            run_cmd(f'brew cask uninstall intellij-idea-ce')
        elif is_centos_series():
            pass
    if args.config:
        pass


def visual_studio_code(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} vscode')
        elif is_macos():
            run_cmd(f'brew cask install visual-studio-code')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install vscode')
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} vscode')
        elif is_macos():
            run_cmd(f'brew cask uninstall visual-studio-code')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove vscode')
    if args.config:
        src_file = f'{BASE_DIR}/vscode/settings.json'
        dst_dir = f'{HOME}/.config/Code/User/'
        if is_macos():
            dst_dir = '{HOME}/Library/Application Support/Code/User/'
        os.makedirs(dst_dir, exist_ok=True)
        os.symlink(src_file, dst_dir, target_is_directory=True)
        run_cmd(f'ln -svf {src_file} {dst_dir}')


def intellij_idea_scala(**kwargs):
    """Install the Scala plugin for IntelliJ IDEA Community Edition.
    """
    args = namespace(kwargs)
    url = "http://plugins.jetbrains.com/files/1347/73157/scala-intellij-bin-2019.3.17.zip"
    intellij_idea_plugin(version=args.version, url=url)
