from .utils import option_pip, option_python, option_user, namespace, add_subparser, run_cmd
from . import utils


def install_py_github(**kwargs):
    args = namespace(kwargs)
    utils.install_py_github(
        url=args.url, sudo=args.sudo, user=args.user, pip=args.pip
    )


def _add_subparser_install_py_github(subparsers):
    subparser = subparsers.add_parser(
        "install_py_github",
        aliases=["inpygit", "pygit", "ipg"],
        help="Install the latest version of a Python package from GitHub."
    )
    subparser.add_argument(
        dest="url", help=f"The URL of the Python package's GitHub repository."
    )
    option_user(subparser)
    option_python(subparser)
    option_pip(subparser)
    subparser.set_defaults(func=install_py_github)
    return subparser


def dsutil(**kwargs):
    """Install the Python package dsutil.
    """
    args = namespace(kwargs)
    if args.install:
        url = "https://github.com/dclong/dsutil"
        utils.install_py_github(
            url=url, pip=args.pip, sudo=args.sudo, user=args.user
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.pip} uninstall {args._yes_s} dsutil")


def _dsutil_args(subparser):
    option_user(subparser)


def _add_subparser_dsutil(subparsers):
    add_subparser(
        subparsers,
        "dsutil",
        func=dsutil,
        aliases=[],
        add_argument=_dsutil_args
    )


def xinstall(**kwargs):
    """Install xonsh, a Python based shell.
    """
    args = namespace(kwargs)
    if args.install:
        url = "https://github.com/dclong/xinstall"
        utils.install_py_github(
            url=url, sudo=args.sudo, user=args.user, pip=args.pip
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.sudo_s} {args.pip} uninstall xinstall")


def _xinstall_args(subparser):
    option_user(subparser)


def _add_subparser_xinstall(subparsers):
    add_subparser(
        subparsers,
        "xinstall",
        func=xinstall,
        aliases=[],
        add_argument=_xinstall_args
    )
