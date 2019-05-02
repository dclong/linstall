#!/usr/bin/env python3

import os
import json
import platform
import shutil
import re
from typing import Any, List, Sequence, Callable, Union
from argparse import ArgumentParser
import datetime
import logging

USER_ID = os.getuid()
GROUP_ID = os.getgid()
PREFIX = '' if USER_ID == 0 else 'sudo'
HOME = os.path.expanduser('~')
BASE_DIR = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
PLATFORM = platform.platform().lower() 
SETTINGS_FILE = os.path.join(HOME, '.linstall.json')
SETTINGS = json.load(SETTINGS_FILE) if os.path.isfile(SETTINGS_FILE) else {}


def _update_apt_source(seconds: float = 3600 * 12):
    key = 'apt_source_update_time'
    time = SETTINGS.get(key, datetime.datetime(2000, 1, 1))
    now = datetime.datetime.now()
    if (now - time).seconds > seconds:
        os.system(f'{PREFIX} apt-get update')
        SETTINGS[key] = now
        json.dump(SETTINGS, SETTINGS_FILE)


def parse_args(args=None, namespace=None):
    """Parse command-line arguments for the install/configuration util.
    """
    parser = ArgumentParser(description='Easy installation and configuration for Unix/Linux')
    subparsers = parser.add_subparsers(dest='sub_cmd', help='Sub commands.')
    #------------------------- linstall itself ------------------------------
    _add_subparser(subparsers, 'update', aliases=['pull', 'upd', 'pu'])
    #------------------------- command-line tools ------------------------------
    _add_subparser(subparsers, 'CoreUtils', aliases=['cu'])
    _add_subparser(subparsers, 'change shell', aliases=['chsh', 'cs'], add_argument=change_shell_args)
    _add_subparser(subparsers, 'Shell utils', aliases=['sh_utils', 'shutils', 'shu', 'su'])
    _add_subparser(subparsers, 'Hyper', aliases=['hp'])
    _add_subparser(subparsers, 'Bash completion', aliases=['completion', 'comp', 'cp'])
    _add_subparser(subparsers, 'Wajig', aliases=['wj'])
    _add_subparser(subparsers, 'exa')
    _add_subparser(subparsers, 'osquery', aliases=['osq'])
    #------------------------- Vim ------------------------------
    _add_subparser(subparsers, 'Vim')
    _add_subparser(subparsers, 'NeoVim', aliases=['nvim'])
    _add_subparser(subparsers, 'SpaceVim', aliases=['svim'], add_argument=spacevim_args)
    _add_subparser(subparsers, 'IdeaVim', aliases=['ivim'])
    #------------------------- development related  ------------------------------
    _add_subparser(subparsers, 'Git')
    _add_subparser(subparsers, 'Python3', aliases=['py3'])
    _add_subparser(subparsers, 'Poetry', aliases=['pt'], add_argument=poetry_args)
    _add_subparser(subparsers, 'Cargo', aliases=['cgo'])
    _add_subparser(subparsers, 'ANTLR')
    _add_subparser(subparsers, 'Docker', aliases=['dock', 'dk'])
    _add_subparser(subparsers, 'Kubernetes', aliases=['k8s'])
    #------------------------- web related ------------------------------
    _add_subparser(subparsers, 'SSH server', aliases=['sshs'])
    _add_subparser(subparsers, 'blogging', aliases=['blog'])
    _add_subparser(subparsers, 'ProxyChains', aliases=['pchains', 'pc'])
    _add_subparser(subparsers, 'download tools', aliases=['dl', 'dlt'])
    #------------------------- JupyterLab related ------------------------------
    _add_subparser(subparsers, 'BeakerX', aliases=['bkx', 'bk'])
    _add_subparser(subparsers, 'Almond', aliases=['al', 'amd'], add_argument=almond_args)
    _add_subparser(subparsers, 'iTypeScript', aliases=['its'])
    #------------------------- IDEs ------------------------------
    _add_subparser(subparsers, 'Visual Studio Code', aliases=['vscode', 'code'])
    _add_subparser(subparsers, 'IntelliJ IDEA', aliases=['intellij', 'idea', 'ii'])
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
    os.system(f'git pull origin master')


def coreutils(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} coreutils')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install coreutils')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install coreutils')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} coreutils')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall coreutils')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove coreutils')
    if args.config:
        if 'darwin' in PLATFORM:
            os.system(f'export PATH="/usr/local/opt/findutils/libexec/gnubin:$PATH"')
            os.system(f'export MANPATH="/usr/local/opt/findutils/libexec/gnuman:$MANPATH"')


