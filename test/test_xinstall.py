"""Test the xinstall module.
"""
import subprocess as sp
from pathlib import Path

DIR_TEST = Path(__file__).resolve().parent
CMD = f"docker build -t dclong/xinstall-test {DIR_TEST}"
sp.run(CMD, shell=True, check=True)


def test_wajig():
    """Test the wajig command.
    """
    cmd = "docker run dclong/xinstall-test xinstall wajig -yic"
    sp.run(cmd, shell=True, check=True)
