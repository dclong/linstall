#!/usr/bin/env python3
import sys
import os
import json
import platform
import shutil
import tempfile
from pathlib import Path
import re
import subprocess as sp
from typing import Any, List, Sequence, Callable, Union
from argparse import ArgumentParser
import datetime
import logging

PLATFORM = platform.platform().lower()
USER_ID = os.getuid()
GROUP_ID = os.getgid()
PREFIX = '' if USER_ID == 0 or 'darwin' in PLATFORM else 'sudo'
HOME = Path.home()
FILE = Path(__file__).resolve()
BASE_DIR = FILE.parent
SETTINGS_FILE = HOME / '.linstall.json'
SETTINGS = {}
if os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE) as fin:
        SETTINGS = json.load(fin)
FORMAT = '%Y-%m-%d %H:%M:%S.%f'
BIN_DIR = HOME / '.local/bin'
BIN_DIR.mkdir(0o700, parents=True, exist_ok=True)
# create symbolic link of script at $HOME/.local/bin/linstall
LINSTALL = BIN_DIR / 'linstall'


def remove_file_safe(path: Path) -> None:
    """Remove a file or sybmolic link.
    :param path: The path to the file or symbolic link.
    """
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def run_cmd(cmd, shell):
    proc = sp.run(cmd, shell=shell, check=True)
    logging.info(proc.args)


def brew_install_safe(pkgs: Union[str, List]) -> None:
    if isinstance(pkgs, list):
        for pkg in pkgs:
            brew_install_safe(pkg)
        return
    proc = sp.run(f'brew ls --versions {pkgs}', shell=True, stdout=sp.PIPE)
    if not proc.stdout:
        run_cmd(f'brew install {pkgs}', shell=True)
    run_cmd(f'brew link {pkgs}', shell=True)


