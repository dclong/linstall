"""Helper functions.
"""
from typing import Union, List, Sequence, Any, Sized, Dict, Callable
from argparse import Namespace
import os
import platform
import json
from pathlib import Path
import urllib.request
import shutil
import tempfile
import re
import datetime
import subprocess as sp
import logging
HOME = Path.home()
USER = HOME.name
USER_ID = os.getuid()
GROUP_ID = os.getgid()
FILE = Path(__file__).resolve()
BASE_DIR = FILE.parent / "data"
LOCAL_DIR = HOME / ".local"
BIN_DIR = LOCAL_DIR / "bin"
BIN_DIR.mkdir(0o700, parents=True, exist_ok=True)

PLATFORM = platform.platform().lower()
SETTINGS_FILE = HOME / ".linstall.json"
SETTINGS = {}
if os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE) as fin:
        SETTINGS = json.load(fin)


def copy_if_exists(src: Union[Path, str], dst: Path = HOME) -> bool:
    """Copy a file.
    No exception is thrown if the source file does not exist.
    :param src: The path of the source file.
    :param dst: The path of the destination file.
    """
    try:
        shutil.copy2(src, dst)
        return True
    except FileNotFoundError:
        return False


def link_if_exists(
    src: Union[Path, str],
    dst: Path = HOME,
    target_is_directory: bool = True
) -> bool:
    """Make a symbolic link of a file.
    No exception is thrown if the source file does not exist.
    :param src: The path of the source file.
    :param dst: The path of the destination file.
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


def remove_file_safe(path: Path) -> None:
    """Remove a file or sybmolic link.
    :param path: The path to the file or symbolic link.
    """
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def run_cmd(cmd: Union[List, str]) -> None:
    """Run a shell command.
    :param cmd: The command to run.
    """
    proc = sp.run(cmd, shell=isinstance(cmd, str), check=True)
    logging.info(proc.args)


def brew_install_safe(pkgs: Union[str, List]) -> None:
    """Using Homebrew to install without throwing exceptions if a package to install already exists.
    :param pkgs: A (list of) package(s) to install using Homebrew.
    """
    if isinstance(pkgs, list):
        for pkg in pkgs:
            brew_install_safe(pkg)
        return
    proc = sp.run(
        f"brew ls --versions {pkgs}", shell=True, check=False, stdout=sp.PIPE
    )
    if not proc.stdout:
        run_cmd(f"brew install {pkgs}")
    run_cmd(f"brew link {pkgs}")


def _any_in_platform(keywords):
    return any(kwd in PLATFORM for kwd in keywords)


def is_ubuntu_debian():
    """Check whehter the current OS is Ubuntu/Debian. 
    """
    dists = ("ubuntu", "debian")
    return _any_in_platform(dists)


def is_linux():
    """Check whehter the current OS is Linux. 
    """
    dists = ("ubuntu", "debian", "centos", "redhat", "fedora")
    return _any_in_platform(dists)


def is_centos_series():
    """Check whehter the current OS belongs to the CentOS series (CentOS, RedHat or Fedora).
    """
    dists = ("centos", "redhat", "fedora")
    return _any_in_platform(dists)


def is_fedora():
    """Check whehter the current OS is Fedora.
    """
    dists = ("fedora", )
    return _any_in_platform(dists)


def is_macos():
    """Check whehter the current OS is macOS.
    """
    dists = ("darwin", )
    return _any_in_platform(dists)


def is_win():
    """Check whehter the current OS is Windows.
    """
    dists = ("win32", )
    return _any_in_platform(dists)


def copy_file(srcfile, dstfile):
    """Copy file without throwing exceptions when a broken symbolic link already exists at the destination.
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


def update_apt_source(yes: bool = True, seconds: float = 3600 * 12):
    """Run apt-get update if necessary.
    :param sudo: If True, run using sudo.
    :param yes: If True, automatically yes to prompt questions.
    :param seconds: Do not run if this function has already been run `seconds` seconds ago.
    """
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    key = "apt_source_update_time"
    time = datetime.datetime.strptime(
        SETTINGS.get(key, "2000-01-01 00:00:00.000000"), fmt
    )
    now = datetime.datetime.now()
    if (now - time).seconds > seconds:
        sudo = "" if USER == "root" else "sudo"
        yes = "--yes" if yes else ""
        run_cmd(f"{sudo} apt-get update {yes}")
        SETTINGS[key] = now.strftime(fmt)
        with open(SETTINGS_FILE, "w") as fout:
            json.dump(SETTINGS, fout)


def _github_version(url) -> str:
    url = f"{url}/releases/latest"
    req = urllib.request.urlopen(url)
    return Path(req.url).name


def install_py_github(
    url: str,
    sudo: bool = False,
    user: bool = False,
    pip: str = "pip3"
) -> None:
    """Automatically install the latest version of a Python package from its GitHub repository.
    :param url: The root URL of the GitHub repository.
    :param sudo: If True, install using sudo.
    :param user: If True, install to user's local directory. 
        This option is equivalant to 'pip install --user'.
    :param pip: The path (pip3 by default) to the pip executable. 
    """
    version = _github_version(url)
    url = f"{url}/releases/download/{version}/{Path(url).name}-{re.sub('[a-zA-Z]', '', version)}-py3-none-any.whl"
    cmd = f"{pip} install {'--user' if user else ''} --upgrade {url}"
    run_cmd(cmd)


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
    fd, file = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    cmd = f"curl -sSL {url} -O {file} && unzip {file} -d {plugins_dir}"
    run_cmd(cmd)


def namespace(dic: Dict) -> Namespace:
    dic.setdefault("sudo", False)
    dic.setdefault("yes", False)
    dic["sudo_s"] = "sudo" if dic["sudo"] else ""
    dic["_sudo_s"] = "--sudo" if dic["sudo"] else ""
    dic["_yes_s"] = "--yes" if dic["yes"] else ""
    return Namespace(**dic)


def option_user(subparser):
    subparser.add_argument(
        "--user",
        dest="user",
        action="store_true",
        help="Install the Python package to user's local directory."
    )


def option_python(subparser):
    subparser.add_argument(
        "--python",
        dest="python",
        default="python3",
        help=f"Path to the python3 command."
    )


def option_ipython(subparser):
    subparser.add_argument(
        "--ipython",
        dest="ipython",
        default="ipython3",
        help=f"Path to the ipython3 command."
    )


def option_pip(subparser):
    subparser.add_argument(
        "--pip", dest="pip", default="pip3", help=f"Path to the pip command."
    )


def option_jupyter(subparser):
    subparser.add_argument(
        "--jupyter",
        dest="jupyter",
        default="jupyter",
        help=f"Path to the jupyter command."
    )


def add_subparser(
    subparsers,
    name: str,
    func: Callable,
    aliases: Sequence = (),
    help_: Union[str, None] = None,
    add_argument: Union[Callable, None] = None
):
    sub_cmd = re.sub(r"(\s+)|-", "_", name.lower())
    aliases = [alias for alias in aliases if alias != sub_cmd]
    help_ = help_ if help_ else f"Install and configure {name}."
    subparser = subparsers.add_parser(sub_cmd, aliases=aliases, help=help_)
    subparser.add_argument(
        "-i",
        "--install",
        dest="install",
        action="store_true",
        help=f"install {name}."
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
        help=f"Print the command to run."
    )
    option_python(subparser)
    option_ipython(subparser)
    option_pip(subparser)
    if add_argument:
        add_argument(subparser)
    subparser.set_defaults(func=func)
    return subparser
