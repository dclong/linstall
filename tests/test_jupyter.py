"""Test the jupyter module.
"""
import subprocess as sp


def test_evcxr_jupyter():
    """Test installing evcxr Jupyter/Lab kernel.
    """
    cmd = "xinstall --sudo -y evcxr -ic"
    sp.run(cmd, shell=True, check=True)
