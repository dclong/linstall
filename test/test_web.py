"""Test the xinstall module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_blogging():
    """Test installing the blogging tools.
    """
    cmd = "xinstall blog -ic"
    sp.run(cmd, shell=True, check=True)


def test_proxychains():
    """Test installing the blogging tools.
    """
    cmd = "sudo xinstall -y pc -ic"
    sp.run(cmd, shell=True, check=True)

