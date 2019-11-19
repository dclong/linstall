#!/usr/bin/env python3
"""Easy installation and configuration of Linux/Mac/Windows apps.
"""
import sys
import os
from typing import Union, Dict
import shutil
from pathlib import Path
import urllib.request
from argparse import Namespace
import getpass
import logging
from .utils import (
    HOME,
    run_cmd,
    update_apt_source,
    brew_install_safe,
    remove_file_safe,
    install_py_github,
    is_win,
    is_linux,
    is_ubuntu_debian,
    is_macos,
    is_fedora,
    is_centos_series,
)
USER = getpass.getuser()
USER_ID = os.getuid()
GROUP_ID = os.getgid()
FILE = Path(__file__).resolve()
BASE_DIR = FILE.parent / 'data'
BIN_DIR = HOME / '.local/bin'
BIN_DIR.mkdir(0o700, parents=True, exist_ok=True)


def _namespace(dic: Dict) -> Namespace:
    dic['sudo'] = 'sudo' if dic['sudo'] else ''
    dic['yes'] = '--yes' if dic['yes'] else ''
    return Namespace(**dic)


def map_keys(**kwargs):
    args = _namespace(kwargs)
    # TODO
    # reset key mappings
    # setxkbmap -option


def coreutils(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(sudo=args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} coreutils',
                shell=True,
            )
        elif is_macos():
            brew_install_safe('coreutils')
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install coreutils', shell=True)
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} coreutils',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall coreutils', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove coreutils', shell=True)
    if args.config:
        if is_macos():
            cmd = f'''export PATH=/usr/local/opt/findutils/libexec/gnubin:"$PATH" \
                && export MANPATH=/usr/local/opt/findutils/libexec/gnuman:"$MANPATH"
                '''
            run_cmd(cmd, shell=True)


# ------------------------- command-line utils related -------------------------
def shell_utils(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} bash-completion command-not-found man-db',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['bash-completion@2', 'man-db'])
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} yum install bash-completion command-not-found man-db',
                shell=True,
            )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} bash-completion command-not-found man-db',
                shell=True,
            )
        elif is_macos():
            run_cmd(
                f'brew uninstall bash-completion man-db',
                shell=True,
            )
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} yum remove bash-completion command-not-found man-db',
                shell=True,
            )
    if args.config:
        pass


def proxy_env(**kwargs):
    args = _namespace(kwargs)
    cmd = 'export http_proxy=http://10.135.227.47:80 && export https_proxy=http://10.135.227.47:80'
    run_cmd(cmd, shell=True)


def change_shell(**kwargs):
    args = _namespace(kwargs)
    if is_linux():
        pass
    elif is_macos():
        run_cmd(f'chsh -s {args.shell}', shell=True)


def homebrew(**kwargs):
    args = _namespace(kwargs)
    if args.dep:
        args.install = True
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} build-essential curl file git',
                shell=True,
            )
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} yum groupinstall "Development Tools"',
                shell=True,
            )
            run_cmd(f'{args.sudo} yum install curl file git', shell=True)
            if is_fedora():
                run_cmd(
                    f'{args.sudo} yum install libxcrypt-compat',
                    shell=True,
                )
    cmd_brew = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"'
    if args.install:
        run_cmd(cmd_brew, shell=True)
    if args.config:
        if is_linux():
            dirs = [f'{HOME}/.linuxbrew', '/home/linuxbrew/.linuxbrew']
            paths = [f'{dir_}/bin/brew' for dir_ in dirs if os.path.isdir(dir_)]
            if paths:
                brew = paths[-1]
                profiles = [f'{HOME}/.bash_profile', f'{HOME}/.profile']
                for profile in profiles:
                    run_cmd(f'{brew} shellenv >> {profile}', shell=True)
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
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            #!{args.sudo} apt-get install {args.yes} hyper
        elif is_macos():
            run_cmd(f'brew cask install hyper', shell=True)
        elif is_centos_series():
            #!sudo yum install hyper
            pass
    if args.config:
        run_cmd(f'hyper i hypercwd', shell=True)
        run_cmd(f'hyper i hyper-search', shell=True)
        run_cmd(f'hyper i hyper-pane', shell=True)
        run_cmd(f'hyper i hyperpower', shell=True)
        path = f'{HOME}/.hyper.js'
        #if os.path.exists(path):
        #    os.remove(path)
        shutil.copy2(os.path.join(BASE_DIR, 'hyper/hyper.js'), path)

    if args.uninstall:
        if is_ubuntu_debian():
            #!{args.sudo} apt-get purge hyper
            pass
        elif is_macos():
            run_cmd(f'brew cask uninstall hyper', shell=True)
        elif is_centos_series():
            #!sudo yum remove hyper
            pass