def parse_args(args=None, namespace=None):
    """Parse command-line arguments for the install/configuration util.
    """
    parser = ArgumentParser(
        description='Easy installation and configuration for Unix/Linux'
    )
    parser.add_argument(
        '-s',
        '--sudo',
        dest='prefix',
        default=PREFIX,
        action='store_const',
        const='sudo',
        help='Run commands using sudo.'
    )
    parser.add_argument(
        '--no-sudo',
        dest='prefix',
        action='store_const',
        const='',
        help='Run commands without using sudo.'
    )
    subparsers = parser.add_subparsers(dest='sub_cmd', help='Sub commands.')
    # ------------------------ linstall itself ------------------------------
    _add_subparser(subparsers, 'update', aliases=['pull', 'upd', 'pu'])
    # ------------------------ command-line tools ----------------------------
    _add_subparser(subparsers, 'CoreUtils', aliases=['cu'])
    _add_subparser(
        subparsers,
        'change shell',
        aliases=['chsh', 'cs'],
        add_argument=change_shell_args
    )
    _add_subparser(subparsers, 'proxy env', aliases=['proxy', 'penv', 'pe'])
    _add_subparser(
        subparsers, 'Shell utils', aliases=['sh_utils', 'shutils', 'shu', 'su']
    )
    _add_subparser(subparsers, 'Bash-it', aliases=['shit', 'bit'])
    _add_subparser(subparsers, 'xonsh')
    _add_subparser(
        subparsers, 'Homebrew', aliases=['brew'], add_argument=homebrew_args
    )
    _add_subparser(subparsers, 'Hyper', aliases=['hp'])
    _add_subparser(subparsers, 'OpenInTerminal', aliases=['oit'])
    _add_subparser(
        subparsers, 'Bash completion', aliases=['completion', 'comp', 'cp']
    )
    _add_subparser(subparsers, 'Wajig', aliases=['wj'], add_argument=wajig_args)
    _add_subparser(subparsers, 'exa')
    _add_subparser(subparsers, 'osquery', aliases=['osq'])
    # ------------------------ Vim ------------------------------
    _add_subparser(subparsers, 'Vim')
    _add_subparser(
        subparsers, 'NeoVim', aliases=['nvim'], add_argument=neovim_args
    )
    _add_subparser(
        subparsers, 'SpaceVim', aliases=['svim'], add_argument=spacevim_args
    )
    _add_subparser(subparsers, 'IdeaVim', aliases=['ivim'])
    #------------------------- development related  ------------------------------
    _add_subparser(subparsers, 'Git', add_argument=git_args)
    _add_subparser(subparsers, 'NodeJS', aliases=['node'])
    _add_subparser(subparsers, 'Python3', aliases=['py3'])
    _add_subparser(subparsers, 'IPython3', aliases=['ipy3'])
    _add_subparser(subparsers, 'yapf', aliases=[])
    _add_subparser(subparsers, 'OpenJDK8', aliases=['jdk8'])
    _add_subparser(
        subparsers, 'Poetry', aliases=['pt'], add_argument=poetry_args
    )
    _add_subparser(subparsers, 'Cargo', aliases=['cgo'])
    _add_subparser(subparsers, 'ANTLR')
    _add_subparser(subparsers, 'Docker', aliases=['dock', 'dk'])
    _add_subparser(subparsers, 'Kubernetes', aliases=['k8s'])
    _add_subparser(subparsers, 'Minikube', aliases=['mkb'])
    #------------------------- web related ------------------------------
    _add_subparser(subparsers, 'SSH server', aliases=['sshs'])
    _add_subparser(subparsers, 'SSH client', aliases=['sshc'])
    _add_subparser(subparsers, 'blogging', aliases=['blog'])
    _add_subparser(subparsers, 'ProxyChains', aliases=['pchains', 'pc'])
    _add_subparser(subparsers, 'dryscrape', aliases=[])
    _add_subparser(subparsers, 'download tools', aliases=['dl', 'dlt'])
    #------------------------- JupyterLab related ------------------------------
    _add_subparser(subparsers, 'BeakerX', aliases=['bkx', 'bk'])
    _add_subparser(
        subparsers, 'Almond', aliases=['al', 'amd'], add_argument=almond_args
    )
    _add_subparser(subparsers, 'iTypeScript', aliases=['its'])
    _add_subparser(subparsers, 'nbdime', aliases=['nbd'])
    #------------------------- IDEs ------------------------------
    _add_subparser(subparsers, 'Visual Studio Code', aliases=['vscode', 'code'])
    _add_subparser(
        subparsers, 'IntelliJ IDEA', aliases=['intellij', 'idea', 'ii']
    )
    #------------------------- misc applications ------------------------------
    _add_subparser(subparsers, 'VirtualBox', aliases=['vbox'])
    #--------------------------------------------------------
    return parser.parse_args(args=args, namespace=namespace)


def map_keys(args):
    # TODO
    # reset key mappings
    # setxkbmap -option
    pass


def update(args):
    os.chdir(BASE_DIR)
    run_cmd(f'git pull origin master', shell=True)


def _any_in_platform(keywords):
    return any(kwd in PLATFORM for kwd in keywords)


def _is_ubuntu_debian():
    dists = ('ubuntu', 'debian')
    return _any_in_platform(dists)


def _is_linux():
    dists = ('ubuntu', 'debian', 'centos', 'redhat', 'fedora')
    return _any_in_platform(dists)


def _is_centos_series():
    dists = ('centos', 'redhat', 'fedora')
    return _any_in_platform(dists)


def _is_fedora():
    dists = ('fedora', )
    return _any_in_platform(dists)


def _is_macos():
    dists = ('darwin', )
    return _any_in_platform(dists)


def coreutils(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} coreutils',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe('coreutils')
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install coreutils', shell=True)
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} coreutils',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall coreutils', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove coreutils', shell=True)
    if args.config:
        if _is_macos():
            cmd = f'''export PATH=/usr/local/opt/findutils/libexec/gnubin:"$PATH" \
                && export MANPATH=/usr/local/opt/findutils/libexec/gnuman:"$MANPATH"
                '''
            run_cmd(cmd, shell=True)


# ------------------------- command-line utils related -------------------------
def shell_utils(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} bash-completion command-not-found man-db',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['bash-completion@2', 'man-db'])
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install bash-completion command-not-found man-db',
                shell=True,
            )
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} bash-completion command-not-found man-db',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew uninstall bash-completion man-db',
                shell=True,
            )
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum remove bash-completion command-not-found man-db',
                shell=True,
            )
    if args.config:
        pass


