"""GitHub related utils.
"""
import logging
import shutil
import requests
from packaging.version import parse
from packaging.specifiers import SpecifierSet
from .utils import (
    option_version, option_pip_bundle, add_subparser, run_cmd
)
from . import utils


def _github_release_url(repo: str) -> str:
    if repo.endswith(".git"):
        repo = repo[:-4]
    if repo.startswith("https://api."):
        return repo
    if repo.startswith("https://"):
        rindex = repo.rindex("/")
        index = repo.rindex("/", 0, rindex)
        repo = repo[(index + 1):]
    elif repo.startswith("git@"):
        index = repo.rindex(":")
        repo = repo[(index + 1):]
    return f"https://api.github.com/repos/{repo}/releases"


def _github_download(args):
    if args.version:
        v0 = args.version[0]
        if v0.isdigit():
            args.version = "==" + args.version
        elif v0 == "v":
            args.version = "==" + args.version[1:]
    spec = SpecifierSet(args.version)
    # get asserts of the first release in the specifier
    resp = requests.get(_github_release_url(args.repo))
    if not resp.ok:
        resp.raise_for_status()
    releases = resp.json()
    assets = next(
        release["assets"] for release in releases if parse(release["tag_name"]) in spec
    )
    # get download URL
    if args.keyword:
        filter_ = lambda name: all(kwd in name for kwd in args.keyword)
    else:
        filter_ = lambda name: True
    url = next(
        asset["browser_download_url"] for asset in assets if filter_(asset["name"])
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

    :param args: The arguments to parse. 
        If None, the arguments from command-line are parsed.
    """
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
    option_version(
        subparser,
        help="The version specifier of the package to download/install/configure."
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
        "-o",
        "--output",
        dest="output",
        required=True,
        help="The output path for the downloaded assert.",
    )
    subparser.add_argument(
        "--cmd",
        "--install-cmd",
        dest="install_cmd",
        default="",
        help="The output path for the downloaded assert.",
    )


def _add_subparser_github_(subparsers) -> None:
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
        url=args.url,
        user=args.user,
        pip_option=args.pip_option,
        prefix=args.prefix,
        python=args.python,
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
    subparser.set_defaults(func=install_py_github)
    return subparser


def dsutil(args) -> None:
    """Install the Python package dsutil.
    """
    if args.install:
        url = "https://github.com/dclong/dsutil"
        utils.install_py_github(
            url=url,
            user=args.user,
            pip_option=args.pip_option,
            extras=args.extras,
            prefix=args.prefix,
            python=args.python,
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.prefix} {args.pip_uninstall} dsutil")


def _dsutil_args(subparser) -> None:
    option_pip_bundle(subparser)
    subparser.add_argument(
        "-e",
        "--extras",
        dest="extras",
        default="",
        help="Extra components to install."
    )


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
            url=url,
            user=args.user,
            pip_option=args.pip_option,
            prefix=args.prefix,
            python=args.python,
        )
    if args.config:
        pass
    if args.uninstall:
        run_cmd(f"{args.prefix} {args.pip_uninstall} uninstall xinstall")


def _xinstall_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_xinstall(subparsers) -> None:
    add_subparser(
        subparsers, "xinstall", func=xinstall, aliases=[], add_argument=_xinstall_args
    )


def _add_subparser_github(subparsers):
    _add_subparser_dsutil(subparsers)
    _add_subparser_xinstall(subparsers)
    _add_subparser_install_py_github(subparsers)
    _add_subparser_github_(subparsers)
