"""Test the github module.
"""
from subprocess import CalledProcessError
from requests.exceptions import HTTPError
from xinstall.utils import run_cmd


def test_install_py_github():
    """Test the wajig command.
    """
    cmd = "xinstall install_py_github https://github.com/dclong/dsutil"
    run_cmd(cmd)


def test_github():
    """Test the wajig command.
    """
    cmd = "xinstall github -r dclong/xinstall -k whl -o xinstall.wheel"
    msg = "rate limit exceeded for url"
    try:
        run_cmd(cmd)
    except HTTPError as err:
        if msg in str(err):
            return
        raise err
    except CalledProcessError as err:
        if msg in err.stderr.decode():
            return
        raise err