def proxy_env(args):
    cmd = 'export http_proxy=http://10.135.227.47:80 && export https_proxy=http://10.135.227.47:80'
    run_cmd(cmd, shell=True)


def change_shell(args):
    if _is_linux():
        pass
    elif _is_macos():
        run_cmd(f'chsh -s {args.shell}', shell=True)


def change_shell_args(subparser):
    subparser.add_argument(
        '-s',
        '--shell',
        dest='shell',
        default='/bin/bash',
        help='the shell to change to.'
    )


def homebrew_args(subparser):
    subparser.add_argument(
        '-d',
        '--install-deps',
        dest='dep',
        action='store_true',
        help='Whether to install dependencies.'
    )


def homebrew(args):
    if args.dep:
        args.install = True
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} build-essential curl file git',
                shell=True,
            )
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum groupinstall "Development Tools"',
                shell=True,
            )
            run_cmd(
                f'{args.prefix} yum install curl file git', shell=True
            )
            if _is_fedora():
                run_cmd(
                    f'{args.prefix} yum install libxcrypt-compat',
                    shell=True,
                )
    cmd_brew = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"'
    if args.install:
        run_cmd(cmd_brew, shell=True)
    if args.config:
        if _is_linux():
            dirs = [f'{HOME}/.linuxbrew', '/home/linuxbrew/.linuxbrew']
            paths = [f'{dir_}/bin/brew' for dir_ in dirs if os.path.isdir(dir_)]
            if paths:
                brew = paths[-1]
                profiles = [f'{HOME}/.bash_profile', f'{HOME}/.profile']
                for profile in profiles:
                    run_cmd(
                        f'{brew} shellenv >> {profile}', shell=True
                    )
            else:
                sys.exit('Homebrew is not installed!')
    if args.uninstall:
        if _is_ubuntu_debian():
            pass
        elif _is_macos():
            pass
        elif _is_centos_series():
            pass


def hyper(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            #!{args.prefix} apt-get install {args.yes} hyper
            pass
        elif _is_macos():
            run_cmd(f'brew cask install hyper', shell=True)
        elif _is_centos_series():
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
        if _is_ubuntu_debian():
            #!{args.prefix} apt-get purge hyper
            pass
        elif _is_macos():
            run_cmd(f'brew cask uninstall hyper', shell=True)
        elif _is_centos_series():
            #!sudo yum remove hyper
            pass


def openinterminal(args):
    if args.install:
        if _is_macos():
            run_cmd(f'brew cask install openinterminal', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if _is_macos():
            run_cmd(
                f'brew cask uninstall openinterminal', shell=True)


def _copy_file(srcfile, dstfile):
    _remove_file(dstfile)
    shutil.copy2(srcfile, dstfile)


def _remove_file(path: str):
    if os.path.islink(path):
        os.unlink(path)
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        shutil.rmtree(path)


def xonsh(args):
    """Install xonsh, a Python based shell.
    """
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


def bash_it(args):
    """Install Bash-it, a community Bash framework.
    For more details, please refer to https://github.com/Bash-it/bash-it#installation.
    """
    if args.install:
        cmd = f'''git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it && \
                ~/.bash_it/install.sh --silent
                '''
        run_cmd(cmd, shell=True)
    if args.config:
        profile  = '.bashrc' if _is_linux() else '.bash_profile'
        with (HOME / profile).open('a') as fout:
            fout.write(f'\n# PATH\nexport PATH={BIN_DIR}:$PATH')
    if args.uninstall:
        run_cmd('~/.bash_it/uninstall.sh', shell=True)
        shutil.rmtree(HOME / '.bash_it')


def bash_completion(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} bash-completion',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['bash-completion@2'])
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install bash-completion', shell=True
            )
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge bash-completion',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall bash-completion', shell=True)
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum remove bash-completion', shell=True
            )


