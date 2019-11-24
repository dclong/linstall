"""Test the xinstall module.
"""
import subprocess as sp
from pathlib import Path

DIR_TEST = Path(__file__).resolve().parent
CMD = f"docker build -t dclong/xinstall-test -f test/Dockerfile {DIR_TEST.parent}"
sp.run(CMD, shell=True, check=True)


def test_wajig():
    """Test the wajig command.
    """
    cmd = "docker run dclong/xinstall-test xinstall -y wajig -ic"
    sp.run(cmd, shell=True, check=True)


def test_install_py_github():
    """Test the wajig command.
    """
    cmd = "docker run dclong/xinstall-test xinstall install_py_github https://github.com/dclong/dsutil --sys"
    sp.run(cmd, shell=True, check=True)