def openinterminal(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_macos():
            run_cmd(f'brew cask install openinterminal', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if is_macos():
            run_cmd(f'brew cask uninstall openinterminal', shell=True)


def xonsh(**kwargs):
    """Install xonsh, a Python based shell.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'pip3 install --user xonsh', shell=True)
    if args.config:
        src = f'{BASE_DIR}/xonsh/xonshrc'
        dst = HOME / '.xonshrc'
        if dst.exists():
            dst.unlink()
        shutil.copy2(src, dst)
    if args.uninstall:
        run_cmd(f'pip3 uninstall xonsh', shell=True)


def bash_it(**kwargs):
    """Install Bash-it, a community Bash framework.
    For more details, please refer to https://github.com/Bash-it/bash-it#installation.
    """
    args = _namespace(kwargs)
    if args.install:
        cmd = f'''git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it && \
                ~/.bash_it/install.sh --silent
                '''
        run_cmd(cmd, shell=True)
    if args.config:
        profile = '.bashrc' if is_linux() else '.bash_profile'
        with (HOME / profile).open('a') as fout:
            fout.write(f'\n# PATH\nexport PATH={BIN_DIR}:$PATH')
    if args.uninstall:
        run_cmd('~/.bash_it/uninstall.sh', shell=True)
        shutil.rmtree(HOME / '.bash_it')


def bash_completion(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} bash-completion',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['bash-completion@2'])
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install bash-completion', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge bash-completion',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall bash-completion', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove bash-completion', shell=True)


def wajig(**kwargs) -> None:
    args = _namespace(kwargs)
    if not is_ubuntu_debian():
        return
    if args.install:
        update_apt_source(args.sudo)
        run_cmd(
            f'{args.sudo} apt-get install {args.yes} wajig',
            shell=True,
        )
    if args.config:
        pass
    if args.proxy:
        cmd = f'''echo '\nAcquire::http::Proxy "{args.proxy}";\nAcquire::https::Proxy "{args.proxy}";' | {args.sudo} tee -a /etc/apt/apt.conf'''
        run_cmd(cmd, shell=True)
    if args.uninstall:
        run_cmd(f'{args.sudo} apt-get purge {args.yes} wajig', shell=True)


def exa(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} cargo install --root /usr/local/ exa',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['exa'])
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} cargo install --root /usr/local/ exa',
                shell=True,
            )
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} cargo uninstall --root /usr/local/ exa',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall exa', shell=True)
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} cargo uninstall --root /usr/local/ exa',
                shell=True,
            )


def osquery(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            cmd = f'''{args.sudo} apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B \
                    && {args.sudo} add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main' \
                    && {args.sudo} apt-get update {args.yes} \
                    && {args.sudo} apt-get {args.yes} install osquery
                '''
            run_cmd(cmd, shell=True)
        elif is_macos():
            brew_install_safe(['osquery'])
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install osquery', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} osquery',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall osquery', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove osquery', shell=True)


# ------------------------- vim related -------------------------
def vim(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} vim vim-nox',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['vim'])
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} yum install {args.yes} vim-enhanced',
                shell=True,
            )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} vim vim-nox',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall vim', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove vim', shell=True)
    if args.config:
        pass


def neovim(**kwargs):
    args = _namespace(kwargs)
    if args.ppa and is_ubuntu_debian():
        args.install = True
        run_cmd(
            f'{args.sudo} add-apt-repository -y ppa:neovim-ppa/stable',
            shell=True,
        )
        update_apt_source(args.sudo)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} neovim',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['neovim'])
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install neovim', shell=True)
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} neovim',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall neovim', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove neovim', shell=True)
    if args.config:
        pass


def _svim_true_color(true_color: Union[bool, None]) -> None:
    # TODO: use the toml module to help you parse the file??
    # I'm not sure whether it is feasible ...
    if true_color is None:
        return
    file = HOME / '.SpaceVim.d/init.toml'
    if not file.is_file():
        _svim_gen_config()
    with file.open() as fin:
        lines = fin.readlines()
    for idx, line in enumerate(lines):
        if line.strip().startswith('enable_guicolors'):
            if true_color:
                lines[idx] = line.replace('false', 'true')
            else:
                lines[idx] = line.replace('true', 'false')
    with file.open('w') as fout:
        fout.writelines(lines)


def _svim_gen_config():
    des_dir = HOME / '.SpaceVim.d'
    os.makedirs(des_dir, exist_ok=True)
    shutil.copy2(os.path.join(BASE_DIR, 'SpaceVim/init.toml'), des_dir)


def spacevim(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        run_cmd(
            f'curl -sLf https://spacevim.org/install.sh | bash',
            shell=True,
        )
        if shutil.which('nvim'):
            run_cmd(
                f'nvim --headless +"call dein#install()" +qall',
                shell=True,
            )
        cmd = f'''pip3 install --user python-language-server'''
        # {args.sudo} npm install -g bash-language-server javascript-typescript-langserver
        run_cmd(cmd, shell=True)
    if args.uninstall:
        run_cmd(
            f'curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall',
            shell=True,
        )
    if args.config:
        _svim_gen_config()
    _svim_true_color(args.true_colors)


def ideavim(**kwargs):
    args = _namespace(kwargs)
    if args.config:
        shutil.copy2(BASE_DIR / 'ideavim/ideavimrc', HOME / '.ideavimrc')


# ------------------------- coding tools related -------------------------
def git(**kwargs) -> None:
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} git git-lfs',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['git', 'git-lfs', 'bash-completion@2'])
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install git', shell=True)
        run_cmd('git lfs install', shell=True)
    if args.uninstall:
        run_cmd('git lfs uninstall', shell=True)
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} git git-lfs',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall git git-lfs', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove git', shell=True)
    if args.config:
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
        run_cmd(
            f'git config --global http.proxy {args.proxy}',
            shell=True,
        )
        run_cmd(
            f'git config --global https.proxy {args.proxy}',
            shell=True,
        )


def antlr(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} antlr4',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['antlr4'])
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install antlr', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} antlr4',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall antlr4', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove antlr', shell=True)


def docker(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} docker.io docker-compose',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(
                [
                    'docker', 'docker-compose', 'bash-completion@2',
                    'docker-completion', 'docker-compose-completion'
                ]
            )
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} yum install docker docker-compose',
                shell=True,
            )
    if args.config:
        run_cmd('gpasswd -a $(id -un) docker', shell=True)
        logging.warning(
            'Please logout and then login to make the group "docker" effective!'
        )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} docker docker-compose',
                shell=True,
            )
        elif is_macos():
            run_cmd(
                f'brew uninstall docker docker-completion docker-compose docker-compose-completion',
                shell=True,
            )
        elif is_centos_series():
            run_cmd(
                f'{args.sudo} yum remove docker docker-compose',
                shell=True,
            )


def kubernetes(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | {args.sudo} apt-key add -',
                shell=True,
            )
            run_cmd(
                f'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | {args.sudo} tee -a /etc/apt/sources.list.d/kubernetes.list',
                shell=True,
            )
            update_apt_source(sudo=args.sudo, seconds=-1E10)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} kubectl',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['kubernetes-cli'])
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} kubectl',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall kubectl', shell=True)
        elif is_centos_series():
            pass


def _minikube_linux(sudo: bool, yes: bool = True):
    run_cmd(
        f'''curl -L https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 -o /tmp/minikube-linux-amd64 \
            && {'sudo' if sudo else ''} apt-get install {yes} /tmp/minikube-linux-amd64 /usr/local/bin/minikube''',
        shell=True,
    )
    print('VT-x/AMD-v virtualization must be enabled in BIOS.')


def minikube(**kwargs):
    args = _namespace(kwargs)
    virtualbox(**kwargs)
    kubernetes(**kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(sudo=args.sudo, seconds=-1E10)
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_macos():
            run_cmd(f'brew cask install minikube', shell=True)
        elif is_centos_series():
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_win():
            run_cmd(f'choco install minikube', shell=True)
            print('VT-x/AMD-v virtualization must be enabled in BIOS.')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo} rm /usr/local/bin/minikube', shell=True)
        elif is_macos():
            run_cmd(f'brew cask uninstall minikube', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} rm /usr/local/bin/minikube', shell=True)


# ------------------------- programming languages -------------------------
def cargo(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} cargo',
                shell=True,
            )
        if is_macos():
            brew_install_safe(['cargo'])
        if is_centos_series():
            run_cmd(
                f'{args.sudo} yum install {args.yes} cargo',
                shell=True,
            )
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} cargo',
                shell=True,
            )
        if is_macos():
            run_cmd(f'brew uninstall cargo', shell=True)
        if is_centos_series():
            run_cmd(f'yum remove cargo', shell=True)


def openjdk8(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} openjdk-jdk-8 maven gradle',
                shell=True,
            )
        if is_macos():
            cmd = 'brew tap AdoptOpenJDK/openjdk && brew cask install adoptopenjdk8'
            run_cmd(cmd, shell=True)
        if is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} openjdk-jdk-8 maven gradle',
                shell=True,
            )
        if is_macos():
            run_cmd(f'brew cask uninstall adoptopenjdk8', shell=True)
        if is_centos_series():
            pass


def sdkman(**kwargs):
    """ Install sdkman.
    https://sdkman.io/install
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(
            f'''curl -s https://get.sdkman.io | bash''',
            shell=True,
        )
    if args.config:
        pass
    if args.uninstall:
        pass


def yapf(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        run_cmd(
            f'pip3 install --user {args.yes} yapf',
            shell=True,
        )
    if args.config:
        shutil.copy2(
            os.path.join(BASE_DIR, 'yapf/style.yapf'),
            os.path.join(args.dst_dir, '.style.yapf')
        )
    if args.uninstall:
        run_cmd(
            f'pip3 uninstall {args.yes} yapf',
            shell=True,
        )


def _dsutil_version() -> str:
    url = 'https://github.com/dclong/dsutil/releases/latest'
    req = urllib.request.urlopen(url)
    return Path(req.url).name


def dsutil(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        url = 'https://github.com/dclong/dsutil'
        install_py_github(url=url, yes=args.yes)
    if args.config:
        pass
    if args.uninstall:
        run_cmd(
            f'pip3 uninstall {args.yes} dsutil',
            shell=True,
        )


def nodejs(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            cmd = f'''{args.sudo} apt-get install {args.yes} nodejs npm'''
            run_cmd(cmd, shell=True)
        if is_macos():
            brew_install_safe(['nodejs'])
        if is_centos_series():
            run_cmd(
                f'{args.sudo} yum install {args.yes} nodejs',
                shell=True,
            )
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} nodejs',
                shell=True,
            )
        if is_macos():
            run_cmd(f'brew uninstall nodejs', shell=True)
        if is_centos_series():
            run_cmd(f'yum remove nodejs', shell=True)


def ipython3(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        cmd = f'pip3 install --user {args.yes} ipython'
        run_cmd(cmd, shell=True)
    if args.config:
        run_cmd('ipython3 profile create', shell=True)
        src_dir = BASE_DIR / 'ipython'
        dst_dir = HOME / '.ipython/profile_default'
        shutil.copy2(src_dir / 'ipython_config.py', dst_dir)
        shutil.copy2(src_dir / 'startup.ipy', dst_dir / 'startup')
    if args.uninstall:
        pass


def python3(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            cmd = f'''{args.sudo} apt-get install {args.yes} python3.7 python3-pip python3-setuptools && \
                    {args.sudo} ln -svf /usr/bin/python3.7 /usr/bin/python3
                    '''
            run_cmd(cmd, shell=True)
        if is_macos():
            brew_install_safe(['python3'])
        if is_centos_series():
            run_cmd(
                f'{args.sudo} yum install {args.yes} python34 python34-devel python34-pip',
                shell=True,
            )
            run_cmd(f'pip3.4 install --user setuptools', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} python3 python3-dev python3-setuptools python3-pip python3-venv',
                shell=True,
            )
        if is_macos():
            run_cmd(f'brew uninstall python3', shell=True)
        if is_centos_series():
            run_cmd(f'yum remove python3', shell=True)


def poetry(**kwargs):
    args = _namespace(kwargs)
    if args.python is None:
        args.python = 'python3'
    else:
        args.install = True
    if args.install:
        cmd = f'''curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | {args.python} && \
                {HOME / '.poetry/bin/poetry'} self:update --preview
                '''
        run_cmd(cmd, shell=True)
    if args.config:
        srcfile = HOME / '.poetry/bin/poetry'
        desfile = BIN_DIR / 'poetry'
        if desfile.exists():
            desfile.unlink()
        desfile.symlink_to(srcfile)
        if args.bash_completion:
            if is_linux():
                cmd = f'{HOME}/.poetry/bin/poetry completions bash | {args.sudo} tee /etc/bash_completion.d/poetry.bash-completion > /dev/null'
                run_cmd(cmd, shell=True)
                return
            if is_macos():
                cmd = f'$HOME/.poetry/bin/poetry completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion'
                run_cmd(cmd, shell=True)
    if args.uninstall:
        run_cmd(f'poetry self:uninstall', shell=True)


# ------------------------- JupyterLab kernels -------------------------
def nbdime(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'pip3 install --user nbdime', shell=True)
    if args.uninstall:
        run_cmd(f'pip3 uninstall nbdime', shell=True)
    if args.config:
        run_cmd(f'nbdime config-git --enable --global', shell=True)


def itypescript(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        run_cmd(
            f'{args.sudo} npm install -g --unsafe-perm itypescript',
            shell=True,
        )
        run_cmd(
            f'{args.sudo} its --ts-hide-undefined --install=global',
            shell=True,
        )
    if args.uninstall:
        run_cmd(
            f'{args.sudo} jupyter kernelspec uninstall typescript',
            shell=True,
        )
        run_cmd(f'{args.sudo} npm uninstall itypescript', shell=True)
    if args.config:
        pass


def jupyterlab_lsp(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        cmd = '''sudo pip3 install --pre jupyter-lsp \
                && sudo jupyter labextension install @krassowski/jupyterlab-lsp \
                && sudo pip3 install python-language-server[all]'''
        run_cmd(cmd, shell=True)
    if args.config:
        pass
    if args.uninstall:
        pass


def beakerx(**kwargs):
    """Install/uninstall/configure the BeakerX kernels.
    """
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'pip3 install --user beakerx', shell=True)
        run_cmd(f'{args.sudo} beakerx install', shell=True)
        run_cmd(
            f'{args.sudo} jupyter labextension install @jupyter-widgets/jupyterlab-manager',
            shell=True,
        )
        run_cmd(
            f'{args.sudo} jupyter labextension install beakerx-jupyterlab',
            shell=True,
        )
    if args.uninstall:
        run_cmd(
            f'{args.sudo} jupyter labextension uninstall beakerx-jupyterlab',
            shell=True,
        )
        run_cmd(
            f'{args.sudo} jupyter labextension uninstall @jupyter-widgets/jupyterlab-manager',
            shell=True,
        )
        run_cmd(f'{args.sudo} beakerx uninstall', shell=True)
        run_cmd(f'pip3 uninstall beakerx', shell=True)
    if args.config:
        run_cmd(
            f'{args.sudo} chown -R {USER_ID}:{GROUP_ID} {HOME}',
            shell=True,
        )


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
        run_cmd(
            f'curl -L -o {coursier} https://git.io/coursier-cli',
            shell=True,
        )
        run_cmd(f'chmod +x {coursier}', shell=True)
        run_cmd(
            f'''{coursier} bootstrap -f -r jitpack -i user \
                -I user:sh.almond:scala-kernel-api_{args.scala_version}:{args.almond_version} \
                -o {almond} \
                sh.almond:scala-kernel_{args.scala_version}:{args.almond_version}''',
            shell=True,
        )
        run_cmd(
            f'{args.sudo} {almond} --install --global --force',
            shell=True,
        )
    if args.config:
        pass


# ------------------------- web tools -------------------------
def ssh_server(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} openssh-server fail2ban',
                shell=True,
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
                f'{args.sudo} apt-get purge {args.yes} openssh-server fail2ban',
                shell=True,
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
        ssh = Path(f"/home_host/{USER}/.ssh")
        if ssh.is_dir():
            # inside a Docker container, use .ssh from host
            try:
                shutil.rmtree(HOME / ".ssh")
            except FileNotFoundError:
                pass
            shutil.copytree(ssh, HOME)
        (HOME / ".ssh").mkdir(exist_ok=True)
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
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} proxychains4',
                shell=True,
            )
        elif is_macos():
            brew_install_safe(['proxychains-ng'])
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install proxychains', shell=True)
    if args.config:
        print('Configuring proxychains ...')
        des_dir = os.path.join(HOME, '.proxychains')
        os.makedirs(des_dir, exist_ok=True)
        shutil.copy2(
            os.path.join(BASE_DIR, 'proxychains/proxychains.conf'), des_dir
        )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo} apt-get purge proxychains', shell=True)
        elif is_macos():
            run_cmd(f'brew uninstall proxychains-ng', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove proxychains', shell=True)


def dryscrape(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            cmd = f'''{args.sudo} apt-get install {args.yes} qt5-default libqt5webkit5-dev build-essential xvfb \
                && pip3 install --user dryscrape
                '''
            run_cmd(cmd, shell=True)
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
    args = _namespace(kwargs)
    if args.install:
        run_cmd(f'pip3 install --user pelican markdown', shell=True)
        archives = HOME / 'archives'
        archives.mkdir(0o700, exist_ok=True)
        blog = archives / 'blog'
        if blog.is_dir():
            run_cmd(f'git -C {blog} pull origin master', shell=True)
        else:
            run_cmd(
                f'git clone git@github.com:dclong/blog.git {archives}',
                shell=True
            )
        cmd = f'''git -C {blog} submodule init && \
                git -C {blog} submodule update --recursive --remote
                '''
        run_cmd(cmd, shell=True)
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f'pip3 uninstall pelican markdown', shell=True)


def download_tools(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} wget curl aria2',
                shell=True,
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
                f'{args.sudo} apt-get purge {args.yes} wget curl aria2',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew uninstall wget curl aria2', shell=True)
        elif is_centos_series():
            pass


# ------------------------- IDE -------------------------
def intellij_idea(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} add-apt-repository ppa:mmk2410/intellij-idea',
                shell=True,
            )
            update_apt_source(sudo=args.sudo, seconds=-1E10)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} intellij-idea-community',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew cask install intellij-idea-ce', shell=True)
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} intellij-idea-ce',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew cask uninstall intellij-idea-ce', shell=True)
        elif is_centos_series():
            pass
    if args.config:
        pass


