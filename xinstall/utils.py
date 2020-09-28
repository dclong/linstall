"""Helper functions.
"""
from typing import Union, List, Tuple, Sequence, Iterable, Any, Sized, Dict, Callable
import os
import sys
import json
from pathlib import Path
import urllib.request
import shutil
import tempfile
import re
import datetime
import subprocess as sp
import logging
import distro
logging.basicConfig(
    format=
    "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
    level=logging.INFO
)
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
    src: Union[Path, str], dst: Path = HOME, target_is_directory: bool = True
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
    logging.debug(proc.args)


def brew_install_safe(pkgs: Union[str, List]) -> None:
    """Using Homebrew to install without throwing exceptions if a package to install already exists.

    :param pkgs: A (list of) package(s) to install using Homebrew.
    """
    if isinstance(pkgs, str):
        pkgs = [pkgs]
    for pkg in pkgs:
        run_cmd(
            f"""brew install {pkg} \
            && brew unlink {pkg} \
            && brew link --force --overwrite {pkg}"""
        )


def is_ubuntu_debian():
    """Check whehter the current OS is Ubuntu/Debian.
    """
    return DISTRO_ID in ("ubuntu", "debian")


def is_linux():
    """Check whehter the current OS is Linux. 
    """
    return sys.platform == "linux"


def is_centos_series():
    """Check whehter the current OS belongs to the CentOS series (CentOS, RedHat or Fedora).
    """
    return DISTRO_ID in ("centos", "redhat", "fedora")


def is_fedora():
    """Check whehter the current OS is Fedora.
    """
    return DISTRO_ID == "fedora"


def is_macos():
    """Check whehter the current OS is macOS.
    """
    return DISTRO_ID == "darwin"


def is_win():
    """Check whehter the current OS is Windows.
    """
    return sys.platform == "win32"


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


def update_apt_source(prefix: str = "", yes: str = "--yes", seconds: float = 3600 * 12):
    """Run apt-get update if necessary.

    :param prefix: The prefix command (e.g., sudo) to use.
    :param yes: The yes flag (-y, --yes or an empty string).
    :param seconds: Do not run if this function has already been run `seconds` seconds ago.
    """
    fmt = "%Y-%m-%d %H:%M:%S.%f"
    key = "apt_source_update_time"
    time = datetime.datetime.strptime(
        SETTINGS.get(key, "2000-01-01 00:00:00.000000"), fmt
    )
    now = datetime.datetime.now()
    if (now - time).seconds > seconds:
        run_cmd(f"{prefix} apt-get update {yes}")
        SETTINGS[key] = now.strftime(fmt)
        with open(SETTINGS_FILE, "w") as fout:
            json.dump(SETTINGS, fout)


def _github_version(url) -> str:
    url = f"{url}/releases/latest"
    req = urllib.request.urlopen(url)
    return Path(req.url).name


def install_py_github(url: str, user: bool = False, pip: str = "pip3") -> None:
    """Automatically install the latest version of a Python package from its GitHub repository.

    :param url: The root URL of the GitHub repository.
    :param user: If True, install to user's local directory. 
    This option is equivalant to 'pip install --user'.
    :param pip: The path (pip3 by default) to the pip executable. 
    """
    ver = _github_version(url)
    ver_no_letter = re.sub("[a-zA-Z]", "", ver)
    url = f"{url}/releases/download/{ver}/{Path(url).name}-{ver_no_letter}-py3-none-any.whl"
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


def option_user(subparser):
    """Add the option --user to the subparser.

    :param subparser: A sub parser.
    """
    subparser.add_argument(
        "--user",
        dest="user",
        action="store_true",
        help="Install the Python package to user's local directory."
    )


def option_python(subparser) -> None:
    """Add the option --python into the sub parser.

    :param subparser: A sub parser.
    """
    subparser.add_argument(
        "--python",
        dest="python",
        default="python3",
        help="Path to the python3 command."
    )


def option_ipython(subparser) -> None:
    """Add the option --ipython into the sub parser.

    :param subparser: A sub parser.
    """
    subparser.add_argument(
        "--ipython",
        dest="ipython",
        default="ipython3",
        help="Path to the ipython3 command."
    )


def option_pip(subparser) -> None:
    """Add the option --pip into the sub parser.

    :param subparser: A sub parser.
    """
    subparser.add_argument(
        "--pip", dest="pip", default="pip3", help="Path to the pip command."
    )


def option_jupyter(subparser) -> None:
    """Add the option --jupyter into the sub parser.

    :param subparser: A sub parser.
    """
    subparser.add_argument(
        "--jupyter",
        dest="jupyter",
        default="jupyter",
        help="Path to the jupyter command."
    )


def option_option(subparser) -> None:
    """Add the option --option into the sub parser.

    :param subparser: A sub parser.
    """
    subparser.add_argument(
        "--option", dest="option", default="", help="Additional options."
    )


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
    :param add_argument: A callable object to add aditional arguments (in addition to those default arguments), defaults to None
    :type add_argument: Union[Callable, None], optional
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
    path: Path,
    regex: List[Tuple[str, str]] = None,
    exact: List[Tuple[str, str]] = None,
    append: Union[str, Iterable[str]] = None,
    exist_skip: bool = True,
) -> None:
    """Update a text file using regular expression substitution.
    :param regex: A list of tuples containing regular expression patterns
    and the corresponding replacement text.
    :param exact: A list of tuples containing exact patterns and the corresponding replacement text.
    :param append: A string of a list of lines to append.
    When append is a list of lines, "\n" is automatically added to each line.
    :param exist_skip: Skip appending if already exists.
    """
    if isinstance(path, str):
        path = Path(path)
    text = path.read_text()
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
    path.write_text(text)
