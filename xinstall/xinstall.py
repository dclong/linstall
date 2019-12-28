#!/usr/bin/env python3
"""Easy installation and configuration of Linux/Mac/Windows apps.
"""
import sys
import os
from typing import Union, Dict
import shutil
import tempfile
from pathlib import Path
import re
from argparse import Namespace
import logging
from . import utils
from .utils import (
    USER,
    HOME,
    run_cmd,
    update_apt_source,
    brew_install_safe,
    remove_file_safe,
    is_win,
    is_linux,
    is_ubuntu_debian,
    is_macos,
    is_fedora,
    is_centos_series,
    intellij_idea_plugin,
)
USER_ID = os.getuid()
GROUP_ID = os.getgid()
FILE = Path(__file__).resolve()
BASE_DIR = FILE.parent / 'data'
LOCAL_DIR = HOME / '.local'
BIN_DIR = LOCAL_DIR / 'bin'
BIN_DIR.mkdir(0o700, parents=True, exist_ok=True)
__version__ = "0.3.6"


def _namespace(dic: Dict) -> Namespace:
    dic.setdefault('sudo', False)
    dic.setdefault('yes', False)
    dic['sudo_s'] = 'sudo' if dic['sudo'] else ''
    dic['_sudo_s'] = '--sudo' if dic['sudo'] else ''
    dic['_yes_s'] = '--yes' if dic['yes'] else ''
    return Namespace(**dic)


def coreutils(**kwargs):
    """Install CoreUtils.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} coreutils')
        elif is_macos():
            brew_install_safe('coreutils')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install coreutils')
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} coreutils')
        elif is_macos():
            run_cmd(f'brew uninstall coreutils')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove coreutils')
    if args.config:
        if is_macos():
            cmd = f'''export PATH=/usr/local/opt/findutils/libexec/gnubin:"$PATH" \
                && export MANPATH=/usr/local/opt/findutils/libexec/gnuman:"$MANPATH"
                '''
            run_cmd(cmd)


# ------------------------- command-line utils related -------------------------
def shell_utils(**kwargs):
    """Install Shell-related utils.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} bash-completion command-not-found man-db',
            )
        elif is_macos():
            brew_install_safe(['bash-completion@2', 'man-db'])
        elif is_centos_series():
            run_cmd(
                f'{args.sudo_s} yum install bash-completion command-not-found man-db',
            )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} bash-completion command-not-found man-db',
            )
        elif is_macos():
            run_cmd(f'brew uninstall bash-completion man-db')
        elif is_centos_series():
            run_cmd(
                f'{args.sudo_s} yum remove bash-completion command-not-found man-db',
            )
    if args.config:
        pass


def change_shell(**kwargs):
    """Change the default shell.
    """
    args = _namespace(kwargs)
    if is_linux():
        pass
    elif is_macos():
        run_cmd(f'chsh -s {args.shell}')


def homebrew(**kwargs):
    """Install Homebrew.
    """
    args = _namespace(kwargs)
    if args.dep:
        args.install = True
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} build-essential curl file git',
            )
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum groupinstall "Development Tools"')
            run_cmd(f'{args.sudo_s} yum install curl file git')
            if is_fedora():
                run_cmd(f'{args.sudo_s} yum install libxcrypt-compat')
    cmd_brew = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"'
    if args.install:
        run_cmd(cmd_brew)
    if args.config:
        if is_linux():
            dirs = [f'{HOME}/.linuxbrew', '/home/linuxbrew/.linuxbrew']
            paths = [f'{dir_}/bin/brew' for dir_ in dirs if os.path.isdir(dir_)]
            if paths:
                brew = paths[-1]
                profiles = [f'{HOME}/.bash_profile', f'{HOME}/.profile']
                for profile in profiles:
                    run_cmd(f'{brew} shellenv >> {profile}')
            else:
                sys.exit('Homebrew is not installed!')
    if args.uninstall:
        if is_ubuntu_debian():
            pass
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def hyper(**kwargs):
    """Install the hyper.js terminal.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            #!{args.sudo_s} apt-get install {args._yes_s} hyper
        elif is_macos():
            run_cmd(f'brew cask install hyper')
        elif is_centos_series():
            #!sudo yum install hyper
            pass
    if args.config:
        run_cmd(f'hyper i hypercwd')
        run_cmd(f'hyper i hyper-search')
        run_cmd(f'hyper i hyper-pane')
        run_cmd(f'hyper i hyperpower')
        path = f'{HOME}/.hyper.js'
        #if os.path.exists(path):
        #    os.remove(path)
        shutil.copy2(os.path.join(BASE_DIR, 'hyper/hyper.js'), path)

    if args.uninstall:
        if is_ubuntu_debian():
            #!{args.sudo_s} apt-get purge hyper
            pass
        elif is_macos():
            run_cmd(f'brew cask uninstall hyper')
        elif is_centos_series():
            #!sudo yum remove hyper
            pass


def openinterminal(**kwargs):
    """Install openinterminal.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_macos():
            run_cmd(f"brew cask install openinterminal")
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd(f"brew cask uninstall openinterminal")


