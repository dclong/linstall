"""GitHub related utils.
"""
import logging
import shutil
import requests
from packaging.version import parse
from packaging.specifiers import SpecifierSet
from .utils import (option_python, option_pip_bundle, add_subparser, run_cmd)
from . import utils
logging.basicConfig(
    format=
    "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
    level=logging.INFO
)


def _github_download(args):
    if args.version:
        v0 = args.version[0]
        if v0.isdigit():
            args.version = "==" + args.version
        elif v0 == "v":
            args.version = "==" + args.version[1:]
    spec = SpecifierSet(args.version)
    # get asserts of the first release in the specifier
    url = f"https://api.github.com/repos/{args.repo}/releases"
    resp = requests.get(url)
    if not resp.ok:
        resp.raise_for_status()
    releases = resp.json()
    assets = next(
        release["assets"] for release in releases if parse(release["tag_name"]) in spec
    )
    # get download URL
    if args.keyword:
        args.filter = lambda name: all(kwd in name for kwd in args.keyword)
    url = next(
        asset["browser_download_url"] for asset in assets if args.filter(asset["name"])
    )
    # download the assert
    logging.info("Downloading assert from the URL: %s", url)
    resp = requests.get(url, stream=True)
    if not resp.ok:
        resp.raise_for_status()
    with open(args.output, "wb") as fout:
        shutil.copyfileobj(resp.raw, fout)


def github(args) -> None:
    """Download packages from GitHub and then install and configure it.

    :param args:
    """
    if args.output:
        _github_download(args)
    if args.install_cmd:
        run_cmd(f"{args.install_cmd} {args.output}")


def _github_args(subparser):
    subparser.add_argument(
        "-r",
        "--repo",
        "--repository",
        dest="repo",
        required=True,
        help="The GitHub repository from which to download the package.",
    )
    subparser.add_argument(
        "-v",
        "--version",
        dest="version",
        default="",
        help="The version specifier of the package to download/install/configure.",
    )
    subparser.add_argument(
        "-k",
        "--kwd",
        "--keyword",
        dest="keyword",
        nargs="+",
        default=(),
        help="The keywords that assert's name must contain.",
    )
    subparser.add_argument(
        "-f",
        "--filter",
        dest="filter",
        default=lambda namme: True,
        help=
        "The function to filter assert. It is overwritten by --keyword if specified.",
    )
    subparser.add_argument(
        "-o",
        "--output",
        dest="output",
        default="",
        help="The output path for the downloaded assert.",
    )
    subparser.add_argument(
        "--cmd",
        "--install-cmd",
        dest="install_cmd",
        default="",
        help="The output path for the downloaded assert.",
    )


def _add_subparser_github(subparsers) -> None:
    add_subparser(
        subparsers,
        "github",
        func=github,
        aliases=["gh"],
        add_argument=_github_args,
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
