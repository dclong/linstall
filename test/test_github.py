"""Test the github module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_install_py_github():
    """Test the wajig command.
    """
    cmd = "xinstall install_py_github https://github.com/dclong/dsutil --sys"
    sp.run(cmd, shell=True, check=True)