def xonsh(**kwargs):
    """Install xonsh, a Python based shell.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f"{args.pip} install --user xonsh")
    if args.config:
        src = f"{BASE_DIR}/xonsh/xonshrc"
        dst = HOME / ".xonshrc"
        if dst.exists():
            dst.unlink()
        shutil.copy2(src, dst)
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall xonsh")


def bash_it(**kwargs):
    """Install Bash-it, a community Bash framework.
    For more details, please refer to https://github.com/Bash-it/bash-it#installation.
    """
    args = _namespace(kwargs)
    if args.install:
        cmd = f'''git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it && \
                ~/.bash_it/install.sh --silent
                '''
        run_cmd(cmd)
    if args.config:
        profile = '.bashrc' if is_linux() else '.bash_profile'
        with (HOME / profile).open('a') as fout:
            fout.write(f'\n# PATH\nexport PATH={BIN_DIR}:$PATH')
    if args.uninstall:
        run_cmd('~/.bash_it/uninstall.sh')
        shutil.rmtree(HOME / '.bash_it')


def bash_completion(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} bash-completion',
            )
        elif is_macos():
            brew_install_safe(['bash-completion@2'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install bash-completion')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge bash-completion')
        elif is_macos():
            run_cmd(f'brew uninstall bash-completion')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove bash-completion')


def wajig(**kwargs) -> None:
    args = _namespace(kwargs)
    if not is_ubuntu_debian():
        return
    if args.install:
        update_apt_source()
        run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} wajig')
    if args.config:
        pass
    if args.proxy:
        cmd = f'''echo '\nAcquire::http::Proxy "{args.proxy}";\nAcquire::https::Proxy "{args.proxy}";' | {args.sudo_s} tee -a /etc/apt/apt.conf'''
        run_cmd(cmd)
    if args.uninstall:
        run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} wajig')


def exa(**kwargs):
    """Install exa which is an Rust-implemented alternative to ls.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} cargo install --root /usr/local/ exa')
        elif is_macos():
            brew_install_safe(['exa'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} cargo install --root /usr/local/ exa')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} cargo uninstall --root /usr/local/ exa')
        elif is_macos():
            run_cmd(f'brew uninstall exa')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} cargo uninstall --root /usr/local/ exa')


def osquery(**kwargs):
    """Install osquery for Linux admin.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            cmd = f'''{args.sudo_s} apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B \
                    && {args.sudo_s} add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main' \
                    && {args.sudo_s} apt-get update {args._yes_s} \
                    && {args.sudo_s} apt-get {args._yes_s} install osquery
                '''
            run_cmd(cmd)
        elif is_macos():
            brew_install_safe(['osquery'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install osquery')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} osquery')
        elif is_macos():
            run_cmd(f'brew uninstall osquery')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove osquery')


# ------------------------- vim related -------------------------
def vim(**kwargs):
    """Install Vim.
    """
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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


def ideavim(**kwargs):
    """Install IdeaVim for IntelliJ.
    """
    args = _namespace(kwargs)
    if args.config:
        shutil.copy2(BASE_DIR / 'ideavim/ideavimrc', HOME / '.ideavimrc')


# ------------------------- coding tools related -------------------------
def git(**kwargs) -> None:
    """Install and configure Git.
    """
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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


def docker(**kwargs):
    """Install and configure Docker container.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} docker.io docker-compose',
            )
        elif is_macos():
            brew_install_safe(
                [
                    'docker', 'docker-compose', 'bash-completion@2',
                    'docker-completion', 'docker-compose-completion'
                ]
            )
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install docker docker-compose')
    if args.config:
        run_cmd('gpasswd -a $(id -un) docker')
        logging.warning(
            'Please logout and then login to make the group "docker" effective!'
        )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} docker docker-compose',
            )
        elif is_macos():
            run_cmd(
                f'brew uninstall docker docker-completion docker-compose docker-compose-completion',
            )
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove docker docker-compose')


