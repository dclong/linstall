
"""Test the shell module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_wajig():
    """Test the wajig command.
    """
    cmd = "sudo xinstall -y wajig -ic"
    sp.run(cmd, shell=True, check=True)