# ------------------------- command-line utils related -------------------------
def shell_utils(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} bash-completion command-not-found man-db')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install bash-completion man-db')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install bash-completion command-not-found man-db')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} bash-completion command-not-found man-db')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall bash-completion man-db')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove bash-completion command-not-found man-db')
    if args.config:
        pass


def change_shell(args):
    if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
        pass
    elif 'darwin' in PLATFORM:
        os.system(f'chsh -s {args.shell}')
    elif 'centos' in PLATFORM:
        pass


def change_shell_args(subparser):
    subparser.add_argument(
        '-s',
        '--shell',
        dest='shell',
        default='/bin/bash',
        help='the shell to change to.')


def hyper(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            #!{PREFIX} apt-get install {args.yes} hyper
            pass
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask install hyper')
        elif 'centos' in PLATFORM:
            #!sudo yum install hyper
            pass
    if args.config:
        os.system(f'hyper i hypercwd')
        os.system(f'hyper i hyper-search')
        os.system(f'hyper i hyper-pane')
        os.system(f'hyper i hyperpower')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            #!{PREFIX} apt-get purge hyper
            pass
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask uninstall hyper')
        elif 'centos' in PLATFORM:
            #!sudo yum remove hyper
            pass

def bash_completion(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} bash-completion')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install bash-completion')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install bash-completion')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge bash-completion')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall bash-completion')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove bash-completion')


def wajig(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} wajig')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} wajig')


def exa(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} cargo install --root /usr/local/ exa')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install exa')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} cargo install --root /usr/local/ exa')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} cargo uninstall --root /usr/local/ exa')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall exa')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} cargo uninstall --root /usr/local/ exa')


def osquery(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get install {args.yes} osquery')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install osquery')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install osquery')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} osquery')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall osquery')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove osquery')


# ------------------------- vim related -------------------------
def vim(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} vim vim-nox')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install vim')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install {args.yes} vim-enhanced')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} vim vim-nox')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall vim')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove vim')
    if args.config:
        pass


def neovim(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} neovim')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install neovim')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install neovim')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} neovim')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall neovim')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove neovim')
    if args.config:
        pass


def _svim_true_color(true_color: bool):
    FILE = os.path.join(HOME, '.SpaceVim.d/init.toml')
    if os.path.isfile(FILE):
        with open(FILE, 'r') as fin:
            lines = fin.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith('enable_guicolors'):
                if true_color:
                    lines[i] = line.replace('false', 'true')
                else:
                    lines[i] = line.replace('true', 'false')
        with open(FILE, 'w') as fout:
            fout.writelines(lines)


def spacevim(args):
    if args.install:
        os.system(f'curl -sLf https://spacevim.org/install.sh | bash')
        if shutil.which('nvim'):
            os.system(f'nvim --headless +"call dein#install()" +qall')
    if args.uninstall:
        os.system(f'curl -sLf https://spacevim.org/install.sh | bash -s -- --uninstall')
    if args.config:
        des_dir = os.path.join(HOME, '.SpaceVim.d')
        os.system(f'mkdir -p {des_dir}')
        os.system(f'cp {BASE_DIR}/SpaceVim/init.toml {des_dir}')
        _svim_true_color(args.true_color)


def spacevim_args(subparser):
    subparser.add_argument(
        '-t',
        '--true-color',
        dest='true_color',
        type=to_bool,
        default=True,
        help='whether to enable true color (default true) for SpaceVim.')


def ideavim(args):
    if args.config:
        os.system(f'cp {BASE_DIR}/ideavim/ideavimrc $HOME/.ideavimrc')


# ------------------------- coding tools related -------------------------
def git(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} git git-lfs')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install git git-lfs')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install git')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} git git-lfs')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall git git-lfs')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove git')
    if args.config:
        os.system(f'cp "{BASE_DIR}/git/gitconfig" $HOME/.gitconfig')
        os.system(f'cp "{BASE_DIR}/git/gitignore" $HOME/.gitignore')
        if 'darwin' in PLATFORM:
            os.system(f'cp {BASE_DIR}/git/mac/git_completion {HOME}/.git_completion')


def antlr(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} antlr4')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install antlr4')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install antlr')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} antlr4')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall antlr4')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove antlr')


