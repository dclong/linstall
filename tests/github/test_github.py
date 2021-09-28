"""Test the github module.
"""
from subprocess import CalledProcessError
from requests.exceptions import HTTPError
from xinstall.utils import run_cmd
from xinstall import github
import subprocess as sp


def test_install_py_github():
    """Test the install_py_github command.
    """
    cmd = "xinstall dsutil -e docker"
    sp.run(cmd, shell=True, check=True)
    github.install_python_lib(
        url="https://github.com/dclong/dsutil",
        user=False,
        extras="docker",
        python="python3"
    )
    cmd = "python3 -c 'import dsutil.docker'"
    sp.run(cmd, shell=True, check=True)


def test_github():
    """Test the github command.
    """
    cmd = "xinstall github -r dclong/xinstall -k whl -o xinstall.wheel"
    msg = "rate limit exceeded for url"
    try:
        run_cmd(cmd, capture_output=True)
    except HTTPError as err:
        if msg in str(err):
            return
        raise err
    except CalledProcessError as err:
        if msg in err.stderr.decode():
            return
        raise err
