"""Test the shell module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_wajig():
    """Test the wajig command.
    """
    cmd = "xinstall --sudo -y wajig -ic"
    sp.run(cmd, shell=True, check=True)
