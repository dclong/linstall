"""Test the dev module.
"""
import subprocess as sp
from xinstall.utils import is_ubuntu_debian, update_apt_source
if is_ubuntu_debian():
    update_apt_source(prefix="sudo", seconds=0)


def test_git():
    """Test installing and configuring Git.
    """
    cmd = "xinstall --sudo -y git -ic"
    sp.run(cmd, shell=True, check=True)


def test_pyjnius():
    """Test installing and configuring pyjnius.
    """
    cmd = "xinstall pyjnius -ic"
    sp.run(cmd, shell=True, check=True)


def test_nodejs():
    """Test installing nodejs.
    """
    cmd = "xinstall --sudo -y nodejs -ic"
    sp.run(cmd, shell=True, check=True)


def test_bash_lsp():
    """Test installing Bash Language Server.
    """
    cmd = "xinstall bash_lsp -c"
    sp.run(cmd, shell=True, check=True)


def test_rust():
    """Test installing the Rust programming language.
    """
    cmd = "xinstall --sudo -y rust -ic"
    sp.run(cmd, shell=True, check=True)


def test_ipython():
    """Test installing and configuring LightGBM.
    """
    cmd = "xinstall ipython -ic"
    sp.run(cmd, shell=True, check=True)