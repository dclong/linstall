"""Test the xinstall module.
"""
import subprocess as sp
from pathlib import Path

DIR_TEST = Path(__file__).resolve().parent
CMD = f"docker build --no-cache -t dclong/xinstall-test -f test/Dockerfile {DIR_TEST.parent}"
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
    """Test installing and configuring NoMachine.
    """
    cmd = "docker run dclong/xinstall-test xinstall nomachine"
    sp.run(cmd, shell=True, check=True)


def test_intellij_idea():
    """Test installing and configuring IntelliJ Idea.
    """
    cmd = "docker run dclong/xinstall-test xinstall intellij"
    sp.run(cmd, shell=True, check=True)


def test_git():
    """Test installing and configuring Git.
    """
    cmd = "docker run dclong/xinstall-test xinstall -y git -ic"
    sp.run(cmd, shell=True, check=True)


def test_pyjnius():
    """Test installing and configuring pyjnius.
    """
    cmd = "docker run dclong/xinstall-test xinstall pyjnius -ic"
    sp.run(cmd, shell=True, check=True)


def test_nodejs():
    """Test installing nodejs.
    """
    cmd = "docker run dclong/xinstall-test xinstall -y nodejs -ic"
    sp.run(cmd, shell=True, check=True)


def test_bash_lsp():
    """Test installing Bash Language Server.
    """
    cmd = "docker run dclong/xinstall-test xinstall bash_lsp -c"
    sp.run(cmd, shell=True, check=True)