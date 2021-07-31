"""Test the virtualization module.
"""
import subprocess as sp


def test_kubectl():
    """Test the kubernetes command.
    """
    cmd = "xinstall --sudo kubectl -ic"
    sp.run(cmd, shell=True, check=True)
