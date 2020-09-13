"""Test the xinstall module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_proxychains():
    """Test installing the blogging tools.
    """
    cmd = "xinstall --sudo -y pc -ic"
    sp.run(cmd, shell=True, check=True)
