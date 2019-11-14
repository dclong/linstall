from typing import Sequence, Union, Callable
from argparse import ArgumentParser
import re
from .utils import is_macos
import linstall


def wajig_args(subparser):
    subparser.add_argument(
        '-p',
        '--proxy',
        dest='proxy',
        default='',
        help='Configure apt to use the specified proxy.'
    )


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


def neovim_args(subparser):
    subparser.add_argument(
        '--ppa',
        dest='ppa',
        action='store_true',
        help='Install the latest version of NeoVim from PPA.'
    )


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


def git_args(subparser):
    subparser.add_argument(
        '-p',
        '--proxy',
        dest='proxy',
        default='',
        help='Configure Git to use the specified proxy.'
    )


def yapf_args(subparser):
    subparser.add_argument(
        '-d',
        '--dest-dir',
        dest='dst_dir',
        requested=True,
        help='The destination directory to copy the YAPF configuration file to.'
    )


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


def _add_subparser(
    subparsers,
    name: str,
    aliases: Sequence = (),
    func: Union[Callable, None] = None,
    add_argument: Union[Callable, None] = None
):
    sub_cmd = re.sub(r'(\s+)|-', '_', name.lower())
    aliases = [alias for alias in aliases if alias != sub_cmd]
    func = func if func else eval('linstall.{sub_cmd}')
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
        default='' if linstall.USER_ID == 0 or is_macos() else 'sudo',
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
    _add_subparser(subparsers, 'dsutil', aliases=[])
    _add_subparser(subparsers, 'OpenJDK8', aliases=['jdk8'])
    _add_subparser(subparsers, 'sdkman', aliases=[])
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
    _add_subparser(subparsers, 'jupyterlab-lsp', aliases=['jlab-lsp', 'jlab_lsp'])
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


def main():
    args = parse_args()
    args.func(**vars(args))


if __name__ == '__main__':
    main()