def wajig(args) -> None:
    if not _is_ubuntu_debian():
        return
    if args.install:
        _update_apt_source()
        run_cmd(
            f'{args.prefix} apt-get install {args.yes} wajig',
            shell=True,
        )
    if args.config:
        pass
    if args.proxy:
        cmd = f'''echo '\nAcquire::http::Proxy "{args.proxy}";\nAcquire::https::Proxy "{args.proxy}";' | {args.prefix} tee -a /etc/apt/apt.conf'''
        run_cmd(cmd, shell=True)
    if args.uninstall:
        run_cmd(
            f'{args.prefix} apt-get purge {args.yes} wajig', shell=True)


def wajig_args(subparser):
    subparser.add_argument(
        '-p',
        '--proxy',
        dest='proxy',
        default='',
        help='Configure apt to use the specified proxy.'
    )


def exa(args):
    if args.install:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} cargo install --root /usr/local/ exa',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['exa'])
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} cargo install --root /usr/local/ exa',
                shell=True,
            )
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} cargo uninstall --root /usr/local/ exa',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall exa', shell=True)
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} cargo uninstall --root /usr/local/ exa',
                shell=True,
            )


def osquery(args):
    if args.install:
        if _is_ubuntu_debian():
            cmd = f'''{args.prefix} apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B \
                    && {args.prefix} add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main' \
                    && {args.prefix} apt-get update {args.yes} \
                    && {args.prefix} apt-get {args.yes} install osquery
                '''
            run_cmd(cmd, shell=True)
        elif _is_macos():
            brew_install_safe(['osquery'])
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install osquery', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} osquery',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall osquery', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove osquery', shell=True)


# ------------------------- vim related -------------------------
def vim(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} vim vim-nox',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['vim'])
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install {args.yes} vim-enhanced',
                shell=True,
            )
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} vim vim-nox',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall vim', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove vim', shell=True)
    if args.config:
        pass


def neovim(args):
    if args.ppa and _is_ubuntu_debian():
        args.install = True
        run_cmd(
            f'{args.prefix} add-apt-repository -y ppa:neovim-ppa/stable',
            shell=True,
        )
        _update_apt_source()
    if args.install:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} neovim',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['neovim'])
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install neovim', shell=True)
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} neovim',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall neovim', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove neovim', shell=True)
    if args.config:
        pass


def neovim_args(subparser):
    subparser.add_argument(
        '--ppa',
        dest='ppa',
        action='store_true',
        help='Install the latest version of NeoVim from PPA.'
    )


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


def spacevim(args):
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
        cmd = f'''pip3 install --user python-language-server \
                && {args.prefix} npm install -g bash-language-server javascript-typescript-langserver
            '''
        run_cmd(cmd, shell=True)
    if args.uninstall:
        run_cmd(
            f'curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall',
            shell=True,
        )
    if args.config:
        _svim_gen_config()
    _svim_true_color(args.true_colors)


def spacevim_args(subparser):
    subparser.add_argument(
        '--enable-true-colors',
        dest='true_colors',
        action='store_true',
        default=None,
        help='enable true color (default true) for SpaceVim.'
    )
    subparser.add_argument(
        '--disable-true-colors',
        dest='true_colors',
        action='store_false',
        help='disable true color (default true) for SpaceVim.'
    )


def ideavim(args):
    if args.config:
        shutil.copy2(BASE_DIR / 'ideavim/ideavimrc', HOME / '.ideavimrc')


# ------------------------- coding tools related -------------------------
def git(args) -> None:
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} git git-lfs',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['git', 'git-lfs', 'bash-completion@2'])
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install git', shell=True)
        run_cmd('git lfs install', shell=True)
    if args.uninstall:
        run_cmd('git lfs uninstall', shell=True)
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} git git-lfs',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall git git-lfs', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove git', shell=True)
    if args.config:
        gitconfig = HOME / '.gitconfig'
        # try to remove the file to avoid dead symbolic link problem
        remove_file_safe(gitconfig)
        shutil.copy2(BASE_DIR / 'git/gitconfig', gitconfig)
        gitignore = HOME / '.gitignore'
        remove_file_safe(gitignore)
        shutil.copy2(BASE_DIR / 'git/gitignore', gitignore)
        if _is_macos():
            file = '/usr/local/etc/bash_completion.d/git-completion.bash'
            bashrc = f'\n# Git completion\n[ -f {file} ] &&  . {file}'
            with (HOME / '.bash_profile').open('a') as fout:
                fout.write(bashrc)
    if 'proxy' in args and args.proxy:
        run_cmd(
            f'git config --global http.proxy {proxy}',
            shell=True,
        )
        run_cmd(
            f'git config --global https.proxy {proxy}',
            shell=True,
        )