def docker(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} docker docker-compose')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install docker docker-completion docker-compose docker-compose-completion')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install docker docker-compose')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} docker docker-compose')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall docker docker-completion docker-compose docker-compose-completion')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove docker docker-compose')


def kubernetes(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | {PREFIX} apt-key add -')
            os.system(f'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | {PREFIX} tee -a /etc/apt/sources.list.d/kubernetes.list')
            _update_apt_source(seconds=-1E10)
            os.system(f'{PREFIX} apt-get install {args.yes} kubectl')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install kubernetes-cli')
        elif 'centos' in PLATFORM:
            pass
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} kubectl')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall kubectl')
        elif 'centos' in PLATFORM:
            pass


# ------------------------- programming languages -------------------------
def cargo(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} cargo')
        if 'darwin' in PLATFORM:
            os.system(f'brew install cargo')
        if 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install {args.yes} cargo')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} cargo')
        if 'darwin' in PLATFORM:
            os.system(f'brew uninstall cargo')
        if 'centos' in PLATFORM:
            os.system(f'yum remove cargo')


def python3(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} python3 python3-dev python3-setuptools python3-pip python3-venv')
        if 'darwin' in PLATFORM:
            os.system(f'brew install python3')
        if 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install {args.yes} python34 python34-devel python34-pip')
            os.system(f'{PREFIX} pip3.4 install setuptools')
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} python3 python3-dev python3-setuptools python3-pip python3-venv')
        if 'darwin' in PLATFORM:
            os.system(f'brew uninstall python3')
        if 'centos' in PLATFORM:
            os.system(f'yum remove python3')


def poetry(args):
    if args.install:
        os.system(f'curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | {args.python}')
    if args.config:
        if 'darwin' in PLATFORM:
            os.system(f'$HOME/.poetry/bin/poetry completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion')
        else:
            os.system(f'{PREFIX} $HOME/.poetry/bin/poetry completions bash > /etc/bash_completion.d/poetry.bash-completion')
    if args.uninstall:
        os.system(f'poetry self:uninstall')


def poetry_args(subparser):
    subparser.add_argument(
        '-p',
        '--python',
        dest='python',
        default='python3',
        help='The path to the Python interpreter.')


# ------------------------- JupyterLab kernels -------------------------
def itypescript(args):
    if args.install:
        os.system(f'{PREFIX} npm install -g --unsafe-perm itypescript')
        os.system(f'{PREFIX} its --ts-hide-undefined --install=global')
    if args.uninstall:
        os.system(f'{PREFIX} jupyter kernelspec uninstall typescript')
        os.system(f'{PREFIX} npm uninstall itypescript')
    if args.config:
        pass


def beakerx(args):
    if args.install:
        os.system(f'{PREFIX} pip3 install beakerx')
        os.system(f'{PREFIX} beakerx install')
        os.system(f'{PREFIX} jupyter labextension install @jupyter-widgets/jupyterlab-manager')
        os.system(f'{PREFIX} jupyter labextension install beakerx-jupyterlab')
    if args.uninstall:
        os.system(f'{PREFIX} jupyter labextension uninstall beakerx-jupyterlab')
        os.system(f'{PREFIX} jupyter labextension uninstall @jupyter-widgets/jupyterlab-manager')
        os.system(f'{PREFIX} beakerx uninstall')
        os.system(f'{PREFIX} pip3 uninstall beakerx')
    if args.config:
        os.system(f'{PREFIX} chown -R {USER_ID}:{GROUP_ID} {HOME}')


def almond(args):
    if args.install:
        coursier = os.path.join(HOME, '.local/bin/coursier')
        almond = os.path.join(HOME, '.local/bin/almond')
        os.system(f'curl -L -o {coursier} https://git.io/coursier-cli')
        os.system(f'chmod +x {coursier}')
        os.system(f'''{coursier} bootstrap -f -r jitpack -i user \
                -I user:sh.almond:scala-kernel-api_{args.scala_version}:{args.almond_version} \
                -o {almond} \
                sh.almond:scala-kernel_{args.scala_version}:{args.almond_version}''')
        os.system(f'{PREFIX} {almond} --install --global --force')
    if args.config:
        pass


def almond_args(subparser):
    subparser.add_argument(
        '-a',
        '--almond-version',
        dest='almond_version',
        default='0.4.0',
        help='the version (0.4.0 by default) of Almond to install.')
    subparser.add_argument(
        '-s',
        '--scala-version',
        dest='scala_version',
        default='2.12.8',
        help='the version (2.12.8 by default) of Scala to install.')


