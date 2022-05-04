"""Test the shell module.
"""
import subprocess as sp


def test_wajig():
    """Test installing the wajig command.
    """
    cmd = "xinstall --sudo -y wajig -ic"
    sp.run(cmd, shell=True, check=True)


def test_gh():
    """Test installing the gh command.
    """
    cmd = "xinstall --sudo -y gh -ic"
    sp.run(cmd, shell=True, check=True)