def visual_studio_code(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(sudo=args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} vscode',
                shell=True,
            )
        elif is_macos():
            run_cmd(f'brew cask install visual-studio-code', shell=True)
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum install vscode', shell=True)
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} vscode',
                shell=True,
            )
        elif is_macos():
            run_cmd(
                f'brew cask uninstall visual-studio-code',
                shell=True,
            )
        elif is_centos_series():
            run_cmd(f'{args.sudo} yum remove vscode', shell=True)
    if args.config:
        src_file = f'{BASE_DIR}/vscode/settings.json'
        dst_dir = f'{HOME}/.config/Code/User/'
        if is_macos():
            dst_dir = '{HOME}/Library/Application Support/Code/User/'
        os.makedirs(dst_dir, exist_ok=True)
        os.symlink(src_file, dst_dir, target_is_directory=True)
        run_cmd(f'ln -svf {src_file} {dst_dir}', shell=True)


def virtualbox(**kwargs):
    args = _namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(sudo=args.sudo)
            run_cmd(
                f'{args.sudo} apt-get install {args.yes} virtualbox-qt',
                shell=True,
            )
        elif is_macos():
            run_cmd(
                f'brew cask install virtualbox virtualbox-extension-pack',
                shell=True,
            )
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo} apt-get purge {args.yes} virtualbox-qt',
                shell=True,
            )
        elif is_macos():
            run_cmd(
                f'brew cask uninstall virtualbox virtualbox-extension-pack',
                shell=True,
            )
        elif is_centos_series():
            pass
    if args.config:
        pass
