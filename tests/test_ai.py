"""Test the ai module.
"""
import subprocess as sp


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


def test_pytorch():
    """Test installing and configuring PyTorch.
    """
    cmd = "xinstall pytorch -ic"
    sp.run(cmd, shell=True, check=True)