def git_args(subparser):
    subparser.add_argument(
        '-p',
        '--proxy',
        dest='proxy',
        default='',
        help='Configure Git to use the specified proxy.'
    )


def antlr(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} antlr4',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['antlr4'])
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install antlr', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} antlr4',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall antlr4', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove antlr', shell=True)


def docker(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} docker.io docker-compose',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['docker', 'docker-compose', 'bash-completion@2', 'docker-completion', 'docker-compose-completion'])
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install docker docker-compose',
                shell=True,
            )
    if args.config:
        run_cmd('gpasswd -a $(id -un) docker', shell=True)
        logger.warning('Please logout and then login to make the group "docker" effective!')
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} docker docker-compose',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew uninstall docker docker-completion docker-compose docker-compose-completion',
                shell=True,
            )
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} yum remove docker docker-compose',
                shell=True,
            )


def kubernetes(args):
    if args.install:
        if _is_ubuntu_debian():
            run_cmd(
                f'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | {args.prefix} apt-key add -',
                shell=True,
            )
            run_cmd(
                f'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | {args.prefix} tee -a /etc/apt/sources.list.d/kubernetes.list',
                shell=True,
            )
            _update_apt_source(seconds=-1E10)
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} kubectl',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['kubernetes-cli'])
        elif _is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} kubectl',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall kubectl', shell=True)
        elif _is_centos_series():
            pass


def _minikube_linux():
    run_cmd(
        f'''curl -L https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 -o /tmp/minikube-linux-amd64 \
            && {args.prefix} apt-get install {args.yes} /tmp/minikube-linux-amd64 /usr/local/bin/minikube''',
        shell=True,
    )
    print('VT-x/AMD-v virtualization must be enabled in BIOS.')


def minikube(args):
    virtualbox(args)
    kubernetes(args)
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source(seconds=-1E10)
            _minikube_linux()
        elif _is_macos():
            run_cmd(f'brew cask install minikube', shell=True)
        elif _is_centos_series():
            _minikube_linux()
        elif 'win32' in PLATFORM:
            run_cmd(f'choco install minikube', shell=True)
            print('VT-x/AMD-v virtualization must be enabled in BIOS.')
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} rm /usr/local/bin/minikube', shell=True
            )
        elif _is_macos():
            run_cmd(f'brew cask uninstall minikube', shell=True)
        elif _is_centos_series():
            run_cmd(
                f'{args.prefix} rm /usr/local/bin/minikube', shell=True
            )


# ------------------------- programming languages -------------------------
def cargo(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} cargo',
                shell=True,
            )
        if _is_macos():
            brew_install_safe(['cargo'])
        if _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install {args.yes} cargo',
                shell=True,
            )
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} cargo',
                shell=True,
            )
        if _is_macos():
            run_cmd(f'brew uninstall cargo', shell=True)
        if _is_centos_series():
            run_cmd(f'yum remove cargo', shell=True)


def openjdk8(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} openjdk-jdk-8 maven gradle',
                shell=True,
            )
        if _is_macos():
            cmd = 'brew tap AdoptOpenJDK/openjdk && brew cask install adoptopenjdk8'
            run_cmd(cmd, shell=True)
        if _is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} openjdk-jdk-8 maven gradle',
                shell=True,
            )
        if _is_macos():
            run_cmd(f'brew cask uninstall adoptopenjdk8', shell=True)
        if _is_centos_series():
            pass

