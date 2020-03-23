"""Test the jupyter module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_evcxr_jupyter():
    """Test installing evcxr Jupyter/Lab kernel.
    """
    cmd = "sudo xinstall -y evcxr -ic"
    sp.run(cmd, shell=True, check=True)