def kubernetes(**kwargs):
    """Install and configure kubernetes command-line interface.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | {args.sudo_s} apt-key add -',
            )
            run_cmd(
                f'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | {args.sudo_s} tee -a /etc/apt/sources.list.d/kubernetes.list',
            )
            update_apt_source(seconds=-1E10)
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} kubectl')
        elif is_macos():
            brew_install_safe(['kubernetes-cli'])
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} kubectl')
        elif is_macos():
            run_cmd(f'brew uninstall kubectl')
        elif is_centos_series():
            pass


def _minikube_linux(sudo: bool, yes: bool = True):
    run_cmd(
        f'''curl -L https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 -o /tmp/minikube-linux-amd64 \
            && {'sudo' if sudo else ''} apt-get install {yes} /tmp/minikube-linux-amd64 /usr/local/bin/minikube''',
    )
    print('VT-x/AMD-v virtualization must be enabled in BIOS.')


def minikube(**kwargs):
    args = _namespace(kwargs)
    virtualbox(**kwargs)
    kubernetes(**kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(seconds=-1E10)
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_macos():
            run_cmd(f'brew cask install minikube')
        elif is_centos_series():
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_win():
            run_cmd(f'choco install minikube')
            print('VT-x/AMD-v virtualization must be enabled in BIOS.')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} rm /usr/local/bin/minikube')
        elif is_macos():
            run_cmd(f'brew cask uninstall minikube')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} rm /usr/local/bin/minikube')


# ------------------------- programming languages -------------------------
def cargo(**kwargs):
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'''curl -s https://get.sdkman.io | bash''')
    if args.config:
        pass
    if args.uninstall:
        pass


def yapf(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'{args.pip} install --user {args._yes_s} yapf')
    if args.config:
        shutil.copy2(
            os.path.join(BASE_DIR, 'yapf/style.yapf'),
            os.path.join(args.dst_dir, '.style.yapf')
        )
    if args.uninstall:
        run_cmd(f'{args.pip} uninstall {args._yes_s} yapf')


def xinstall(**kwargs):
    """Install xonsh, a Python based shell.
    """
    args = _namespace(kwargs)
    if args.install:
        url = 'https://github.com/dclong/xinstall'
        utils.install_py_github(
            url=url, sudo=args.sudo, sys=args.sys, pip=args.pip
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.sudo_s} {args.pip} uninstall xinstall")


def dsutil(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        url = 'https://github.com/dclong/dsutil'
        utils.install_py_github(url=url, pip=args.pip)
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f'{args.pip} uninstall {args._yes_s} dsutil')


def nodejs(**kwargs):
    args = _namespace(kwargs)
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


def bash_lsp(**kwargs):
    """Install Bash Language Server.
    """
    args = _namespace(kwargs)
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


def ipython3(**kwargs):
    """Install IPython for Python 3.
    """
    args = _namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user {args._yes_s} ipython"
        run_cmd(cmd)
    if args.config:
        run_cmd("{args.ipython} profile create")
        src_dir = BASE_DIR / "ipython"
        dst_dir = HOME / ".ipython/profile_default"
        shutil.copy2(src_dir / "ipython_config.py", dst_dir)
        shutil.copy2(src_dir / "startup.ipy", dst_dir / "startup")
    if args.uninstall:
        pass


def python3(**kwargs):
    """Install and configure Python 3.
    """
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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


# ------------------------- JupyterLab kernels -------------------------
def nbdime(**kwargs):
    """Install and configure nbdime for comparing difference of notebooks.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'{args.pip} install --user nbdime')
    if args.uninstall:
        run_cmd(f'{args.pip} uninstall nbdime')
    if args.config:
        run_cmd(f'nbdime config-git --enable --global')


