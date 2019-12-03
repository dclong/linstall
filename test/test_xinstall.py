"""Test the xinstall module.
"""
import subprocess as sp
from pathlib import Path

DIR_TEST = Path(__file__).resolve().parent
CMD = f"docker build -t dclong/xinstall-test -f test/Dockerfile {DIR_TEST.parent}"
sp.run(CMD, shell=True, check=True)


def test_version():
    """Test the version command.
    """
    cmd = "docker run dclong/xinstall-test xinstall version"
    sp.run(cmd, shell=True, check=True)


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


def test_nomachine():
    """Test installing NoMachine.
    """
    cmd = "docker run dclong/xinstall-test xinstall nomachine"
    sp.run(cmd, shell=True, check=True)


def test_intellij_idea():
    """Test installing IntelliJ Idea.
    """
    cmd = "docker run dclong/xinstall-test xinstall intellij"
    sp.run(cmd, shell=True, check=True)
