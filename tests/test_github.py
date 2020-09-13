"""Test the github module.
"""
import subprocess as sp


def test_install_py_github():
    """Test the wajig command.
    """
    cmd = "xinstall install_py_github https://github.com/dclong/dsutil"
    sp.run(cmd, shell=True, check=True)
