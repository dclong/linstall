"""Test the shell module.
"""
import subprocess as sp


def test_wajig():
    """Test the wajig command.
    """
    cmd = "xinstall --sudo -y wajig -ic"
    sp.run(cmd, shell=True, check=True)
