"""Helper functions.
"""
from typing import Union, List, Any, Sized
import os
import platform
import json
from pathlib import Path
import urllib.request
import shutil
import re
import datetime
import subprocess as sp
import logging
HOME = Path.home()
PLATFORM = platform.platform().lower()
SETTINGS_FILE = HOME / '.linstall.json'
SETTINGS = {}
if os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE) as fin:
        SETTINGS = json.load(fin)


def remove_file_safe(path: Path) -> None:
    """Remove a file or sybmolic link.
    :param path: The path to the file or symbolic link.
    """
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def run_cmd(cmd, shell):
    proc = sp.run(cmd, shell=shell, check=True)
    logging.info(proc.args)


def brew_install_safe(pkgs: Union[str, List]) -> None:
    if isinstance(pkgs, list):
        for pkg in pkgs:
            brew_install_safe(pkg)
        return
    proc = sp.run(
        f'brew ls --versions {pkgs}', shell=True, check=False, stdout=sp.PIPE
    )
    if not proc.stdout:
        run_cmd(f'brew install {pkgs}', shell=True)
    run_cmd(f'brew link {pkgs}', shell=True)


def _any_in_platform(keywords):
    return any(kwd in PLATFORM for kwd in keywords)


def is_ubuntu_debian():
    dists = ('ubuntu', 'debian')
    return _any_in_platform(dists)


def is_linux():
    dists = ('ubuntu', 'debian', 'centos', 'redhat', 'fedora')
    return _any_in_platform(dists)


def is_centos_series():
    dists = ('centos', 'redhat', 'fedora')
    return _any_in_platform(dists)


def is_fedora():
    dists = ('fedora', )
    return _any_in_platform(dists)


def is_macos():
    dists = ('darwin', )
    return _any_in_platform(dists)


def is_win():
    dists = ('win32', )
    return _any_in_platform(dists)


def copy_file(srcfile, dstfile):
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


def update_apt_source(sudo: bool, yes: bool = True, seconds: float = 3600 * 12):
    fmt = '%Y-%m-%d %H:%M:%S.%f'
    key = 'apt_source_update_time'
    time = datetime.datetime.strptime(
        SETTINGS.get(key, '2000-01-01 00:00:00.000000'), fmt
    )
    now = datetime.datetime.now()
    if (now - time).seconds > seconds:
        run_cmd(f"{'sudo ' if sudo else ''}apt-get update {yes}", shell=True)
        SETTINGS[key] = now.strftime(fmt)
        with open(SETTINGS_FILE, 'w') as fout:
            json.dump(SETTINGS, fout)


def _github_version(url) -> str:
    url = f'{url}/releases/latest'
    req = urllib.request.urlopen(url)
    return Path(req.url).name


def install_py_github(url: str, yes: bool = False) -> None:
    version = _github_version(url)
    url = f"{url}/releases/download/{version}/{Path(url).name}-{re.sub('[a-zA-Z]', '', version)}-py3-none-any.whl"
    yes = '-y' if yes else ''
    run_cmd(
        f'pip3 install --user --upgrade {yes} {url}',
        shell=True,
    )
