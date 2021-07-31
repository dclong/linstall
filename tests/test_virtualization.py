"""Test the virtualization module.
"""
import subprocess as sp


def test_kubernetes():
    """Test the kubernetes command.
    """
    cmd = "xinstall kubectl -ic"
    sp.run(cmd, shell=True, check=True)