# ------------------------- web tools -------------------------
def ssh_server(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} openssh-server fail2ban')
        elif 'darwin' in PLATFORM:
            pass
        elif 'centos' in PLATFORM:
            pass
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} openssh-server fail2ban')
        elif 'darwin' in PLATFORM:
            pass
        elif 'centos' in PLATFORM:
            pass


def proxychains(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} proxychains')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install proxychains-ng')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install proxychains')
    if args.config:
        print('Configuring proxychains ...')
        des_dir = os.path.join(HOME, '.proxychains')
        os.system(f'mkdir -p {des_dir}')
        os.system(f'cp {BASE_DIR}/proxychains/proxychains.conf {des_dir}/')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge proxychains')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall proxychains-ng')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove proxychains')


def blogging(args):
    if args.install:
        # python3(args)
        os.system(f'pip3 install --user pelican markdown')
    if args.config:
        pass
    if args.uninstall:
        os.system(f'pip3 uninstall --user pelican markdown')


def download_tools(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} wget curl aria2')
        elif 'darwin' in PLATFORM:
            os.system(f'brew install wget curl aria2')
        elif 'centos' in PLATFORM:
            pass
    if args.config:
        pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} wget curl aria2')
        elif 'darwin' in PLATFORM:
            os.system(f'brew uninstall wget curl aria2')
        elif 'centos' in PLATFORM:
            pass


# ------------------------- IDE -------------------------
def intellij_idea(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} add-apt-repository ppa:mmk2410/intellij-idea')
            _update_apt_source(seconds=-1E10)
            os.system(f'{PREFIX} apt-get install {args.yes} intellij-idea-community')
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask install intellij-idea-ce')
        elif 'centos' in PLATFORM:
            pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} intellij-idea-ce')
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask uninstall intellij-idea-ce')
        elif 'centos' in PLATFORM:
            pass
    if args.config:
        pass


def visual_studio_code(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} vscode')
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask install visual-studio-code')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum install vscode')
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} vscode')
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask uninstall visual-studio-code')
        elif 'centos' in PLATFORM:
            os.system(f'{PREFIX} yum remove vscode')
    if args.config:
        srcfile = f'{BASE_DIR}/vscode/settings.json'
        desdir = f'{HOME}/.config/Code/User/'
        os.system(f'mkdir -p {desdir}')
        os.system(f'ln -svf {srcfile} {desdir}')


def virtualbox(args):
    if args.install:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            _update_apt_source()
            os.system(f'{PREFIX} apt-get install {args.yes} virtualbox-qt')
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask install virtualbox virtualbox-extension-pack')
        elif 'centos' in PLATFORM:
            pass
    if args.uninstall:
        if 'ubuntu' in PLATFORM or 'debian' in PLATFORM:
            os.system(f'{PREFIX} apt-get purge {args.yes} virtualbox-qt')
        elif 'darwin' in PLATFORM:
            os.system(f'brew cask uninstall virtualbox virtualbox-extension-pack')
        elif 'centos' in PLATFORM:
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


def _add_subparser(subparsers, name: str, aliases: Sequence = (), func: Union[Callable, None] = None, add_argument: Union[Callable, None] = None):
    sub_cmd = re.sub(r'\s+', '_', name.lower())
    aliases = [alias for alias in aliases if alias != sub_cmd]
    func = func if func else eval(sub_cmd)
    subparser = subparsers.add_parser(
        sub_cmd,
        aliases=aliases,
        help=f'install and configure {name}.')
    subparser.add_argument(
        '-i',
        '--install',
        dest='install',
        action='store_true',
        help=f'install {name}.')
    subparser.add_argument(
        '-u',
        '--uninstall',
        dest='uninstall',
        action='store_true',
        help=f'uninstall {name}.')
    subparser.add_argument(
        '-y',
        '--yes',
        dest='yes',
        action='store_const',
        const='--yes',
        default='',
        help='Automatical yes (default no) to prompts.')
    subparser.add_argument(
        '-c',
        '--configure',
        dest='config',
        action='store_true',
        help=f'configure {name}.')
    if add_argument:
        add_argument(subparser)
    subparser.set_defaults(func=func)
    return subparser


if __name__ == '__main__':
    args = parse_args()
    args.func(args)
