"""Test the ai module.
"""
import sys
import subprocess as sp
import pytest


def test_kaggle():
    """Test installing the Python package kaggle.
    """
    cmd = "xinstall kaggle -ic"
    sp.run(cmd, shell=True, check=True)


def test_lightgbm():
    """Test installing and configuring LightGBM.
    """
    cmd = "xinstall lightgbm -ic"
    sp.run(cmd, shell=True, check=True)


#@pytest.mark.skipif(sys.version_info >= (3, 9), reason="Skip test on Python 3.9+.")
def test_pytorch():
    """Test installing and configuring PyTorch.
    """
    cmd = "xinstall pytorch -ic"
    sp.run(cmd, shell=True, check=True)