def yapf(args):
    if args.install:
        run_cmd(
            f'pip3 install --user {args.yes} yapf',
            shell=True,
        )
    if args.config:
        shutil.copy2(os.path.join(BASE_DIR, 'yapf/style.yapf'), os.path.join(args.dst_dir, '.style.yapf'))
    if args.uninstall:
        run_cmd(
            f'pip3 uninstall {args.yes} yapf',
            shell=True,
        )

def yapf_args(subparser):
    subparser.add_argument(
        '-d',
        '--dest-dir',
        dest='dst_dir',
        requested=True,
        help='The destination directory to copy the YAPF configuration file to.'
    )


def nodejs(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            cmd = f'''{args.prefix} apt-get install {args.yes} nodejs npm'''
            run_cmd(cmd, shell=True)
        if _is_macos():
            brew_install_safe(['nodejs'])
        if _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install {args.yes} nodejs',
                shell=True,
            )
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} nodejs',
                shell=True,
            )
        if _is_macos():
            run_cmd(f'brew uninstall nodejs', shell=True)
        if _is_centos_series():
            run_cmd(f'yum remove nodejs', shell=True)


def ipython3(args):
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


def python3(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            cmd = f'''{args.prefix} apt-get install {args.yes} python3.7 python3-pip python3-setuptools && \
                    {args.prefix} ln -svf /usr/bin/python3.7 /usr/bin/python3
                    '''
            run_cmd(cmd, shell=True)
        if _is_macos():
            brew_install_safe(['python3'])
        if _is_centos_series():
            run_cmd(
                f'{args.prefix} yum install {args.yes} python34 python34-devel python34-pip',
                shell=True,
            )
            run_cmd(
                f'pip3.4 install --user setuptools', shell=True)
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} python3 python3-dev python3-setuptools python3-pip python3-venv',
                shell=True,
            )
        if _is_macos():
            run_cmd(f'brew uninstall python3', shell=True)
        if _is_centos_series():
            run_cmd(f'yum remove python3', shell=True)


def poetry(args):
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
            if _is_linux():
                cmd = f'{HOME}/.poetry/bin/poetry completions bash | {args.prefix} tee /etc/bash_completion.d/poetry.bash-completion > /dev/null'
                run_cmd(cmd, shell=True)
                return
            if _is_macos():
                cmd = f'$HOME/.poetry/bin/poetry completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion'
                run_cmd(cmd, shell=True)
    if args.uninstall:
        run_cmd(f'poetry self:uninstall', shell=True)


def poetry_args(subparser):
    subparser.add_argument(
        '-p',
        '--python',
        dest='python',
        default=None,
        help='The path to the Python interpreter.'
    )
    subparser.add_argument(
        '-b',
        '--bash-completion',
        dest='bash_completion',
        action='store_true',
        help='Configure Bash completion for poetry as well.'
    )


# ------------------------- JupyterLab kernels -------------------------
def nbdime(args):
    if args.install:
        run_cmd(f'pip3 install --user nbdime', shell=True)
    if args.uninstall:
        run_cmd(f'pip3 uninstall nbdime', shell=True)
    if args.config:
        run_cmd(f'nbdime config-git --enable --global', shell=True)


def itypescript(args):
    if args.install:
        run_cmd(
            f'{args.prefix} npm install -g --unsafe-perm itypescript',
            shell=True,
        )
        run_cmd(
            f'{args.prefix} its --ts-hide-undefined --install=global',
            shell=True,
        )
    if args.uninstall:
        run_cmd(
            f'{args.prefix} jupyter kernelspec uninstall typescript',
            shell=True,
        )
        run_cmd(f'{args.prefix} npm uninstall itypescript', shell=True)
    if args.config:
        pass


