"""GitHub related utils.
"""
import logging
from .utils import (option_python, option_pip_bundle, add_subparser, run_cmd)
from . import utils
logging.basicConfig(
    format=
    "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
    level=logging.INFO
)


def install_py_github(args) -> None:
    """Install a Python package from GitHub.
    """
    utils.install_py_github(
        url=args.url, user=args.user, pip=args.pip, pip_option=args.pip_option
    )


def _add_subparser_install_py_github(subparsers) -> None:
    subparser = subparsers.add_parser(
        "install_py_github",
        aliases=["inpygit", "pygit", "ipg"],
        help="Install the latest version of a Python package from GitHub."
    )
    subparser.add_argument(
        dest="url", help="The URL of the Python package's GitHub repository."
    )
    option_pip_bundle(subparser)
    option_python(subparser)
    subparser.set_defaults(func=install_py_github)
    return subparser


def dsutil(args) -> None:
    """Install the Python package dsutil.
    """
    if args.install:
        url = "https://github.com/dclong/dsutil"
        utils.install_py_github(
            url=url, pip=args.pip, user=args.user, pip_option=args.pip_option
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall {args.yes_s} dsutil")


def _dsutil_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_dsutil(subparsers) -> None:
    add_subparser(
        subparsers, "dsutil", func=dsutil, aliases=[], add_argument=_dsutil_args
    )


def xinstall(args) -> None:
    """Install xonsh, a Python based shell.
    """
    if args.install:
        url = "https://github.com/dclong/xinstall"
        utils.install_py_github(
            url=url, user=args.user, pip=args.pip, pip_option=args.pip_option
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall xinstall")


def _xinstall_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_xinstall(subparsers) -> None:
    add_subparser(
        subparsers, "xinstall", func=xinstall, aliases=[], add_argument=_xinstall_args
    )