def itypescript(**kwargs):
    """Install and configure the ITypeScript kernel.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'{args.sudo_s} npm install -g --unsafe-perm itypescript')
        run_cmd(f'{args.sudo_s} its --ts-hide-undefined --install=global')
    if args.uninstall:
        run_cmd(f'{args.sudo_s} jupyter kernelspec uninstall typescript')
        run_cmd(f'{args.sudo_s} npm uninstall itypescript')
    if args.config:
        pass


def jupyterlab_lsp(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        cmd = '''{args.sudo_s} {args.pip} install --pre jupyter-lsp \
                && {args.sudo_s} {args.jupyter} labextension install @krassowski/jupyterlab-lsp \
                && {args.sudo_s} {args.pip} install python-language-server[all] pyls-mypy'''
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def beakerx(**kwargs):
    """Install/uninstall/configure the BeakerX kernels.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'{args.pip} install --user beakerx')
        run_cmd(f'{args.sudo_s} beakerx install')
        run_cmd(
            f'{args.sudo_s} jupyter labextension install @jupyter-widgets/jupyterlab-manager',
        )
        run_cmd(
            f'{args.sudo_s} jupyter labextension install beakerx-jupyterlab',
        )
    if args.uninstall:
        run_cmd(
            f'{args.sudo_s} jupyter labextension uninstall beakerx-jupyterlab',
        )
        run_cmd(
            f'{args.sudo_s} jupyter labextension uninstall @jupyter-widgets/jupyterlab-manager',
        )
        run_cmd(f'{args.sudo_s} beakerx uninstall')
        run_cmd(f'{args.pip} uninstall beakerx')
    if args.config:
        run_cmd(f'{args.sudo_s} chown -R {USER_ID}:{GROUP_ID} {HOME}')


def almond(**kwargs):
    """Install/uninstall/configure the Almond Scala kernel.
    """
    args = _namespace(kwargs)
    if args.almond_version is None:
        args.almond_version = '0.4.0'
    else:
        args.install = True
    if args.scala_version is None:
        args.scala_version = '2.12.12'
    else:
        args.install = True
    if args.install:
        coursier = os.path.join(BIN_DIR, 'coursier')
        almond = os.path.join(BIN_DIR, 'almond')
        run_cmd(f'curl -L -o {coursier} https://git.io/coursier-cli')
        run_cmd(f'chmod +x {coursier}')
        run_cmd(
            f'''{coursier} bootstrap -f -r jitpack -i user \
                -I user:sh.almond:scala-kernel-api_{args.scala_version}:{args.almond_version} \
                -o {almond} \
                sh.almond:scala-kernel_{args.scala_version}:{args.almond_version}''',
        )
        run_cmd(f'{args.sudo_s} {almond} --install --global --force')
    if args.config:
        pass


# ------------------------- web tools -------------------------
def ssh_server(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} openssh-server fail2ban',
            )
        elif is_macos():
            pass
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} openssh-server fail2ban',
            )
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def ssh_client(**kwargs) -> None:
    """Configure SSH client.
    :param kwargs: Keyword arguments.
    """
    args = _namespace(kwargs)
    if args.config:
        ssh_src = Path(f"/home_host/{USER}/.ssh")
        ssh_dst = HOME / ".ssh"
        if ssh_src.is_dir():
            # inside a Docker container, use .ssh from host
            try:
                shutil.rmtree(ssh_dst)
            except FileNotFoundError:
                pass
            shutil.copytree(ssh_src, ssh_dst)
        ssh_dst.mkdir(exist_ok=True)
        src = BASE_DIR / 'ssh/client/config'
        des = HOME / '.ssh/config'
        shutil.copy2(src, des)
        des.chmod(0o600)