def beakerx(args):
    """Install/uninstall/configure the BeakerX kernels.
    """
    if args.install:
        run_cmd(f'pip3 install --user beakerx', shell=True)
        run_cmd(f'{args.prefix} beakerx install', shell=True)
        run_cmd(
            f'{args.prefix} jupyter labextension install @jupyter-widgets/jupyterlab-manager',
            shell=True,
        )
        run_cmd(
            f'{args.prefix} jupyter labextension install beakerx-jupyterlab',
            shell=True,
        )
    if args.uninstall:
        run_cmd(
            f'{args.prefix} jupyter labextension uninstall beakerx-jupyterlab',
            shell=True,
        )
        run_cmd(
            f'{args.prefix} jupyter labextension uninstall @jupyter-widgets/jupyterlab-manager',
            shell=True,
        )
        run_cmd(f'{args.prefix} beakerx uninstall', shell=True)
        run_cmd(f'pip3 uninstall beakerx', shell=True)
    if args.config:
        run_cmd(
            f'{args.prefix} chown -R {USER_ID}:{GROUP_ID} {HOME}',
            shell=True,
        )


def almond(args):
    """Install/uninstall/configure the Almond Scala kernel.
    """
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
            f'{args.prefix} {almond} --install --global --force',
            shell=True,
        )
    if args.config:
        pass


def almond_args(subparser):
    subparser.add_argument(
        '-a',
        '--almond-version',
        dest='almond_version',
        default=None,
        help='the version (0.4.0 by default) of Almond to install.'
    )
    subparser.add_argument(
        '-s',
        '--scala-version',
        dest='scala_version',
        default=None,
        help='the version (2.12.8 by default) of Scala to install.'
    )


# ------------------------- web tools -------------------------
def ssh_server(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} openssh-server fail2ban',
                shell=True,
            )
        elif _is_macos():
            pass
        elif _is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} openssh-server fail2ban',
                shell=True,
            )
        elif _is_macos():
            pass
        elif _is_centos_series():
            pass


def ssh_client(args):
    if args.config:
        src = BASE_DIR / 'ssh/client/config'
        des = HOME / '.ssh/config'
        shutil.copy2(src, des)
        des.chmod(0o600)


def proxychains(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} proxychains',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['proxychains-ng'])
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install proxychains', shell=True)
    if args.config:
        print('Configuring proxychains ...')
        des_dir = os.path.join(HOME, '.proxychains')
        os.makedirs(des_dir, exist_ok=True)
        shutil.copy2(
            os.path.join(BASE_DIR, 'proxychains/proxychains.conf'), des_dir
        )
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge proxychains', shell=True)
        elif _is_macos():
            run_cmd(f'brew uninstall proxychains-ng', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove proxychains', shell=True)


def dryscrape(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            cmd = f'''{args.prefix} apt-get install {args.yes} qt5-default libqt5webkit5-dev build-essential xvfb \
                && pip3 install --user dryscrape
                '''
            run_cmd(cmd, shell=True)
        elif _is_macos():
            pass
        elif _is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            pass
        elif _is_macos():
            pass
        elif _is_centos_series():
            pass


def blogging(args):
    if args.install:
        run_cmd(f'pip3 install --user pelican markdown', shell=True)
        archives = HOME / 'archives'
        archives.mkdir(0o700, exist_ok=True)
        blog = archives / 'blog'
        if blog.is_dir():
            run_cmd(f'git -C {blog} pull origin master', shell=True)
        else:
            run_cmd(f'git clone git@github.com:dclong/blog.git {archives}', shell=True)
        cmd = f'''git -C {blog} submodule init && \
                git -C {blog} submodule update --recursive --remote
                '''
        run_cmd(cmd, shell=True)
    if args.config:
        pass
    if args.uninstall:
        run_cmd(
            f'pip3 uninstall pelican markdown', shell=True)


def download_tools(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} wget curl aria2',
                shell=True,
            )
        elif _is_macos():
            brew_install_safe(['wget', 'curl', 'aria2'])
        elif _is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} wget curl aria2',
                shell=True,
            )
        elif _is_macos():
            run_cmd(f'brew uninstall wget curl aria2', shell=True)
        elif _is_centos_series():
            pass


# ------------------------- IDE -------------------------
def intellij_idea(args):
    if args.install:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} add-apt-repository ppa:mmk2410/intellij-idea',
                shell=True,
            )
            _update_apt_source(seconds=-1E10)
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} intellij-idea-community',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew cask install intellij-idea-ce', shell=True)
        elif _is_centos_series():
            pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} intellij-idea-ce',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew cask uninstall intellij-idea-ce', shell=True)
        elif _is_centos_series():
            pass
    if args.config:
        pass


