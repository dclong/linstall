"""Test the utils module.
"""
import subprocess as sp
from xinstall import utils


def test_install_py_github():
    """Test the install_py_github command.
    """
    cmd = "xinstall dsutil -e docker"
    sp.run(cmd, shell=True, check=True)
    utils.install_py_github(
        url="https://github.com/dclong/dsutil",
        user=False,
        pip="python3 -m pip",
        extras="docker",
    )
    cmd = "python3 -c 'import dsutil.docker'"
    sp.run(cmd, shell=True, check=True)
