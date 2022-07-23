"""Helper functions.
"""
from __future__ import annotations
from typing import Union, Sequence, Iterable, Any, Sized, Callable
import os
import sys
import json
from pathlib import Path
import shutil
import tempfile
import re
import textwrap
import datetime
import subprocess as sp
import logging
import distro

HOME = Path.home()
USER = HOME.name
FILE = Path(__file__).resolve()
BASE_DIR = FILE.parent / "data"
LOCAL_DIR = HOME / ".local"
BIN_DIR = LOCAL_DIR / "bin"
BIN_DIR.mkdir(0o700, parents=True, exist_ok=True)
DISTRO_ID = distro.id()
# settings of xinstall
SETTINGS_FILE = HOME / ".xinstall.json"
SETTINGS = {}
if os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE, encoding="utf-8") as fin:
        SETTINGS = json.load(fin)


def copy_if_exists(src: Union[Path, str], dst: Path = HOME) -> bool:
    """Copy a file.
    No exception is thrown if the source file does not exist.

    :param src: The path of the source file.
    :param dst: The path of the destination file.
    :return: True if the copy operation succeed and false otherwise.
    """
    try:
        shutil.copy2(src, dst)
        return True
    except FileNotFoundError:
        return False


def link_if_exists(
    src: Union[Path, str], dst: Path = HOME, target_is_directory: bool = True
) -> bool:
    """Make a symbolic link of a file.
    No exception is thrown if the source file does not exist.

    :param src: The path of the source file.
    :param dst: The path of the destination file.
    :param target_is_directory: Please refer to https://docs.python.org/3/library/os.html#os.symlink.
    :return: True if the link operation succeed and false otherwise.
    """
    try:
        Path(dst).unlink()
    except FileNotFoundError:
        pass
    try:
        os.symlink(src, dst, target_is_directory=target_is_directory)
        return True
    except FileNotFoundError:
        return False


def copy_file(srcfile, dstfile):
    """Copy file without throwing exceptions
    when a broken symbolic link already exists at the destination.

    :param srcfile: The source file to copy from.
    :param dstfile: The destination file to copy to.
    """
    _remove_file(dstfile)
    shutil.copy2(srcfile, dstfile)


def _remove_file(path: str):
    if os.path.islink(path):
        os.unlink(path)
    if os.path.isfile(path):
        os.remove(path)
    if os.path.isdir(path):
        shutil.rmtree(path)


def to_bool(value: Any) -> bool:
    """Convert an object to a bool value (True or False).

    :param value: any object that can be converted to a bool value.
    :return: True or False.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ("t", "true", "y", "yes"):
            return True
        if value.isdigit():
            return int(value) != 0
        return False
    if isinstance(value, int) and value != 0:
        return True
    if isinstance(value, Sized) and len(value) > 0:
        return True
    return False


def intellij_idea_plugin(version: str, url: str):
    """Install the specified plugin for IntelliJ IDEA Community Edition.

    :param version: The version of IntelliJ IDEA.
    :param url: The download URL of the plugin to install.
    """
    plugins_dir = f".IdeaIC{version}/config/plugins"
    if is_macos():
        plugins_dir = f"Library/Application Support/IdeaIC{version}"
    plugins_dir = Path.home() / plugins_dir
    plugins_dir.mkdir(mode=0o750, parents=True, exist_ok=True)
    file_dsptr, file = tempfile.mkstemp(suffix=".zip")
    os.close(file_dsptr)
    cmd = f"curl -sSL {url} -O {file} && unzip {file} -d {plugins_dir}"
    run_cmd(cmd)


def option_version(subparser, help: str = ""):
    """Add the option -v/--version to the subparser.

    :param subparser: A sub parser.
    :param help: The help doc for the option.
    """
    if not help:
        help = "The version."
    subparser.add_argument("-v", "--version", dest="version", default="", help=help)


def add_subparser(
    subparsers,
    name: str,
    func: Callable,
    aliases: Sequence = (),
    help_: Union[str, None] = None,
    add_argument: Union[Callable, None] = None
) -> None:
    """Add a sub parser to the main parser.

    :param subparsers: The subparsers handler.
    :param name: The name of the sub command.
    :param func: The function corresponding to the sub parser.
    :param aliases: A list of aliases of the sub command.
    :type aliases: Sequence, optional
    :param help_: Help doc of the sub command. If None, then the help doc of func is used.
    :type help_: Union[str, None], optional
    :param add_argument: A callable object to add aditional arguments
    (in addition to those default arguments), defaults to None
    :type add_argument: Union[Callable, None], optional
    :return:
    """
    sub_cmd = re.sub(r"(\s+)|-", "_", name.lower())
    aliases = [alias for alias in aliases if alias != sub_cmd]
    help_ = help_ if help_ else func.__doc__
    subparser = subparsers.add_parser(sub_cmd, aliases=aliases, help=help_)
    subparser.add_argument(
        "-i", "--install", dest="install", action="store_true", help=f"install {name}."
    )
    subparser.add_argument(
        "-u",
        "--uninstall",
        dest="uninstall",
        action="store_true",
        help=f"uninstall {name}."
    )
    subparser.add_argument(
        "-c",
        "--configure",
        dest="config",
        action="store_true",
        help=f"configure {name}."
    )
    subparser.add_argument(
        "-l",
        "--log",
        dest="log",
        action="store_true",
        help="Print the command to run."
    )
    if add_argument:
        add_argument(subparser)
    subparser.set_defaults(func=func)
    return subparser


def update_file(
    path: Union[str, Path],
    regex: Union[list[tuple[str, str]], None] = None,
    exact: Union[list[tuple[str, str]], None] = None,
    append: Union[str, Iterable[str], None] = None,
    exist_skip: bool = True,
) -> None:
    """Update a text file using regular expression substitution.

    :param path: The path to the file to be updated.
    :param regex: A list of tuples containing regular expression patterns
        and the corresponding replacement text.
    :param exact: A list of tuples containing exact patterns and the corresponding replacement text.
    :param append: A string of a list of lines to append.
        When append is a list of lines, "\n" is automatically added to each line.
    :param exist_skip: Skip appending if already exists.
    """
    if isinstance(path, str):
        path = Path(path)
    text = path.read_text(encoding="utf-8")
    if regex:
        for pattern, replace in regex:
            text = re.sub(pattern, replace, text)
    if exact:
        for pattern, replace in exact:
            text = text.replace(pattern, replace)
    if append:
        if not isinstance(append, str):
            append = "\n".join(append)
        if not exist_skip or append not in text:
            text += append
    path.write_text(text, encoding="utf-8")


def update_dict(dict1, dict2, recursive: bool = False):
    """Update dict1 using dict2.
    """
    if not recursive:
        dict1.update(dict2)
        return
    for key, val in dict2.items():
        if not isinstance(val, dict
                         ) or key not in dict1 or not isinstance(dict1[key], dict):
            dict1[key] = val
            continue
        update_dict(dict1[key], val)