def visual_studio_code(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} vscode',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew cask install visual-studio-code', shell=True)
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum install vscode', shell=True)
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} vscode',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew cask uninstall visual-studio-code',
                shell=True,
            )
        elif _is_centos_series():
            run_cmd(f'{args.prefix} yum remove vscode', shell=True)
    if args.config:
        src_file = f'{BASE_DIR}/vscode/settings.json'
        dst_dir = f'{HOME}/.config/Code/User/'
        if _is_macos():
            dst_dir = '{HOME}/Library/Application Support/Code/User/'
        os.makedirs(dst_dir, exist_ok=True)
        os.symlink(src_file, dst_dir, target_is_directory=True)
        run_cmd(f'ln -svf {src_file} {dst_dir}', shell=True)


def virtualbox(args):
    if args.install:
        if _is_ubuntu_debian():
            _update_apt_source()
            run_cmd(
                f'{args.prefix} apt-get install {args.yes} virtualbox-qt',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew cask install virtualbox virtualbox-extension-pack',
                shell=True,
            )
        elif _is_centos_series():
            pass
    if args.uninstall:
        if _is_ubuntu_debian():
            run_cmd(
                f'{args.prefix} apt-get purge {args.yes} virtualbox-qt',
                shell=True,
            )
        elif _is_macos():
            run_cmd(
                f'brew cask uninstall virtualbox virtualbox-extension-pack',
                shell=True,
            )
        elif _is_centos_series():
            pass
    if args.config:
        pass


# ------------------------- helper functions -------------------------
def to_bool(value: Any) -> bool:
    """Convert an object to a bool value (True or False).

    :param value: any object that can be converted to a bool value.
    :return: True or False.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ('t', 'true', 'y', 'yes'):
            return True
        if value.isdigit():
            return int(value) != 0
        return False
    if isinstance(value, int) and value != 0:
        return True
    if isinstance(value, Sized) and len(value) > 0:
        return True
    return False


def _add_subparser(
    subparsers,
    name: str,
    aliases: Sequence = (),
    func: Union[Callable, None] = None,
    add_argument: Union[Callable, None] = None
):
    sub_cmd = re.sub(r'(\s+)|-', '_', name.lower())
    aliases = [alias for alias in aliases if alias != sub_cmd]
    func = func if func else eval(sub_cmd)
    subparser = subparsers.add_parser(
        sub_cmd, aliases=aliases, help=f'install and configure {name}.'
    )
    subparser.add_argument(
        '-i',
        '--install',
        dest='install',
        action='store_true',
        help=f'install {name}.'
    )
    subparser.add_argument(
        '-u',
        '--uninstall',
        dest='uninstall',
        action='store_true',
        help=f'uninstall {name}.'
    )
    subparser.add_argument(
        '-y',
        '--yes',
        dest='yes',
        action='store_const',
        const='--yes',
        default='',
        help='Automatical yes (default no) to prompts.'
    )
    subparser.add_argument(
        '-c',
        '--configure',
        dest='config',
        action='store_true',
        help=f'configure {name}.'
    )
    subparser.add_argument(
        '-l',
        '--log',
        dest='log',
        action='store_true',
        help=f'Print the command to run.'
    )
    if add_argument:
        add_argument(subparser)
    subparser.set_defaults(func=func)
    return subparser


def _update_apt_source(seconds: float = 3600 * 12):
    key = 'apt_source_update_time'
    time = datetime.datetime.strptime(
        SETTINGS.get(key, '2000-01-01 00:00:00.000000'), FORMAT
    )
    now = datetime.datetime.now()
    if (now - time).seconds > seconds:
        run_cmd(f'{args.prefix} apt-get update {args.yes}', shell=True)
        SETTINGS[key] = now.strftime(FORMAT)
        with open(SETTINGS_FILE, 'w') as fout:
            json.dump(SETTINGS, fout)


if __name__ == '__main__':
    remove_file_safe(LINSTALL)
    LINSTALL.symlink_to(FILE)
    args = parse_args()
    args.func(args)
