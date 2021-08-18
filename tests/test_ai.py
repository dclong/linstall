"""Test the ai module.
"""
import sys
import subprocess as sp
PY_VER = sys.version_info


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


@pytest.mark.skipif(PY_VER.major == 3 and PY_VER.minor == 9, "Skip test on Python 3.9.")
def test_pytorch():
    """Test installing and configuring PyTorch.
    """
    cmd = "xinstall pytorch -ic"
    sp.run(cmd, shell=True, check=True)