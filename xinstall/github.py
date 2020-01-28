from .utils import option_pip, option_python, option_sys, namespace, add_subparser, run_cmd
from . import utils


def install_py_github(**kwargs):
    args = namespace(kwargs)
    utils.install_py_github(
        url=args.url, sudo=args.sudo, sys=args.sys, pip=args.pip
    )


def add_subparser_install_py_github(subparsers):
    subparser = subparsers.add_parser(
        "install_py_github",
        aliases=["inpygit", "pygit", "ipg"],
        help="Install the latest version of a Python package from GitHub."
    )
    subparser.add_argument(
        dest="url", help=f"The URL of the Python package's GitHub repository."
    )
    option_sys(subparser)
    option_python(subparser)
    option_pip(subparser)
    subparser.set_defaults(func=install_py_github)
    return subparser


def dsutil(**kwargs):
    """Install the Python package dsutil.
    """
    args = namespace(kwargs)
    if args.install:
        url = 'https://github.com/dclong/dsutil'
        utils.install_py_github(url=url, pip=args.pip)
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f'{args.pip} uninstall {args._yes_s} dsutil')


def _dsutil_args(subparser):
    option_sys(subparser)


def add_subparser_dsutil(subparsers):
    add_subparser(subparsers, "dsutil", aliases=[], add_argument=_dsutil_args)


def xinstall(**kwargs):
    """Install xonsh, a Python based shell.
    """
    args = namespace(kwargs)
    if args.install:
        url = 'https://github.com/dclong/xinstall'
        utils.install_py_github(
            url=url, sudo=args.sudo, sys=args.sys, pip=args.pip
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.sudo_s} {args.pip} uninstall xinstall")


def _xinstall_args(subparser):
    option_sys(subparser)


def add_subparser_xinstall(subparsers):
    add_subparser(
        subparsers, "xinstall", aliases=[], add_argument=_xinstall_args
    )


def pybay(**kwargs):
    """Install the Python package pybay.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.sudo_s} {args.pip} install git+ssh://git@github.corp.ebay.com/marketing-science/pybay"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.sudo_s} {args.pip} uninstall pybay")


def add_subparser_pybay(subparsers):
    add_subparser(subparsers, "pybay", aliases=[])