def proxychains(**kwargs) -> None:
    """Install and configure ProxyChains.
    :param kwargs: Keyword arguments.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} proxychains4',
            )
        elif is_macos():
            brew_install_safe(['proxychains-ng'])
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install proxychains')
    if args.config:
        print('Configuring proxychains ...')
        des_dir = os.path.join(HOME, '.proxychains')
        os.makedirs(des_dir, exist_ok=True)
        shutil.copy2(
            os.path.join(BASE_DIR, 'proxychains/proxychains.conf'), des_dir
        )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge proxychains')
        elif is_macos():
            run_cmd(f'brew uninstall proxychains-ng')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove proxychains')


def dryscrape(**kwargs):
    """Install and configure dryscrape.
    """
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            cmd = f'''{args.sudo_s} apt-get install {args._yes_s} qt5-default libqt5webkit5-dev build-essential xvfb \
                && {args.pip} install --user dryscrape
                '''
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            pass
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def blogging(**kwargs):
    """Install blogging tools.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f"{args.pip} install --user pelican markdown")
        archives = HOME / "archives"
        archives.mkdir(0o700, exist_ok=True)
        blog = archives / "blog"
        if blog.is_dir():
            run_cmd(f"git -C {blog} pull origin master")
        else:
            run_cmd(f"git clone git@github.com:dclong/blog.git {blog}")
        cmd = f"""git -C {blog} submodule init && \
                git -C {blog} submodule update --recursive --remote
                """
        run_cmd(cmd)
    if args.config:
        (BIN_DIR / "blog").symlink_to(archives / "blog/main.py")
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall pelican markdown")


def download_tools(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} wget curl aria2',
            )
        elif is_macos():
            brew_install_safe(['wget', 'curl', 'aria2'])
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} wget curl aria2',
            )
        elif is_macos():
            run_cmd(f'brew uninstall wget curl aria2')
        elif is_centos_series():
            pass


# ------------------------- IDE -------------------------
def intellij_idea(**kwargs):
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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


def install_py_github(**kwargs):
    args = _namespace(kwargs)
    utils.install_py_github(
        url=args.url, sudo=args.sudo, sys=args.sys, pip=args.pip
    )


def virtualbox(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} virtualbox-qt',
            )
        elif is_macos():
            run_cmd(f'brew cask install virtualbox virtualbox-extension-pack')
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} virtualbox-qt',
            )
        elif is_macos():
            run_cmd(
                f'brew cask uninstall virtualbox virtualbox-extension-pack',
            )
        elif is_centos_series():
            pass
    if args.config:
        pass


def version(**kwargs):
    print(__version__)


def intellij_idea_scala(**kwargs):
    """Install the Scala plugin for IntelliJ IDEA Community Edition.
    """
    args = _namespace(kwargs)
    url = "http://plugins.jetbrains.com/files/1347/73157/scala-intellij-bin-2019.3.17.zip"
    intellij_idea_plugin(version=args.version, url=url)


def nomachine(**kwargs):
    """Install NoMachine.
    """
    args = _namespace(kwargs)
    if args.install:
        ver = args.version[:args.version.rindex(".")]
        if is_ubuntu_debian():
            url = f"https://download.nomachine.com/download/{ver}/Linux/nomachine_{args.version}_amd64.deb"
            with tempfile.TemporaryDirectory() as tempdir:
                file = Path(tempdir) / "nomachine.deb"
                cmd = f"curl -sSL {url} -o {file} && dpkg -i {file}"
                run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def pyjnius(**kwargs):
    """Install pyjnius for calling Java from Python.
    """
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install pyspark findspark optimuspyspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall pyspark findspark optimuspyspark"
        run_cmd(cmd)


def evcxr_jupyter(**kwargs):
    """Install the evcxr Rust kernel for Jupyter/Lab server.
    """
    args = _namespace(kwargs)
    if args.install:
        cmd = f"""{args.sudo_s} apt-get install {args._yes_s} cmake cargo \
            && cargo install --force evcxr_jupyter \
            && {HOME}/.cargo/bin/evcxr_jupyter --install
            """
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"""{HOME}/.cargo/bin/evcxr_jupyter --uninstall \
            && cargo uninstall evcxr_jupyter
            """
        run_cmd(cmd)


def rust(**kwargs):
    """Install the Rust programming language.
    """
    args = _namespace(kwargs)
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
    args = _namespace(kwargs)
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


def kaggle(**kwargs):
    """Insert the Python package kaggle.
    """
    args = _namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user kaggle"
        run_cmd(cmd)
    if args.config:
        home_host = Path("/home_host/dclong/")
        kaggle_home_host = home_host / ".kaggele"
        kaggle_home = HOME / ".kaggele"
        if home_host.is_dir():
            kaggle_home_host.mkdir(exist_ok=True)
            kaggle_home.symlink_to(kaggle_home_host)
        else:
            kaggle_home.mkdir(exist_ok=True)
    if args.uninstall:
        pass


def lightgbm(**kwargs):
    """Insert the Python package kaggle.
    """
    args = _namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user lightgmb graphviz"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass
